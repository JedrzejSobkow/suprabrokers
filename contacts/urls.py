from django.urls import path
from .views import ContactListView, ContactDetailView, ContactUpdateView, ContactCreateView, ContactDeleteView, preview_csv, import_csv_page
from . import api_views

urlpatterns = [
    path('', ContactListView.as_view(), name='contact_list'),
    path('add/', ContactCreateView.as_view(), name='contact_add'),
    path('<int:pk>/', ContactDetailView.as_view(), name='contact_detail'),
    path('<int:pk>/edit/', ContactUpdateView.as_view(), name='contact_edit'),
    path('<int:pk>/delete/', ContactDeleteView.as_view(), name='contact_delete'),
    
    path('api/contacts/', api_views.ContactListCreateAPI.as_view(), name='api_contact_list'),
    path('api/contacts/<int:pk>/', api_views.ContactRetrieveUpdateDestroyAPI.as_view(), name='api_contact_detail'),
    
    path('import/', import_csv_page, name='import_csv_page'),
    path('import/preview/', preview_csv, name='preview_csv'),
]