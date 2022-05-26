from rest_framework import generics
from .serializers import SnackSerializer
from .models import Snack

class SnackList(generics.ListCreateAPIView):
  queryset = Snack.objects.all()
  serializer_class = SnackSerializer

class SnackDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Snack.objects.all()
  serializer_class = SnackSerializer