import json

from django.http import HttpResponse, JsonResponse
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
        try:
            if request.META['CONTENT_TYPE'] == "application/json":
                # print(request.META)
                data = json.loads(request.body)
                data['ip'] = request.META['REMOTE_ADDR']
                Problem.objects.create(**data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
        return JsonResponse({'success': True})
    return render(request, 'main/create_problem.html')