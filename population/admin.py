from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

@admin.register(Population)
class PopulationAdmin(ImportExportModelAdmin):
    list_display = ('name','code','year','value')
    list_filter = ['name']
    search_fields = ['name']