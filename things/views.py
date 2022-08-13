from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Thing
from .serializers import ThingsSerializer
from .permissions import IsOwnerOrReadOnly


# Create your views here.
class ThingListView(ListCreateAPIView):
    queryset = Thing.objects.all()
    serializer_class = ThingsSerializer


class ThingDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Thing.objects.all()
    serializer_class = ThingsSerializer
    permission_classes = [IsOwnerOrReadOnly]
