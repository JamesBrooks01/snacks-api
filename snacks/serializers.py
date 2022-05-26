from rest_framework import serializers
from .models import Snack

class SnackSerializer(serializers.ModelSerializer):
  class Meta:
    fields = ('id', 'purchaser', 'title', 'description', 'created_on', 'updated_on')
    model = Snack