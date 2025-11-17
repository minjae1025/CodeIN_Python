import json, ast, os, subprocess, time
import traceback

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
            if request.user.is_authenticated:
                user = request.user  # 원하는 User 객체
            else:
                return JsonResponse({'error': 'Only authenticated users'}, status=403)
            if request.META['CONTENT_TYPE'] == "application/json":
                # print(request.META)
                data = json.loads(request.body)
                print(data)
                try:
                    for case in data['example']['cases']:
                        for item in case['inputs']:
                            print(item)
                            temp = ast.literal_eval(item)
                except Exception as e:
                    print("User Input에 문법 오류")
                    print(e)
                    return JsonResponse({'success': False}, status=400)

                data['ip'] = request.META['REMOTE_ADDR']
                data['create_user'] = user
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
        # print(request.META)
        run_result = []
        try:
            data = json.loads(request.body)
            code, file_path, cases = py_run_setting(data)
            for case in cases:
                str_input, str_output = py_write_code(case, file_path, code)
                total_result = {}
                try:
                    start_time = time.perf_counter()
                    result = py_code_run(file_path)
                    execution_time = time.perf_counter() - start_time

                    stdout = result.stdout  # 표준 출력
                    stderr = result.stderr  # 표준 에러
                    return_code = result.returncode  # 프로세스 종료 코드

                    if return_code == 0:
                        test_result = 0
                        output_data = stdout.strip()
                    else:
                        test_result = -1
                        # output_data = stderr
                        output_data = "runtime error"

                    total_result = {'output': output_data, 'result_code': test_result, 'time': f'{execution_time:.3f}',
                                    'answer_value': str_output, 'input': str_input}
                except subprocess.TimeoutExpired:
                    total_result = {'test_result': 1}
                except Exception as e:
                    test_result = f'Execution Failed: {e}'
                    print(f"결과: {test_result}")
                finally:
                    run_result.append(total_result)
                    os.remove(file_path)  # 실행 후 삭제
                    pass
            return JsonResponse({'success': True, 'result': run_result})
        except Exception as e:
            print(e)
            return JsonResponse({'error': f'Server processing error: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Only POST method'}, status=405)


def submit_code(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user  # 원하는 User 객체
        else:
            return JsonResponse({'error': 'Only authenticated users'}, status=403)

        run_result = []
        try:
            data = json.loads(request.body)
            code, file_path, cases = py_run_setting(data)
            for case in cases:
                str_input, str_output = py_write_code(case, file_path, code)
                total_result = {}
                try:
                    start_time = time.perf_counter()
                    result = py_code_run(file_path)
                    execution_time = time.perf_counter() - start_time

                    stdout = result.stdout  # 표준 출력
                    stderr = result.stderr  # 표준 에러
                    return_code = result.returncode  # 프로세스 종료 코드
                    answer = False

                    if return_code == 0:
                        test_result = 0
                        output_data = stdout.strip().split('\n')
                        if output_data[-1] == str_output:
                            answer = True
                    else:
                        test_result = -1
                        # output_data = stderr
                        output_data = "runtime error"

                    total_result = {'output': output_data, 'result_code': test_result, 'time': f'{execution_time:.3f}',
                                    'answer_value': str_output, 'input': str_input, 'answer': answer}
                except subprocess.TimeoutExpired:
                    total_result = {'test_result': 1}
                except Exception as e:
                    test_result = f'Execution Failed: {e}'
                    print(f"결과: {test_result}")
                finally:
                    run_result.append(total_result)
                    os.remove(file_path)  # 실행 후 삭제
                    pass

            # print(run_result)

            all_answer = False
            for item in run_result:
                if item['answer']:
                    all_answer = True
                else:
                    all_answer = False
                    break

            duplicate_check = False
            if all_answer:
                problem = Problem.objects.get(id=data['id'])
                for solved in user.solved_problem:
                    if solved == data['id']:
                        duplicate_check = True
                        return JsonResponse({'success': True, 'result': run_result, 'history': False, 'pass': True})

                if not duplicate_check:
                    problem.answer_count += 1
                    problem.save()
                    user.question_count += 1
                    user.solved_problem.append(data['id'])
                    user.save()
                    return JsonResponse({'success': True, 'result': run_result, 'history': True, 'pass': True})

            return JsonResponse({'success': True, 'result': run_result, 'history': False, 'pass': False})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': f'Server processing error: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Only POST method'}, status=405)


def py_code_run(file_path):
    return subprocess.run(
        ['python', file_path],
        capture_output=True,
        text=True,
        timeout=10,
        check=False  # 에러가 발생해도 예외를 발생시키지 않도록 설정
    )


def py_write_code(case, file_path, code):
    str_input = case.get('inputs')
    str_output = case.get('output')
    py_input = []
    for item in str_input:
        py_input.append(ast.literal_eval(item))

    with open(file_path, 'w', encoding='utf8') as f:
        f.write(code)
        f.write(f"\nprint(solution({str(py_input)[1:-1]}))")

    return str_input, str_output


def py_run_setting(data):
    code = data.get('code')

    temp_file_name = str(time.strftime("%Y%m%d_%H%M%S", time.localtime())) + '.py'
    file_path = os.path.join("temp_code", temp_file_name)

    TEMP_DIR = os.path.join(os.getcwd(), "temp_code")  # 프로젝트 루트 기준으로 경로 설정
    os.makedirs(TEMP_DIR, exist_ok=True)  # 디렉터리가 없으면 생성합니다.

    problem = Problem.objects.get(id=data['id'])
    example = problem.example
    cases = (dict(example).get('cases'))

    return code, file_path, cases
