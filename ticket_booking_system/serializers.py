from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ticket_booking_system.models import Message
from ticket_booking_system.ai_agent import ai_agent_response


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "user", "text", "timestamp", "sender"]
        read_only_fields = ["id", "user", "timestamp", "sender"]


class MessageListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = Message.objects.filter(user=request.user).order_by("timestamp")
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        text = request.data.get("text", "").strip()
        if not text:
            return Response({"error": "No text"}, status=status.HTTP_400_BAD_REQUEST)
        ai_response = ai_agent_response(request.user, text)
        msgs = Message.objects.filter(user=request.user).order_by("-timestamp")[:2]
        user_msg, ai_msg = sorted(msgs, key=lambda m: m.timestamp)
        return Response({
            "user_message": MessageSerializer(user_msg).data,
            "ai_message": MessageSerializer(ai_msg).data
        }, status=status.HTTP_201_CREATED)

    def delete(self, request):
        Message.objects.filter(user=request.user).delete()
        return Response({"status": "history deleted"})
