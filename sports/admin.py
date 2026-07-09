from django.contrib import admin
from .models import Match

# Rejestrujemy tylko to, co wiemy na 100%, że istnieje
admin.site.register(Match)