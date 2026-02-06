from django.urls import path
from .views import (
    ContactListView, 
    ContactDetailView, 
    ContactUpdateView, 
    ContactCreateView, 
    ContactDeleteView, 
    contact_weather,
    preview_csv, 
    import_csv_page,
    import_csv_json,
    export_contacts_csv
)
from . import api_views

urlpatterns = [
    path('', ContactListView.as_view(), name='contact_list'),
    path('add/', ContactCreateView.as_view(), name='contact_add'),
    path('<int:pk>/', ContactDetailView.as_view(), name='contact_detail'),
    path('<int:pk>/edit/', ContactUpdateView.as_view(), name='contact_edit'),
    path('<int:pk>/delete/', ContactDeleteView.as_view(), name='contact_delete'),
    
    path('contacts/', api_views.ContactListCreateAPI.as_view(), name='api_contact_list'),
    path('contacts/<int:pk>/', api_views.ContactRetrieveUpdateDestroyAPI.as_view(), name='api_contact_detail'),
    
    path('<int:pk>/weather/', contact_weather, name='contact_weather'),
    
    path('import/', import_csv_page, name='import_csv_page'),
    path('import/preview/', preview_csv, name='preview_csv'),
    path('import/json/', import_csv_json, name='import_csv_json'),
    path('export/', export_contacts_csv, name='export_csv'),
]