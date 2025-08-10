from django.contrib import admin
from events.models import Category, Event

admin.site.register(Event)
admin.site.register(Category)

