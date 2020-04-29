from django.urls import path
from search_queries.views import QuestionFilter


urlpatterns = [
    path('questions_filter/', QuestionFilter.as_view()),
]
