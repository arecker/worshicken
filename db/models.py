import uuid

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_superuser=False):
        user = self.model(email=self.normalize_email(email))
        user.is_superuser = is_superuser
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        return self.create_user(email, password=password, is_superuser=True)


class User(AbstractBaseUser):
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=uuid.uuid4)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_superuser = models.BooleanField(default=False)

    first_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=80, blank=True)
    korean_name = models.CharField(max_length=80, blank=True)

    is_singer = models.BooleanField(default=False, verbose_name='Vocalist?')
    is_sound = models.BooleanField(default=False, verbose_name='Sound?')
    is_slides = models.BooleanField(default=False, verbose_name='Slides?')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        if all([self.first_name, self.last_name]):
            name = f'{self.first_name} {self.last_name}'
            if self.korean_name:
                name += f'({self.korean_name})'
            return name
        return self.get_username()

    class Meta:
        ordering = ('last_name',)


class Invitation(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=uuid.uuid4)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class Instrument(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=uuid.uuid4)
    name = models.CharField(max_length=80)
    musicians = models.ManyToManyField(User, blank=True, related_name='instruments')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Song(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=uuid.uuid4)
    title = models.CharField(max_length=80)

    class Meta:
        ordering = ('title',)


class SongChart(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='charts')
    key = models.CharField(max_length=1, choices=[(c, c.upper()) for c in ['a', 'b', 'c', 'd', 'e', 'f', 'g']])
    pitch = models.CharField(max_length=1, blank=True, choices=[('s', '♯'), ('f', '♭')])
    chart = models.FileField(upload_to='charts')

    def __str__(self):
        return f'{self.key}{self.pitch}'
