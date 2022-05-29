from django.db import models


class User(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=50)
    salt = models.CharField(max_length=50)

    class Meta:
        indexes = [
            models.indexes.Index(fields=['username'], name='username')
        ]


class HealthUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    real_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    tel = models.CharField(max_length=11)


class NuclearicAcid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.IntegerField()
    place = models.CharField(max_length=50)


class Cookie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cookie = models.CharField(max_length=50, unique=True)
    TTL = models.DateTimeField()

    class Meta:
        indexes = [
            models.indexes.Index(fields=['cookie'], name='cookie'),
            models.indexes.Index(fields=['user'], name='user')
        ]
