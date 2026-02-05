from rest_framework import generics
from .models import Contact
from .serializers import ContactSerializer

class ContactListCreateAPI(generics.ListCreateAPIView):
    queryset = Contact.objects.all().order_by('last_name', 'created_at')
    serializer_class = ContactSerializer

class ContactRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer