from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_note, name='upload_note'),
    path('history/', views.history_page, name='history_page'),
]
