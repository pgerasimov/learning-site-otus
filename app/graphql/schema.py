import graphene
from app.models import Course, UserProfile


class UserType(graphene.ObjectType):
    id = graphene.Int()
    username = graphene.String()
    email = graphene.String()
    full_name = graphene.String()
    role = graphene.String()


class CourseType(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    start_date = graphene.String()
    summary = graphene.String()
    duration = graphene.Int()
    image = graphene.String()
    teachers = graphene.List(UserType)
    students = graphene.List(UserType)


class Query(graphene.ObjectType):
    all_courses = graphene.List(CourseType)
    all_students = graphene.List(UserType)
    all_teachers = graphene.List(UserType)

    def resolve_all_courses(self, info):
        return Course.objects.all()

    def resolve_all_teachers(self, info):
        return UserProfile.objects.filter(role='teacher')

    def resolve_all_students(self, info):
        return UserProfile.objects.filter(role='student')


schema = graphene.Schema(query=Query)
