from django.urls import path

from . import views

app_name = 'pasvir'
urlpatterns = [
    path('', views.home, name='home'),
    path('auditees/', views.AuditeesView.as_view(), name='auditees'),
    path('auditee/new/', views.new_auditee, name='new_auditee'),
    path(
        'auditee/show/<int:auditee_id>/',
        views.show_auditee,
        name='show_auditee',
    ),
    path(
        'auditee/edit/<int:auditee_id>/',
        views.edit_auditee,
        name='edit_auditee',
    ),
    path(
        'auditee/delete/<int:auditee_id>/',
        views.delete_auditee,
        name='delete_auditee',
    ),
    path('documents/', views.DocumentsView.as_view(), name='documents'),
    path('document/new/', views.new_document, name='new_document'),
    path(
        'document/show/<int:document_id>/',
        views.show_document,
        name='show_document',
    ),
    path(
        'document/edit/<int:document_id>',
        views.edit_document,
        name='edit_document',
    ),
    path(
        'document/delete/<int:document_id>/',
        views.delete_document,
        name='delete_document',
    ),
    path(
        'download/<str:path>/',
        views.download_attachment,
        name='download_attachment',
    ),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
]
