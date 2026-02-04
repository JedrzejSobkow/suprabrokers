from django.urls import path
from .views import ContactListView, ContactDetailView

urlpatterns = [
    path('', ContactListView.as_view(), name='contact_list'),
    path('<int:pk>/', ContactDetailView.as_view(), name='contact_detail'),
]