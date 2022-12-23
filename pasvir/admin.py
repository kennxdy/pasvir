from django.contrib import admin

from .models import City, State


class StateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id', 'name']
    list_per_page = 10


class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id', 'name']
    list_per_page = 10


admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)

admin.site.site_header = 'Pasvir'
admin.site.site_title = 'Pasvir administration area'
admin.site.index_title = 'Pasvir administration'
