from django.urls import path
from ticket_booking_system.views import CustomLoginView, CustomLogoutView, chat_view
from ticket_booking_system.serializers import MessageListCreateAPIView

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("chat/", chat_view, name="chat"),
    path("api/messages/", MessageListCreateAPIView.as_view(), name="messages_api"),
]