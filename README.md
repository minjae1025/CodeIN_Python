# CodeIN_Python
### 2025학년도 2학기 파이썬 프로젝트입니다

## 라이브러리
1. Django
2. mysqlclient

## 실행 방법
1. ```cd CodeIN```
2. ```python manage.py runserver```
3. 웹 브라우저로 ```localhost:8000``` 접속

## 데이터베이스 세팅(MySQL 기준)
1. mysql에서 codein 이라는 database를 만든다.
2. CodeIN안에 mysettings.py를 만든 후 다음 문구를 추가한다.
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'codein',
        'USER' : 데이터베이스 유저 이름,
        'PASSWORD' : 데이터베이스 비밀번호,
        'HOST' : '127.0.0.1',
        'PORT' : '3306',
    }
}
```
3. ```cd CodeIN```, ```python manage.py migrate``` 입력 후 실행!
4. 단, 초기상태로 시작함

## 관리자 계정 생성법
1. ```cd Code```
2. ```python manage.py createsuperuser``` 입력 후 이름과 이메일, 비밀번호 입력
