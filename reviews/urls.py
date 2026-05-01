from django.urls import path
from . import views

urlpatterns = [
    path('<slug:club_slug>/add/', views.add_review, name='add_review'),
    path('<int:pk>/edit/', views.edit_review, name='edit_review'),
    path('<int:pk>/delete/', views.delete_review, name='delete_review'),
]
