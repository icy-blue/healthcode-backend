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
    age = models.IntegerField(default=-1)
    tel = models.CharField(max_length=15)
    real_id = models.CharField(max_length=18)


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
