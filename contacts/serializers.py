from rest_framework import serializers
from .models import Contact, ContactStatus

class ContactStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactStatus
        fields = ['id', 'name']

class ContactSerializer(serializers.ModelSerializer):
    status = ContactStatusSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=ContactStatus.objects.all(), source='status', write_only=True
    )

    class Meta:
        model = Contact
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone_number',
            'city', 'status', 'status_id', 'created_at'
        ]