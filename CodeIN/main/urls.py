from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('problems/', views.problems, name='problems'),
    path('create_problem/', views.create_problem, name='create_problem'),
    path('problem/<int:problem_id>/', views.solve_problem, name='solve_problem'),
]