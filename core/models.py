from django.db import models
from django.contrib.auth.models import User
from PyPDF2 import PdfReader
import re

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
    term = models.CharField(max_length=20, blank=True)
    file = models.FileField(upload_to='exam_papers/')
    extracted_text = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.file and self.file.name.endswith('.pdf'):
            try:
                pdf_path = self.file.path
                reader = PdfReader(pdf_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                self.extracted_text = text
                super().save(update_fields=['extracted_text'])

                # --- Split text into questions and create Question objects ---
                # Example: Split on "Q1.", "Q2.", ... (case-insensitive)
                questions = re.split(r'Q\d+\.', text, flags=re.IGNORECASE)
                # Remove any empty strings and leading/trailing whitespace
                questions = [q.strip() for q in questions if q.strip()]
                # Delete old questions for this paper to avoid duplicates
                self.questions.all().delete()
                for q_text in questions:
                    Question.objects.create(exam_paper=self, text=q_text)
            except Exception as e:
                self.extracted_text = f"Error extracting text: {e}"
                super().save(update_fields=['extracted_text'])

    def __str__(self):
        return f"{self.subject.name} {self.year} {self.term}"

class Question(models.Model):
    exam_paper = models.ForeignKey(ExamPaper, on_delete=models.CASCADE, related_name='questions')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    frequency = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        similar_questions = Question.objects.filter(
            text=self.text,
            topic=self.topic
        ).exclude(pk=self.pk)
        self.frequency = similar_questions.count() + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Q: {self.text[:50]}..."

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='notes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"