from django.urls import path
from . import views

urlpatterns = [
    path('club/<slug:club_slug>/', views.post_list, name='post_list'),
    path('club/<slug:club_slug>/create/', views.create_post, name='create_post'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
]
