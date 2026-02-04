from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import ContactForm
from .models import Contact
from .utils import enrich_contacts

class ContactListView(ListView):
    model = Contact
    template_name = 'contacts/contact_list.html'
    context_object_name = 'contacts'
    paginate_by = 10
    ordering = ['last_name', 'created_at'] 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enrich_contacts(context['contacts'])
        return context

class ContactDetailView(DetailView):
    model = Contact
    template_name = 'contacts/contact_detail.html'
    
class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/contact_form.html'
    success_url = reverse_lazy('contact_list')

class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/contact_form.html'
    success_url = reverse_lazy('contact_list')

class ContactDeleteView(DeleteView):
    model = Contact
    template_name = 'contacts/contact_confirm_delete.html'
    success_url = reverse_lazy('contact_list')