from django.contrib import admin
from ticket_booking_system.models import Booking, User, Performance, Actor, Author


admin.site.register(Booking)
admin.site.register(User)
admin.site.register(Performance)
admin.site.register(Actor)
admin.site.register(Author)