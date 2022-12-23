from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render
from django.views.generic import ListView

from .forms import AuditeeForm, DocumentForm
from .models import Auditee, City, Document


@login_required(login_url='/admin')
def home(request):
    auditees = Auditee.objects.all().order_by('-id')[:4]
    documents = Document.objects.all().order_by('-id')[:4]
    context = {'navbar': 'home', 'auditees': auditees, 'documents': documents}
    return render(request, 'pasvir/home.html', context)


class AuditeesView(LoginRequiredMixin, ListView):
    login_url = '/admin'
    paginate_by = 10
    model = Auditee
    queryset = Auditee.objects.all()

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = Auditee.objects.filter(
                Q(name__icontains=query)
                | Q(code__icontains=query)
                | Q(email__icontains=query)
            ).order_by('id')
        else:
            object_list = self.model.objects.all().order_by('id')
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_auditees'] = self.queryset.count()
        return context


@login_required(login_url='/admin')
def new_auditee(request):
    form = AuditeeForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Auditee created successfully!')
        return redirect('pasvir:auditees')
    context = {'form': form}
    return render(request, 'pasvir/new_auditee.html', context)


def load_cities(request):
    state_id = request.GET.get('state')
    cities = City.objects.filter(state_id=state_id).order_by('name')
    return render(
        request, 'pasvir/city_dropdown_list_options.html', {'cities': cities}
    )


@login_required(login_url='/admin')
def show_auditee(request, auditee_id):
    try:
        auditee = Auditee.objects.get(pk=auditee_id)
    except Auditee.DoesNotExist:
        raise Http404('Auditado não existe')
    context = {'auditee': auditee}
    return render(request, 'pasvir/show_auditee.html', context)


@login_required(login_url='/admin')
def edit_auditee(request, auditee_id):
    auditee = Auditee.objects.get(pk=auditee_id)
    if request.method == 'POST':
        form = AuditeeForm(request.POST, instance=auditee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Auditee updated successfully!')
            return redirect('pasvir:show_auditee', auditee_id=auditee.id)
    else:
        form = AuditeeForm(instance=auditee)
    context = {'auditee': auditee, 'form': form}
    return render(request, 'pasvir/edit_auditee.html', context)


@login_required(login_url='/admin')
def delete_auditee(request, auditee_id):
    auditee = Auditee.objects.get(pk=auditee_id).delete()
    messages.success(request, 'Auditee deleted successfully!')
    return redirect('pasvir:auditees')


class DocumentsView(LoginRequiredMixin, ListView):
    login_url = '/admin'
    paginate_by = 9
    model = Document
    queryset = Document.objects.all()

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = Document.objects.filter(
                Q(auditee__name__icontains=query)
                | Q(auditee__code__icontains=query)
            ).order_by('id')
        else:
            object_list = self.model.objects.all().order_by('id')
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_documents'] = self.queryset.count()
        return context


@login_required(login_url='/admin')
def new_document(request):
    form = DocumentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Document created successfully!')
        return redirect('pasvir:documents')
    context = {'form': form}
    return render(request, 'pasvir/new_document.html', context)


@login_required(login_url='/admin')
def show_document(request, document_id):
    try:
        document = Document.objects.get(pk=document_id)
    except Document.DoesNotExist:
        raise Http404('Auditado não existe')
    context = {'document': document}
    return render(request, 'pasvir/show_document.html', context)


@login_required(login_url='/admin')
def edit_document(request, document_id):
    document = Document.objects.get(pk=document_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, 'Document updated successfully!')
            return redirect('pasvir:show_document', document_id=document.id)
    else:
        form = DocumentForm(instance=document)
    context = {'document': document, 'form': form}
    return render(request, 'pasvir/edit_document.html', context)


@login_required(login_url='/admin')
def delete_document(request, document_id):
    document = Document.objects.get(pk=document_id).delete()
    messages.success(request, 'Document deleted successfully!')
    return redirect('pasvir:documents')


def download_attachment(request, path):
    document = Document.objects.get(content=path)
    return FileResponse(document.content, as_attachment=True)
