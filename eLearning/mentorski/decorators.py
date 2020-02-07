from .models import Korisnici
from django.shortcuts import redirect

"""def deorator(function):
    def wrap(request, *args, **kwargs):
        if SOMETHING:
            return function(request, *args, **kwargs)
        else:
            REJECT
    return wrap""" # spranca za custom dekorator

def mentor_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.role == 'mentor':#ako ulogirani korisnik ima odgovarajuću rolu pozove se funkcija koja je dekorirana
            return function(request, *args, **kwargs)
        else:
            return redirect('index')
    return wrap

def student_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.role == 'student':#ako ulogirani korisnik ima odgovarajuću rolu pozove se funkcija koja je dekorirana
            return function(request, *args, **kwargs)
        else:
            return redirect('index')
    return wrap
