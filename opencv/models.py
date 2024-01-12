from django.db import models
import uuid

# Create your models here.

class Imgcaptured (models.Model):
    id=models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True,editable=False)
    image=models.ImageField(upload_to='imgcaptured/')
    height=models.FloatField(blank=True, null=True)
    width = models.FloatField(blank=True,null=True)
    canopy=models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Imgcaptured-{self.created_at}"