from django.db import models


class PlantUpload(models.Model):
	image = models.ImageField(upload_to='uploads/')
	predicted_label = models.CharField(max_length=255)
	confidence = models.FloatField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.predicted_label} - {self.created_at:%Y-%m-%d %H:%M}'
