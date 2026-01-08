from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]
