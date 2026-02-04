from django.views.generic import ListView, DetailView
from .models import Contact

class ContactListView(ListView):
    model = Contact
    template_name = 'contacts/contact_list.html'
    context_object_name = 'contacts'
    paginate_by = 10
    ordering = ['last_name', 'created_at'] 
    
class ContactDetailView(DetailView):
    model = Contact
    template_name = 'contacts/contact_detail.html'