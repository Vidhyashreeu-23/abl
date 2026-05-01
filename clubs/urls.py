from django.urls import path
from . import views

urlpatterns = [
    path('', views.club_list, name='club_list'),
    path('create/', views.create_club, name='create_club'),
    path('my-clubs/', views.my_clubs, name='my_clubs'),
    path('<slug:slug>/', views.club_detail, name='club_detail'),
    path('<slug:slug>/edit/', views.edit_club, name='edit_club'),
    path('<slug:slug>/delete/', views.delete_club, name='delete_club'),
    path('<slug:slug>/join/', views.join_club, name='join_club'),
    path('<slug:slug>/leave/', views.leave_club, name='leave_club'),
    path('<slug:slug>/members/', views.member_list, name='member_list'),
]
