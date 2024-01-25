from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from app.models import UserProfile, Course
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake data for the app'

    def handle(self, *args, **kwargs):
        # Create a user
        user = User.objects.create_user(username=fake.user_name(), password=fake.password())
        full_name = fake.name()
        email = fake.email()
        age = fake.random_int(min=18, max=30)
        experience = fake.random_int(min=1, max=4)
        workplace = fake.company()
        bio = fake.text()

        # Try to get an existing user profile, create one if it doesn't exist
        user_profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'full_name': full_name,
                'email': email,
                'age': age,
                'experience': experience,
                'workplace': workplace,
                'bio': bio,
                'role': 'student'
            }
        )

        if not created:
            print(f"User with username {user.username} already exists: {user_profile}")
        else:
            print(f"Created user: {user_profile}")

        # Create teachers
        for _ in range(10):
            teacher_user = User.objects.create_user(username=fake.user_name(), password=fake.password())
            full_name = fake.name()
            email = fake.email()
            age = fake.random_int(min=22, max=65)
            experience = fake.random_int(min=1, max=20)
            workplace = fake.company()
            bio = fake.text()

            teacher_profile = UserProfile.objects.create(
                user=teacher_user,
                full_name=full_name,
                email=email,
                age=age,
                experience=experience,
                workplace=workplace,
                bio=bio,
                role='teacher'
            )
            print(f"Created teacher: {teacher_profile}")

        # Create students
        for _ in range(10):
            student_user = User.objects.create_user(username=fake.user_name(), password=fake.password())
            full_name = fake.name()
            email = fake.email()
            age = fake.random_int(min=18, max=30)
            experience = fake.random_int(min=1, max=4)
            workplace = fake.company()
            bio = fake.text()

            student_profile = UserProfile.objects.create(
                user=student_user,
                full_name=full_name,
                email=email,
                age=age,
                experience=experience,
                workplace=workplace,
                bio=bio,
                role='student'
            )
            print(f"Created student: {student_profile}")

        # Create courses
        for _ in range(6):
            course = Course.objects.create(
                title=fake.word(),
                description=fake.text(),
                start_date=fake.date_this_year(),
                summary=fake.text(),
                duration=random.randint(1, 10),
                image='https://via.placeholder.com/300',
            )
            print(f"Created course: {course}")

            # Add teachers
            teachers = UserProfile.objects.filter(role='teacher').exclude(id=user_profile.id).order_by('?')[
                       :random.randint(1, 3)]
            course.teachers.set(teachers)
            print(f"Added teachers to course: {teachers}")

            # Add students (excluding the one already created)
            students = UserProfile.objects.filter(role='student').exclude(id=user_profile.id).order_by('id')[
                       :random.randint(5, 15)]
            course.students.set(students)
            print(f"Added students to course: {students}")

        self.stdout.write(self.style.SUCCESS('Successfully generated fake data'))
