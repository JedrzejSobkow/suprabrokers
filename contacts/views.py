import csv
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from .forms import ContactForm
from .models import Contact, ContactStatus
from .utils import enrich_contacts, validate_contact_row

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
    


def preview_csv(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]

        if not csv_file.name.endswith('.csv'):
            return JsonResponse({"error": "The file must be a CSV"}, status=400)

        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        
        existing_emails = set(Contact.objects.values_list('email', flat=True))
        existing_phones = set(Contact.objects.values_list('phone_number', flat=True))
        valid_statuses = set(ContactStatus.objects.values_list('name', flat=True))
        
        imported_rows = []

        for row in reader:
            errors = validate_contact_row(row, existing_emails, existing_phones, valid_statuses)
            imported_rows.append({
                "row": row,
                "errors": errors,
                "is_valid": len(errors) == 0
            })

        return JsonResponse({"rows": imported_rows})

    return JsonResponse({"error": "No file uploaded"}, status=400)


def import_csv_page(request):
    return render(request, 'contacts/import_csv.html')