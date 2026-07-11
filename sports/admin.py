from django.contrib import admin
from .models import Match, Video, Analysis # Dodaliśmy Analysis do importów

admin.site.register(Match)
admin.site.register(Video)
admin.site.register(Analysis) # Ta linijka dodaje zakładkę do panelu