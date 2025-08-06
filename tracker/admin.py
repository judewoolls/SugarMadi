from django.contrib import admin

# Register your models here.
from .models import Exercise, BloodSugarReading, Entry, Snack
admin.site.register(Exercise)
admin.site.register(BloodSugarReading)
admin.site.register(Entry)
admin.site.register(Snack)