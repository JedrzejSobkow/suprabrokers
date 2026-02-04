from django.core.validators import RegexValidator
from django.db import models

# VALIDATORS:
phone_validator = RegexValidator(
    regex=r'^\+?\d{7,15}$',
    message="Phone number must be entered in the format: '+999999999'. From 7 to 15 digits allowed."
)


# MODELS:
class ContactStatus(models.Model): # The task description suggested using ContactStatusChoices
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(validators=[phone_validator], max_length=16, unique=True)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=100)
    status = models.ForeignKey(ContactStatus, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"