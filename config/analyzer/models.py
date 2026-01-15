from django.db import models

class Student(models.Model):
    roll_number = models.IntegerField()  # NOT NULL by default
    name = models.CharField(max_length=100)

    physics_q = models.IntegerField()
    physics_h = models.IntegerField()
    physics_p = models.IntegerField()

    maths_q = models.IntegerField()
    maths_h = models.IntegerField()
    maths_p = models.IntegerField()

    chemistry_q = models.IntegerField()
    chemistry_h = models.IntegerField()
    chemistry_p = models.IntegerField()

    english_q = models.IntegerField()
    english_h = models.IntegerField()
    english_p = models.IntegerField()

    attendance = models.IntegerField()

    def __str__(self):
        return f"{self.roll_number} - {self.name}"
