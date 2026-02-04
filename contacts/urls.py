from django.urls import path
from .views import ContactListView, ContactDetailView, ContactUpdateView, ContactCreateView, ContactDeleteView

urlpatterns = [
    path('', ContactListView.as_view(), name='contact_list'),
    path('add/', ContactCreateView.as_view(), name='contact_add'),
    path('<int:pk>/', ContactDetailView.as_view(), name='contact_detail'),
    path('<int:pk>/edit/', ContactUpdateView.as_view(), name='contact_edit'),
    path('<int:pk>/delete/', ContactDeleteView.as_view(), name='contact_delete'),
]