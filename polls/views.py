from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
# from django.views.generic import TemplateView
# from django.views.generic import RedirectView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Author
from .models import Publisher
from .models import Choice, Question
from .forms import AuthorForm, BookForm

from django.utils import timezone

# Create your views here.
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list':latest_question_list}
#     return render(request, 'polls/index.html', context)
#
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    # バグ pub_dateに将来日が格納された質問も表示してしまう。

    def get_queryset(self):
        """まだ公開されていない質問は除外する"""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def author(request):
    form = AuthorForm()
    return render(request, 'lect_030312/author.html', {'form': form}
    )

def book(request):
    form = BookForm()
    return render(request, 'lect_030312/book.html', {'form': form})

class PublisherList(ListView):
    model = Publisher

class PublisherDetail(DetailView):
    model = Publisher

class AuthorList(ListView):
    model = Author

# class AuthorDetail(DetailView):
#     model = Author

class AuthorCreate(CreateView):
    model = Author
    fields = ['name']

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['name']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors-list')


# class AboutView(TemplateView):
#     template_name = "about.html"
#
# class WikipediaView(RedirectView):
#     url = "https://ja.wikipedia.org/"