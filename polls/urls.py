from django.urls import path

from . import views
# from .views import WikipediaView
# from .views import AboutView
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from .views import PublisherList
from .views import PublisherDetail
from django.views.generic import ListView, DetailView
from .views import AuthorCreate, AuthorDelete, AuthorUpdate
from .models import Author

app_name = 'polls'
urlpatterns = [
    path('authors/add/', AuthorCreate.as_view(), name='authors-add'),
    path('authors/<int:pk>/edit/', AuthorUpdate.as_view(), name='authors-update'),
    path('authors/<int:pk>/delete/', AuthorDelete.as_view(), name='authors-delete'),
    path('authors/',
         ListView.as_view(model=Author), name='authors-list'),
    path('authors/<int:pk>/',
         DetailView.as_view(model=Author), name='authors-detail'),
    path('',  views.IndexView.as_view(), name='index'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('author/', views.author),
    path('book/', views.book),
    path('about/', TemplateView.as_view(template_name="about.html")),
    path('wikipedia/', RedirectView.as_view(url="https://www.wikipedia.org")),
    path('publishers/', PublisherList.as_view()),
    path('publishers/<int:pk>/', PublisherDetail.as_view()),
    # path('about/', AboutView.as_view()),
    # path('wikipedia/', WikipediaView.as_view()),
]
