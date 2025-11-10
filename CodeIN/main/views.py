from django.shortcuts import render
from .models import Problem

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def problems(request):
    problem_list = Problem.objects.all()
    return render(request, 'main/problems.html', {'list':problem_list})

def create_problem(request):
    if request.method == "POST":
        client_ip = request.META.get('REMOTE_ADDR')
    return render(request, 'main/create_problem.html')