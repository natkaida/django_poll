from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Question, Choice, Vote

def index(request):
    all_questions = Question.objects.order_by('-published')[:5]
    context = {'all_questions': all_questions}
    return render(request, 'index.html', context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Нет такого вопроса')
    return render(request, 'detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    labels = []
    data = []
    question = Question.objects.get(id=question_id)
    votes = question.choice_set.all()
    for item in votes:
        labels.append(item.name)
        data.append(item.votes)
    context = {'question': question, 'labels': labels, 'data': data}    
    return render(request, 'results.html', context)

@login_required()
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        user_choice = question.choice_set.get(pk=request.POST['choice'])
        if not question.user_voted(request.user):
            return render(request, 'detail.html',  {
            'question': question,
            'error_message': 'Вы уже голосовали в этом опросе. Выберите другой опрос.',
        })
        if user_choice:
            user_choice.votes += 1
            user_choice.save()
            vote = Vote(user=request.user, question=question, choice=user_choice)
            vote.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'detail.html', {
            'question': question,
            'error_message': 'Вы не выбрали вариант ответа!',
        })
    return render(request, 'results.html', {'question': question})