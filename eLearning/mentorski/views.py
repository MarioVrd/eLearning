from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Korisnici, Predmeti, Upisi
from .forms import PredmetForm, KorisniciForm
from .decorators import mentor_required, student_required

# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'GET':
        korisniciForm = KorisniciForm()
        return render(request, 'register.html', {'form': korisniciForm})
    elif request.method == 'POST':
        korisniciForm = KorisniciForm(request.POST)
        if korisniciForm.is_valid():
            korisniciForm.save()
            Korisnici.objects.filter(email = korisniciForm.cleaned_data.get('email')).update(role = "student")
            return redirect('login')
        else:
            return render(request, 'register.html', {'form': korisniciForm})
    else:
        return HttpResonseNotAllowed()

@student_required
def upisni_list(request):
    if (request.user.is_authenticated):
        username = request.user.get_username()
        student = Korisnici.objects.get(username=username)
        if (request.method == 'POST'):
            if request.POST.get('enroll'):
                predmet_id = request.POST.get('enroll')
                print(predmet_id)
                if not Upisi.objects.filter(student_id=student.id, predmet_id=predmet_id):
                    Upisi.objects.create(student_id=student.id, predmet_id=predmet_id, status='enrolled')
            elif request.POST.get("disenroll"):
                disenroll_id = request.POST.get("disenroll")
                print(disenroll_id)
                Upisi.objects.filter(predmet_id=disenroll_id, student_id=student.id).delete()
            elif request.POST.get("passed"):
                passed_id = request.POST.get("passed")
                print(passed_id)
                Upisi.objects.filter(predmet_id=passed_id, student_id=student.id).update(status="passed")

        upisani = Upisi.objects.filter(student=student.id).order_by('predmet_id')
        predmeti = Predmeti.objects.exclude(id__in=upisani.values('predmet_id'))
        br_semestara = 6 if student.status == "redovni" else 8
        context = {
            'predmeti': predmeti, 
            'upisani': upisani, 
            'student': student, 
            'semestri': range(1, br_semestara + 1)
        }
        return render(request, 'upisni-list.html', context)
    else:
        return redirect('login')

@mentor_required
def upisni_list_studenta(request, student_id):
    student = Korisnici.objects.get(id=student_id)
    if (request.method == 'POST'):
        if request.POST.get('enroll'):
            predmet_id = request.POST.get('enroll')
            print(predmet_id)
            if not Upisi.objects.filter(student_id=student.id, predmet_id=predmet_id):
                Upisi.objects.create(student_id=student.id, predmet_id=predmet_id, status='enrolled')
        elif request.POST.get("disenroll"):
            disenroll_id = request.POST.get("disenroll")
            print(disenroll_id)
            Upisi.objects.filter(predmet_id=disenroll_id, student_id=student.id).delete()
        elif request.POST.get("passed"):
            passed_id = request.POST.get("passed")
            print(passed_id)
            Upisi.objects.filter(predmet_id=passed_id, student_id=student.id).update(status="passed")

    upisani = Upisi.objects.filter(student=student.id).order_by('predmet_id')
    predmeti = Predmeti.objects.exclude(id__in=upisani.values('predmet_id'))
    br_semestara = 6 if student.status == "redovni" else 8
    context = {
        'predmeti': predmeti, 
        'upisani': upisani, 
        'student': student, 
        'semestri': range(1, br_semestara + 1)
    }
    return render(request, 'upisni-list.html', context)

@mentor_required
def predmeti(request):
    if request.method == 'GET':
        predmeti = Predmeti.objects.all()
        return render(request, 'predmeti.html', {'predmeti': predmeti})
    elif request.method == 'POST':
        if request.POST.get("delete"):
            delete_id = request.POST.get("delete")
            Predmeti.objects.filter(id=delete_id).delete()
            return redirect('predmeti')


@mentor_required
def studenti(request):
    studenti = Korisnici.objects.filter(role='student')
    return render(request, 'studenti.html', {'studenti': studenti})


@mentor_required
def dodaj_predmet(request):
    if request.method == 'GET':
        predmetForm = PredmetForm()
        return render(request, 'dodaj-predmet.html', {'form': predmetForm})
    elif request.method == 'POST':
        predmetForm = PredmetForm(request.POST)
        if predmetForm.is_valid():
            predmetForm.save()
            return redirect('predmeti')
        else:
            return redirect('dodaj-predmet') # TODO ispisi gresku ako ne uspije (try - except)

@mentor_required
def predmet_detalji(request, predmet_id):
    predmet = Predmeti.objects.get(id=predmet_id)
    studenti = Korisnici.objects.filter(id__in=predmet.upisi_set.all().values('student_id'))
    return render(request, 'predmet-detalji.html', {'predmet': predmet, 'studenti': studenti})

def uredi_predmet(request, predmet_id):
    predmet = Predmeti.objects.get(id=predmet_id)
    if request.method == 'GET':
        predmetForm = PredmetForm()
        predmetForm.fields['ime'].initial = predmet.ime
        predmetForm.fields['kod'].initial = predmet.kod
        predmetForm.fields['program'].initial = predmet.program
        predmetForm.fields['bodovi'].initial = predmet.bodovi
        predmetForm.fields['sem_redovni'].initial = predmet.sem_redovni
        predmetForm.fields['sem_izvanredni'].initial = predmet.sem_izvanredni
        predmetForm.fields['izborni'].initial = predmet.izborni
        return render(request, 'uredi-predmet.html', {'form': predmetForm})
    elif request.method == 'POST':
        predmetForm = PredmetForm(request.POST, instance=predmet)
        if predmetForm.is_valid():
            predmetForm.save()
            return redirect('predmeti')
        else: 
            return render(request, 'uredi-predmet.html', {'form': predmetForm})
