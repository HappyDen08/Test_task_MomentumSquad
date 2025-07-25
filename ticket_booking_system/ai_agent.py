import json
import os

from openai import OpenAI
from django.utils import timezone
from ticket_booking_system.models import Performance, Booking, Message

client = OpenAI(api_key=os.getenv("OPENAI_SECRET_KEY"))


def get_upcoming_performances_func():
    now = timezone.now()
    performances = Performance.objects.filter(date__gte=now).order_by("date")[:5]
    return [
        {
            "id": p.id,
            "name": p.name,
            "date": p.date.strftime("%Y-%m-%d %H:%M"),
            "author": str(p.author) if p.author else "",
            "actors": [str(a) for a in p.actors.all()]
        }
        for p in performances
    ]


def create_booking_func(user_id, performance_id, seat_code, real_user_id=None):
    user_id = real_user_id or user_id
    try:
        row_str, seat = seat_code.split("-")
        row = int(row_str)
    except Exception:
        return "Invalid seat format. Use format 1-20 for row and A-Q for seat, e.g., 17-F."
    if not (1 <= row <= 20) or seat not in [chr(i) for i in range(ord("A"), ord("Q")+1)]:
        return "Seat does not exist. Row must be 1-20, seat must be A-Q."
    if Booking.objects.filter(performance_id=performance_id, row=row, seat=seat).exists():
        return "This seat is already booked."
    booking = Booking.objects.create(
        user_id=user_id,
        performance_id=performance_id,
        row=row,
        seat=seat
    )
    return f"Booking created: {booking}"


def get_user_bookings_func(user_id, real_user_id=None):
    user_id = real_user_id or user_id
    bookings = Booking.objects.filter(user_id=user_id)
    return [
        {
            "id": b.id,
            "performance": str(b.performance),
            "seat_code": f"{b.row}-{b.seat}"
        }
        for b in bookings
    ]


def cancel_booking_func(user_id, booking_id, real_user_id=None):
    user_id = real_user_id or user_id
    print(f"[DEBUG] cancel_booking_func called with user_id={user_id}, booking_id={booking_id}")
    try:
        booking = Booking.objects.get(id=booking_id, user_id=user_id)
        booking.delete()
        print(f"[DEBUG] Booking {booking_id} deleted for user {user_id}")
        return "Booking cancelled."
    except Booking.DoesNotExist:
        print(f"[DEBUG] Booking {booking_id} not found for user {user_id}")
        return "Booking not found."


function_specs = [
    {
        "name": "get_upcoming_performances",
        "description": "Get a list of upcoming performances.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "create_booking",
        "description": "Create a booking for a ticket. Seat must be in format XX-Y, where XX is row (1-20) and Y is seat (A-Q), e.g., 17-F.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "integer"},
                "performance_id": {"type": "integer"},
                "seat_code": {"type": "string", "description": "Seat in format XX-Y, e.g., 17-F"}
            },
            "required": ["user_id", "performance_id", "seat_code"]
        }
    },
    {
        "name": "get_user_bookings",
        "description": "Get a list of user's bookings.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "integer"},
            },
            "required": ["user_id"]
        }
    },
    {
        "name": "cancel_booking",
        "description": "Cancel a user's booking by booking id. Always use the id from the user's bookings list.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "integer"},
                "booking_id": {"type": "integer"}
            },
            "required": ["user_id", "booking_id"]
        }
    }
]


def ai_agent_response(user, text):

    Message.objects.create(user=user, text=text, sender="user")

    messages = (
        Message.objects
        .filter(user=user)
        .order_by("timestamp")[:30]
    )

    chat_history = [
        {"role": msg.sender if msg.sender != "ai" else "assistant", "content": msg.text}
        for msg in messages
    ]

    if not any(msg["role"] == "system" for msg in chat_history):
        chat_history.insert(0, {
            "role": "system",
            "content": (
                "You are an assistant for booking theater tickets. "
                "Greet the user only once at the beginning of the conversation. "
                "Help them find performances, book seats (only existing seats: rows 1-20, seats A-Q), show and cancel bookings. "
                "Do not allow double booking of the same seat. "
                "If the user wants to book a ticket, ask for the performance and seat in format XX-Y, e.g., 17-F."
                "To cancel a booking, always use the booking id from the user's bookings list and call the cancel_booking function."
                "Never say that a booking is cancelled unless you have called the cancel_booking function and received confirmation."
            )
        })

    # 5. Виклик OpenAI
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=chat_history,
        functions=function_specs,
        function_call="auto"
    )

    choice = response.choices[0]

    if choice.finish_reason == "function_call":
        func_call = choice.message.function_call
        name = func_call.name
        args = json.loads(func_call.arguments)

        if name == "get_upcoming_performances":
            result = get_upcoming_performances_func()
        elif name == "create_booking":
            result = create_booking_func(real_user_id=user.id, **args)
        elif name == "get_user_bookings":
            result = get_user_bookings_func(real_user_id=user.id, **args)
        elif name == "cancel_booking":
            result = cancel_booking_func(real_user_id=user.id, **args)
        else:
            result = "Unknown function."

        chat_history.append(choice.message.model_dump())
        chat_history.append({
            "role": "function",
            "name": name,
            "content": json.dumps(result)
        })

        second_response = client.chat.completions.create(
            model="gpt-4.1",
            messages=chat_history
        )
        reply = second_response.choices[0].message.content
    else:
        reply = choice.message.content

    Message.objects.create(user=user, text=reply, sender="ai")

    return reply
