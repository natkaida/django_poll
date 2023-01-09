from django.contrib import admin
from .models import Question, Choice, Vote

admin.site.site_header = 'Панель управления'
admin.site.site_title = 'Голосования и опросы'
admin.site.index_title = 'Управление опросами и голосованиями'

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['name']}),]
    inlines = [ChoiceInLine]

admin.site.register(Question, QuestionAdmin)
