from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('subject', 'name')

    def __str__(self):
        return f"{self.subject.name} - {self.name}"

class ExamPaper(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    term = models.CharField(max_length=20, blank=True)  # e.g., "Term 1", "Midyear"
    file = models.FileField(upload_to='exam_papers/')  # File upload is now required

    def __str__(self):
        return f"{self.subject.name} {self.year} {self.term}"

class Question(models.Model):
    exam_paper = models.ForeignKey(ExamPaper, on_delete=models.CASCADE, related_name='questions')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    frequency = models.PositiveIntegerField(default=1)  # For pattern analysis

    def __str__(self):
        return f"Q: {self.text[:50]}..."

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='notes/', blank=True, null=True)  # upload note files
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"