from django.db import models

class baza_ogloszen(models.Model):
    tytul = models.CharField(max_length=80)
    lokalizacja = models.CharField(max_length=80)
    cena = models.CharField(max_length=30)
    cena_za_metr = models.CharField(max_length=30)
    liczba_pokoi = models.CharField(max_length=30)
    powierzchnia = models.CharField(max_length=20)
    url_link = models.TextField(max_length=200)
    data_wystawienia = models.DateTimeField()
    data_zakonczenia = models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return self.tytul



