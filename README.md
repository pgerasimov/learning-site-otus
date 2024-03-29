# Learning Platform - "Цифровые навыки для успешной карьеры"

Этот проект представляет собой образовательную платформу, цель которой - предоставить студентам возможность развивать цифровые навыки для успешной карьеры. Проект создан с использованием Django, веб-фреймворка Python, и предоставляет следующие функциональности:

## Основные функции:

- **Курсы:** Разнообразные курсы по цифровым навыкам, предоставляемые опытными преподавателями.
- **Профили студентов и преподавателей:** Регистрация и создание профилей для студентов и преподавателей.
- **Расписание:** Интерактивное расписание для отслеживания занятий и событий.
- **Онлайн-учеба:** Возможность проведения вебинаров и онлайн-курсов.
- **Активность и обратная связь:** Возможность обсуждения курсов, участие в проектах и обратная связь от преподавателей.

## Установка и запуск проекта:

1. Клонируйте репозиторий: `git clone https://github.com/pgerasimov/learning-site-otus.git`
2. Создайте и активируйте виртуальное окружение: `python -m venv venv` и `source venv/bin/activate` (Linux/Mac) или `venv\Scripts\activate` (Windows).
3. Установите зависимости: `pip install -r requirements.txt`
4. Установите и запустите **Redis** в качестве службы
5. Создайте миграции и примените их: `python manage.py makemigrations` и `python manage.py migrate`
6. Сгенерируйте тестовые данные при необходимости `python manage.py generate_test_data`
7. Запустите сервер: `python manage.py runserver`
8. Перейдите по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/) в вашем веб-браузере.
9. Панель администрирования доступна по адресу [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

