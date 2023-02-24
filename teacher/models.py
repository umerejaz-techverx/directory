from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='teacher_images/', blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=20)
    room_number = models.CharField(max_length=10)
    subjects = models.ManyToManyField(Subject, related_name='teachers')

    def __str__(self):
        return self.first_name
