from django.contrib import admin
from embeds.models import SavedEmbed

class SavedEmbedAdmin(admin.ModelAdmin):
    list_display = ('url', 'type', 'last_updated')
    list_filter = ('type', 'last_updated')

admin.site.register(SavedEmbed, SavedEmbedAdmin)
