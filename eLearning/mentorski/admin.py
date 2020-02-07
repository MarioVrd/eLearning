from django.contrib import admin
from .models import Korisnici, Predmeti, Upisi

# Register your models here.

# admin.site.register(Korisnici)
# admin.site.register(Predmeti)
# admin.site.register(Upisi)

@admin.register(Korisnici)
class KorisniciAdmin(admin.ModelAdmin):
    fields = ('username', 'first_name', 'last_name', 'email', 'role', 'status')
    list_display = ('username', 'first_name', 'last_name', 'email', 'role', 'status')
    list_editable = ('role', 'status')

@admin.register(Predmeti)
class PredmetiAdmin(admin.ModelAdmin):
    fields = ('kod', 'ime', 'bodovi', 'program', 'sem_redovni', 'sem_izvanredni', 'izborni')
    list_display = ('kod', 'ime', 'bodovi', 'program', 'sem_redovni', 'sem_izvanredni', 'izborni')
    list_editable = ('izborni', )

@admin.register(Upisi)
class UpisiAdmin(admin.ModelAdmin):
    fields = ('student', 'predmet', 'status')
    list_display = ('student', 'predmet', 'status')
