from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Korisnici(AbstractUser):
    ROLES = [
        ('mentor', 'Mentor'),
        ('student', 'Student'),
    ]
    role = models.CharField(max_length=15, choices=ROLES, default='student')

    STATUS = [
        ('none', 'None'),
        ('redovni', 'Redovni'),
        ('izvanredni', 'Izvanredni'),
    ]
    status = models.CharField(max_length=15, choices=STATUS, default='none')

    class Meta:
        db_table = 'korisnici'

class Predmeti(models.Model):
    ime = models.CharField(max_length=255)
    kod = models.CharField(max_length=16, unique=True)
    program = models.TextField()
    bodovi = models.IntegerField(null=False)
    sem_redovni = models.IntegerField(null=False)
    sem_izvanredni = models.IntegerField(null=False)

    IZBORNI = [
        ('da', 'Da'),
        ('ne', 'Ne'),
    ]
    izborni = models.CharField(max_length=5, choices=IZBORNI)

    student = models.ManyToManyField(Korisnici, through='Upisi')

    def __str__(self):
        return '%s - %s, %s ECTS' % (self.kod, self.ime, self.bodovi)
    
    
    class Meta:
        db_table = 'predmeti'

class Upisi(models.Model):
    student = models.ForeignKey(Korisnici, on_delete=models.CASCADE)
    predmet = models.ForeignKey(Predmeti, on_delete=models.CASCADE)
    status = models.CharField(max_length=64)

    def __str__(self):
        return '%s - %s - %s' % (self.student, self.predmet, self.status)
    

    class Meta:
        db_table = 'upisi'
