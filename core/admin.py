
from django.contrib import admin
from .models import Subject, Topic, ExamPaper, Question, Note

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    search_fields = ['name', 'subject__name']
    list_display = ['name', 'subject']
    list_filter = ['subject']

@admin.register(ExamPaper)
class ExamPaperAdmin(admin.ModelAdmin):
    search_fields = ['subject__name', 'year', 'term']
    list_display = ['subject', 'year', 'term', 'file']
    list_filter = ['subject', 'year', 'term']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['text', 'topic__name', 'exam_paper__subject__name']
    list_display = ['short_text', 'exam_paper', 'topic', 'frequency']
    list_filter = ['exam_paper__subject', 'topic']

    def short_text(self, obj):
        return obj.text[:50]
    short_text.short_description = 'Question'

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    search_fields = ['title', 'user__username', 'subject__name', 'topic__name']
    list_display = ['title', 'user', 'subject', 'topic', 'created_at']
    list_filter = ['subject', 'topic', 'user', 'created_at']