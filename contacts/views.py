import csv
import json
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.decorators.http import require_GET
from django.urls import reverse_lazy
from django.shortcuts import render
from .forms import ContactForm
from .models import Contact, ContactStatus
from .utils import validate_contact_row, get_coordinates, get_weather

class ContactListView(ListView):
    model = Contact
    template_name = 'contacts/contact_list.html'
    context_object_name = 'contacts'
    paginate_by = 10
    
    def get_ordering(self):
        sort = self.request.GET.get('sort')
        direction = self.request.GET.get('dir', 'asc')
        ordering = ['last_name', 'created_at']

        if sort in ['first_name', 'last_name', 'created_at']:
            if direction == 'desc':
                ordering = [f'-{sort}']
            else:
                ordering = [sort]

        return ordering
    
    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q', '').strip()
        if query:
            qs = qs.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
        return qs.order_by(*self.get_ordering())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort', '')
        context['current_dir'] = self.request.GET.get('dir', 'asc')
        context['current_query'] = self.request.GET.get('q', '')
        for contact in context['contacts']:
            contact.coordinates = None
            contact.weather = None
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
    

@require_GET
def contact_weather(request, pk):
    from .models import Contact
    try:
        contact = Contact.objects.get(pk=pk)
    except Contact.DoesNotExist:
        return JsonResponse({"error": "Contact not found"}, status=404)

    lat, lon = get_coordinates(contact.city)
    weather = get_weather(lat, lon, contact.city)
    return JsonResponse({
        "coordinates": {"lat": lat, "lon": lon},
        "weather": weather
    })
    

def preview_csv(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]

        if not csv_file.name.endswith('.csv'):
            return JsonResponse({"error": "The file must be a CSV"}, status=400)

        decoded_file = csv_file.read().decode('utf-8-sig').splitlines()
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



def import_csv_json(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            selected_rows = data.get("selected_rows", [])
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        created_count = 0
        for item in selected_rows:
            row = item["row"]

            status_name = row.get("status")
            status_obj = ContactStatus.objects.filter(name=status_name).first() if status_name else None

            Contact.objects.create(
                first_name=row.get("first_name"),
                last_name=row.get("last_name"),
                email=row.get("email"),
                phone_number=row.get("phone_number"),
                city=row.get("city"),
                status=status_obj
            )
            created_count += 1

        return JsonResponse({"success": True, "created": created_count})

    return JsonResponse({"error": "Invalid request method"}, status=405)

def export_contacts_csv(request):
    contacts = Contact.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts_export.csv"'

    response.write('\ufeff')

    writer = csv.writer(response)
    writer.writerow(['first_name', 'last_name', 'email', 'phone', 'city', 'status'])


    for contact in contacts:
        writer.writerow([
            contact.first_name,
            contact.last_name,
            contact.email,
            contact.phone_number,
            contact.city,
            contact.status.name if contact.status else ''
        ])

    return response