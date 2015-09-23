from django.contrib import admin
from .models import Doctor, Reception


class ReceptionInline(admin.TabularInline):
    model = Reception
    ordering = ('-datetime', )
    readonly_fields = ('datetime', 'patient')
    extra = 0

class DoctorAdmin(admin.ModelAdmin):
    inlines = [ReceptionInline]


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Reception)

