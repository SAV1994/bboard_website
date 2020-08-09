from django.urls import path

from .views import get_bbs, BbDetailView, get_comments

urlpatterns = [
    path('bbs/<int:pk>/comments', get_comments),
    path('bbs/<int:pk>/', BbDetailView.as_view()),
    path('bbs/', get_bbs),
]