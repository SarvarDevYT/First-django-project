from django.db import models


class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone = models.IntegerField()
    joined_date = models.IntegerField()
    age = models.IntegerField()
    avatar = models.ImageField(upload_to='avatars/')
    bio = models.TextField()

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

