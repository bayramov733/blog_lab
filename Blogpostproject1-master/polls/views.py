from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Question, Choice

# Index səhifəsi – son 5 sual
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


# Detail səhifəsi – bir sualın detayı
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """Only show questions published so far."""
        return Question.objects.filter(pub_date__lte=timezone.now())


# Results səhifəsi – səs nəticələri
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


# Vote funksiyası – birdən çox seçim
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    selected_choices = request.POST.getlist('choices')

    if not selected_choices:
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Zəhmət olmasa ən azı bir cavab seçin.",
        })

    for choice_id in selected_choices:
        selected_choice = question.choice_set.get(pk=choice_id)
        selected_choice.votes += 1
        selected_choice.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))