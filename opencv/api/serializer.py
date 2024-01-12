from rest_framework import serializers
from ..models import Imgcaptured

class ImgcapturedModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imgcaptured
        fields = ('image','height','width','canopy',)