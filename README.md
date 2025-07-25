# 🎭 Theater Ticket Booking System with AI Chat

A modern Django web application for booking theater tickets, featuring a smart AI assistant for natural language booking, viewing, and cancelling tickets.

---

## 🚀 Features
- **User authentication** with a beautiful login page
- **AI-powered chat** for booking, viewing, and cancelling tickets
- **Unique seat format:** `XX-Y` (row 1-20, seat A-Q, e.g., `17-F`)
- **No double booking**: AI and backend prevent booking the same seat twice
- **Each user sees only their own chat and bookings**
- **Admin panel** for managing shows, actors, authors, and bookings
- **Responsive, modern UI**

---

## 🛠️ Tech Stack
- **Backend:** Django, Django REST Framework, PostgreSQL
- **AI:** OpenAI Agents SDK (function calling)
- **Frontend:** HTML5, CSS3, vanilla JS
- **Docker:** For easy deployment and local development

---

## ⚡ Quick Start with Docker

### 1. Clone the repository
```bash
git clone https://github.com/HappyDen08/Test_task_MomentumSquad.git
cd Test_task_MomentumSquad
```

### 2. Configure environment variables
- Copy `.env.example` to `.env` and set your variables (DB, OpenAI key, etc).

### 3. Build and run the project
```bash
docker compose build
# First run will create and migrate the database automatically
# (all migrations are already included in the repo)
docker compose up
```

### 4. Create a superuser (for admin panel)
```bash
docker compose exec web python manage.py createsuperuser
```
> **Note:** If you load test data (see below), a superuser will already exist:
> - **Admin login:** `admin` / `admin`
> - **Test users:**
>   - `test1` / `qwerty123`
>   - `test2` / `qwerty123`
> - **Test bookings:**
>   - `1-A`, `1-B`, `1-C` for different users (see admin panel or "Show my bookings" in chat)

### 5. Load test data
- Test data load on auto with script

- Visit [http://localhost:8000/login/](http://localhost:8000/login/) to log in
- Visit [http://localhost:8000/admin/](http://localhost:8000/admin/) for the admin panel

---

## 🧑‍💻 How to Use

1. **Login:**
   - Go to `/login/` and sign in with your credentials.
2. **Chat with AI:**
   - Use the chat to book, view, or cancel tickets in natural language.
   - Example queries:
     - `Book seat 5-H for the next performance.`
     - `Show my bookings.`
     - `Cancel booking with id 3.`
3. **Seat format:**
   - Always use format `XX-Y` (e.g., `17-F`). Only rows 1-20 and seats A-Q are valid.
4. **Clear chat history:**
   - Use the "Clear history" button to delete your chat history.
5. **Logout:**
   - Use the "Logout" button to securely exit your session.

---

## 🤖 AI Scenarios
- **Greeting:** Welcomes the user and offers help.
- **Book a ticket:**
  - Example: “Book seat 5-H for the next performance.”
- **View bookings:**
  - Example: “Show my bookings.”
- **Cancel booking:**
  - Example: “Cancel booking with id 3.”
- **Validation:**
  - Only allows booking valid seats (1-20, A-Q), prevents double booking.

---

## 📁 Project Structure
```
Test_task_MomentumSquad/
├── ticket_booking_system/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── ai_agent.py
│   ├── urls.py
│   └── ...
├── templates/
│   ├── login.html
│   └── chat.html
├── manage.py
├── requirements.txt
├── docker-compose.yml
└── ...
```

**Enjoy your smart theater booking experience!** 🎟️🤖 