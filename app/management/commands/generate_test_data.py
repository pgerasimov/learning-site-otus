import random
from faker import Faker
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from app.models import Teacher, Student, Course

fake = Faker()


class Command(BaseCommand):
    help = 'Generate fake data for the app'

    def handle(self, *args, **kwargs):
        # Создаем учителей
        for _ in range(10):
            user = User.objects.create_user(username=fake.user_name(), password=fake.password())
            Teacher.objects.create(user=user, bio=fake.text())

        # Создаем студентов
        for _ in range(20):
            user = User.objects.create_user(username=fake.user_name(), password=fake.password())
            Student.objects.create(user=user, bio=fake.text())

        # Создаем курсы
        for _ in range(6):
            course = Course.objects.create(
                title=fake.word(),
                description=fake.text(),
                start_date=fake.date_this_year(),
                summary=fake.text(),
                duration=random.randint(1, 10),
                image='https://via.placeholder.com/300',
            )

            # Добавляем учителей
            teachers = Teacher.objects.order_by('?')[:random.randint(1, 3)]
            course.teachers.set(teachers)

            # Добавляем студентов
            students = Student.objects.order_by('?')[:random.randint(5, 15)]
            course.students.set(students)

        self.stdout.write(self.style.SUCCESS('Successfully generated fake data'))
