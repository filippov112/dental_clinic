# Инструкция

1. Ставим `wkhtmltox`, `PostgreSQL`, `dBeaver`(желательно).
    - Сверяемся:
        - Путь установки `wk...`: *C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe*
        - БД:
            ```
                'NAME': 'dental_clinic_db',
                'USER': 'postgres',
                'PASSWORD': '12345678',
                'HOST': 'localhost',
                'PORT': '5432',
            ```
        - Данные почты:
            EMAIL_HOST_USER = 'gryzunovegor39@gmail.com'
            EMAIL_HOST_PASSWORD = 'avatar2012'

2. Перезагружаемся.
3. Открываем проект и создаем виртуальное окружение.
4. Ставим всё что указано в `requirements.txt`.
5. Создаем миграции, применяем их, создаем суперюзера в терминале из каталога `dental_clinic/`:
    ```
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    ```
6. Создаем конфигурацию запуска или запускаемся вручную с терминала: `python manage.py runserver`.