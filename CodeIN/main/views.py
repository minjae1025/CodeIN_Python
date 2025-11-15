import json
import os
import subprocess
import time

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

            with open(file_path, 'w', encoding='utf8') as f:
                f.write(code)
                f.write("\nsolution(2, [[1, 2], [2, 4]])")

            with open(file_path, 'r', encoding='utf8') as f:
                print(f.read())
            try:
                # 2. subprocess 실행
                # - `python3` 명령어로 파일을 실행합니다.
                # - `capture_output=True`로 표준 출력(stdout)과 에러(stderr)를 캡처합니다.
                # - `text=True`로 출력을 문자열로 처리합니다.
                # - `timeout`으로 최대 실행 시간을 제한합니다.

                start_time = time.time()

                result = subprocess.run(
                    ['python', file_path],
                    capture_output=True,
                    text=True,
                    timeout=timeout_seconds,
                    check=False  # 에러가 발생해도 예외를 발생시키지 않도록 설정
                )

                end_time = time.time()
                execution_time = end_time - start_time

                # 3. 결과값 추출
                stdout = result.stdout  # 표준 출력 (성공 시 결과)
                run_result.append(stdout)
                stderr = result.stderr  # 표준 에러 (런타임 에러 메시지)
                return_code = result.returncode  # 프로세스 종료 코드 (0이면 성공)

                if return_code != 0:
                    # 실행 에러 (Runtime Error) 발생
                    test_result = 'Runtime Error'
                    output_data = stderr
                else:
                    # 성공적으로 실행됨
                    test_result = 'Success'
                    output_data = stdout.strip()

                print(f"결과: {test_result}")
                print(f"출력: {output_data}")
                print(f"실행 시간: {execution_time:.3f} 초")

            except subprocess.TimeoutExpired:
                # 시간 초과 (Time Limit Exceeded)
                test_result = 'Time Limit Exceeded'
                print(f"결과: {test_result}")
            except Exception as e:
                # 기타 예외 처리 (파일 입출력 문제 등)
                test_result = f'Execution Failed: {e}'
                print(f"결과: {test_result}")
            finally:
                # 4. 임시 파일 삭제
                os.remove(file_path) # 실행 후에는 반드시 삭제해야 합니다.
                pass

            return JsonResponse({'success': True, 'message': 'Code received successfully'})
        except Exception as e:
            print(e)
            return JsonResponse({'error': f'Server processing error: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Only POST method'}, status=405)
