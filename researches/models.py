import os

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from users.models import User
from unistruct.models import Subject
# Create your models here.


class Research(models.Model):
    name = models.TextField()
    subject = models.ForeignKey("unistruct.Subject", on_delete=models.CASCADE, related_name='researches')

    def __str__(self):
        return self.name

    @property
    def len_students(self):
        return len(self.student_researches.all())

    @property
    def student_researches_list(self):
        return self.student_researches.all()
        
def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

class StudentResearch(models.Model):
    research_file = models.FileField(validators=[validate_file_extension])
    research = models.ForeignKey(Research, on_delete=models.CASCADE, related_name='student_researches')
    students = models.ManyToManyField("users.User", related_name='student_researches')
    # References Field
    references = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ])

    # Conclusions Field
    conclusions = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(20),
            MinValueValidator(0)
        ])

    # Content Field
    content = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(40),
            MinValueValidator(0)
        ])

    # Axes Field
    axes = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(20),
            MinValueValidator(0)
        ])

    # Intro Field
    intro = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ])

    seen = models.BooleanField(default=False)
    corrected = models.BooleanField(default=False)
    corrected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.research.name}"
    
    @property
    def passed(self):
        evaluation_items = [self.references, self.conclusions, self.content, self.axes, self.intro]
        return True if (sum(evaluation_items) >= 50) else False

    @property
    def total(self):
        evaluation_items = [self.references, self.conclusions, self.content, self.axes, self.intro]
        return sum(evaluation_items)

    @property
    def students_list(self):
        return self.students.all()

    @property
    def first_student(self):
        return self.students.first()

    def len_students_list(self):
        return len(self.students.all())
