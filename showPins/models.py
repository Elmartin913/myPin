from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator




# Create your models here.


DELIVERY = (
    (1, 'Odbiór osobity'),
    (2, 'Dostawa email'),
    (3, 'Przesyłka pocztowa'),
)


class User(AbstractUser):
    email = models.EmailField(verbose_name='Email')
    first_name = models.CharField(max_length=256, verbose_name='Imie')
    last_name = models.CharField(max_length=256, null=True, verbose_name='Nazwisko')
    user_desc = models.TextField(null=True, blank=True, verbose_name='Kilka slow o sobie')
    add_date = models.DateField(auto_now_add=True)
    collecion = models.IntegerField(null=True, verbose_name='Kolekcja')
    # photo

    def name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return self.name()


class Photo(models.Model):
    path = models.ImageField(upload_to='photos', verbose_name='Zdjecie')
    title = models.CharField(max_length=128, null=True, verbose_name='Tytul')
    creation_date = models.DateField(auto_now_add=True)
    photo_desc = models.CharField(max_length=128, null=True,blank=True, verbose_name='opis zdjecia')
    price = models.FloatField(default=1.99)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # like, # comment

    class Meta:
        verbose_name = 'Zdjecie'
        verbose_name_plural = 'Zdjecia'
        ordering = ['-creation_date']

    def __str__(self):
        return self.title


class Like(models.Model):
    add_like = models.DateField(auto_now_add=True)
    like_type = models.IntegerField(default=0, verbose_name='Like')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

    def __str__(self):
        return self.like_type


class Comment(models.Model):
    add_comment = models.DateField(auto_now_add=True)
    comment = models.CharField(max_length=128, null=True, verbose_name='Komentarz')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment


class Subscribe(models.Model):
    email_id = models.EmailField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email_id


class Collection(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)


class Card(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    add_card = models.DateField(auto_now_add=True)
    modify_card = models.DateField(auto_now=True)
    buy_price = models.FloatField(default=99999999, verbose_name='Cena zakupy')
    quantity = models.IntegerField(default=1, verbose_name='Liczba')
    delivery = models.IntegerField(choices=DELIVERY, default=2, verbose_name='Rodzaj dostawy')


class OrderId(models.Model):

    add_date = models.DateField(auto_now_add=True)
    buy_price = models.FloatField(default=99999999, verbose_name='Cena zakupu')
    total_price = models.FloatField(default=99999999, verbose_name='Cena zakupy')
    quantity = models.IntegerField(default=1, verbose_name='Liczba')
    delivery = models.IntegerField(choices=DELIVERY, null=True, verbose_name='Rodzaj dostawy')
    delivery_target = models.CharField(max_length=256, null=True, blank=True)
    user = models.ForeignKey(User)
    photo = models.ManyToManyField(Photo)