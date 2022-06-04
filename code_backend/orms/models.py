from django.db import models


class User(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=50)
    salt = models.CharField(max_length=50)
    admin = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.indexes.Index(fields=['username'])
        ]


class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    real_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    age = models.IntegerField(default=0)
    tel = models.CharField(max_length=15)
    real_id = models.CharField(max_length=18, unique=True)


class NuclearicAcid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()
    status = models.IntegerField()
    place = models.CharField(max_length=50)


class Cookie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cookie = models.CharField(max_length=50, unique=True)
    TTL = models.DateTimeField()

    class Meta:
        indexes = [
            models.indexes.Index(fields=['cookie']),
            models.indexes.Index(fields=['user'])
        ]


class Color(models.Model):
    class Type(models.IntegerChoices):
        Green = 1
        Yellow = 2
        Red = 3

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.IntegerField(choices=Type.choices)


class Place(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Passing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    time = models.DateTimeField()

    class Meta:
        indexes = [
            models.indexes.Index(fields=['place']),
            models.indexes.Index(fields=['user']),
            models.indexes.Index(fields=['time'])
        ]
