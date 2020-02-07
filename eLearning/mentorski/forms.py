from django.forms import ModelForm
from .models import Predmeti, Korisnici
from django.contrib.auth.forms import UserCreationForm

class PredmetForm(ModelForm):
    class Meta:
        model = Predmeti
        fields = ['ime', 'kod', 'program', 'bodovi', 'sem_redovni', 'sem_izvanredni', 'izborni']

class KorisniciForm(UserCreationForm):
        class Meta:
                model = Korisnici
                fields = ('username','password1', 'password2', 'email', 'status')
