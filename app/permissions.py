from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Course, UserProfile

# Разрешение для записи на курс
write_course_permission = Permission.objects.create(
    codename='write_course',
    name='Can write on course',
    content_type=ContentType.objects.get_for_model(Course),
)

# Разрешение для редактирования и удаления курса
edit_delete_course_permission = Permission.objects.create(
    codename='edit_delete_course',
    name='Can edit or delete course',
    content_type=ContentType.objects.get_for_model(Course),
)

# Разрешение для создания курса
create_course_permission = Permission.objects.create(
    codename='create_course',
    name='Can create course',
    content_type=ContentType.objects.get_for_model(Course),
)

# Разрешение для записи на курс учеником
write_course_student_permission = Permission.objects.create(
    codename='write_course_student',
    name='Can write on course as student',
    content_type=ContentType.objects.get_for_model(UserProfile),
)

# Разрешение для редактирования и удаления курса учителем
edit_delete_course_teacher_permission = Permission.objects.create(
    codename='edit_delete_course_teacher',
    name='Can edit or delete course as teacher',
    content_type=ContentType.objects.get_for_model(UserProfile),
)

# Разрешение для создания курса учителем
create_course_teacher_permission = Permission.objects.create(
    codename='create_course_teacher',
    name='Can create course as teacher',
    content_type=ContentType.objects.get_for_model(UserProfile),
)
