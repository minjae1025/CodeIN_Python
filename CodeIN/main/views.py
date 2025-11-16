import json, ast, os, subprocess, time

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Problem


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def problems(request):
    problem_list = Problem.objects.all()
    return render(request, 'main/problems.html', {'list': problem_list})


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


def solve_problem(request, problem_id):
    problem = Problem.objects.get(pk=problem_id)
    return render(request, 'main/solve_problem.html', {'problem': problem})


def run_code(request):
    if request.method == "POST":
        run_result = []
        try:
            data = json.loads(request.body)
            code = data.get('code')

            temp_file_name = str(time.strftime("%Y%m%d_%H%M%S", time.localtime())) + '.py'
            file_path = os.path.join("temp_code", temp_file_name)
            timeout_seconds = 10

            TEMP_DIR = os.path.join(os.getcwd(), "temp_code")  # 프로젝트 루트 기준으로 경로 설정
            os.makedirs(TEMP_DIR, exist_ok=True)  # 디렉터리가 없으면 생성합니다.

            problem = Problem.objects.filter(id=data['id'])
            example = problem[0].example
            cases = (dict(example).get('cases'))

            for case in cases:
                str_input = case.get('inputs')
                str_output = case.get('output')
                py_input = []
                for item in str_input:
                    py_input.append(ast.literal_eval(item))

                print(input)
                with open(file_path, 'w', encoding='utf8') as f:
                    f.write(code)
                    f.write(f"\nprint(solution({str(py_input)[1:-1]}))")

                # with open(file_path, 'r', encoding='utf8') as f:
                #     print(f.read())

                total_result = {}
                try:
                    start_time = time.perf_counter()

                    result = subprocess.run(
                        ['python', file_path],
                        capture_output=True,
                        text=True,
                        timeout=timeout_seconds,
                        check=False  # 에러가 발생해도 예외를 발생시키지 않도록 설정
                    )

                    execution_time = time.perf_counter() - start_time

                    stdout = result.stdout  # 표준 출력
                    stderr = result.stderr  # 표준 에러
                    return_code = result.returncode  # 프로세스 종료 코드

                    if return_code != 0: #런타임 에러시
                        test_result = -1
                        # output_data = stderr
                        output_data = "runtime error"
                    else:
                        test_result = 0
                        output_data = stdout.strip()

                    total_result = {'output': output_data, 'result_code': test_result, 'time': f'{execution_time:.3f}', 'answer': str_output, 'input': str_input}
                except subprocess.TimeoutExpired:
                    total_result = {'test_result': 1}
                except Exception as e:
                    test_result = f'Execution Failed: {e}'
                    print(f"결과: {test_result}")
                finally:
                    run_result.append([total_result])
                    os.remove(file_path) # 실행 후 삭제
                    pass
            print(run_result)
            return JsonResponse({'success': True, 'result': run_result})
        except Exception as e:
            print(e)
            return JsonResponse({'error': f'Server processing error: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Only POST method'}, status=405)
