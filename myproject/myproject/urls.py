# myproject/urls.py


from django.urls import path
from . import views

urlpatterns = [
    path('create_person/', views.create_person, name='create_person'),
    path('create_cours/', views.create_cours, name='create_cours'),
    path('create_relation/', views.create_relation, name='create_relation'),
    path('', views.list_person, name='list_person'),
    path('update/<person_id>/', views.update_person, name='update_person'),
    path('delete/<str:person_id>/', views.delete_person, name='delete_person'),]
