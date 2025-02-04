from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=30)


class Student(models.Model):
    name = models.CharField(max_length=30)
    courses = models.ManyToManyField(Course, through="Enrollment")


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()  # дата поступления
    mark = models.IntegerField(max_value=5)  # полученный балл