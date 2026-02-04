from django.contrib import admin
from .models import Contact, ContactStatus

admin.site.register(Contact)
admin.site.register(ContactStatus)