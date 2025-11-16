DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'codein',
        'USER' : 'py_project',
        'PASSWORD' : '1111', # 설정한 비밀번호로 적어주면 된다.
        'HOST' : '127.0.0.1',
        'PORT' : '3306',
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6_7ti@tcvm9gm8i(0g1mcz#-$t3m(*qc($up5r296vg^2f!s*9'
