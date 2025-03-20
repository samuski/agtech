from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('success/<int:upload_id>/', views.upload_success, name='upload_success'),
]
