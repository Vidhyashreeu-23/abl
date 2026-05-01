from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('<int:pk>/edit/', views.edit_event, name='edit_event'),
    path('<int:pk>/delete/', views.delete_event, name='delete_event'),
    path('<int:pk>/register/', views.register_event, name='register_event'),
    path('my-events/', views.my_events, name='my_events'),
    path('club/<slug:club_slug>/create/', views.create_event, name='create_event'),
]
