from django.contrib import admin

from .models import PlantUpload


@admin.register(PlantUpload)
class PlantUploadAdmin(admin.ModelAdmin):
	list_display = ('id', 'predicted_label', 'confidence', 'created_at')
	list_filter = ('predicted_label', 'created_at')
	search_fields = ('predicted_label',)
