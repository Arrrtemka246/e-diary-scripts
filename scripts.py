import random

from datacenter.models import (
    Chastisement,
    Commendation,
    Lesson,
    Mark,
    Schoolkid,
)


COMMENDATIONS = [
    'Хвалю!',
    'Молодец!',
    'Отлично!',
    'Так держать!',
    'Прекрасная работа!',
    'Очень хороший ответ!',
    'Ты на верном пути!',
    'Замечательно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
]


def get_schoolkid(schoolkid_name):
    """Найти одного ученика по части ФИО."""
    if not schoolkid_name.strip():
        print('Имя ученика не указано.')
        return None

    try:
        return Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except Schoolkid.DoesNotExist:
        print(f'Ученик "{schoolkid_name}" не найден.')
    except Schoolkid.MultipleObjectsReturned:
        print(
            f'По запросу "{schoolkid_name}" найдено несколько учеников. '
            'Уточните имя.'
        )

    return None


def fix_marks(schoolkid):
    """Исправить двойки и тройки ученика на пятёрки."""
    return Mark.objects.filter(
        schoolkid=schoolkid,
        points__in=[2, 3],
    ).update(points=5)


def remove_chastisements(schoolkid):
    """Удалить все замечания выбранного ученика."""
    return Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid_name, subject_title):
    """Добавить случайную похвалу за последний урок по предмету."""
    schoolkid = get_schoolkid(schoolkid_name)
    if schoolkid is None:
        return None

    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject_title,
    ).order_by('-date').first()

    if lesson is None:
        print(
            f'Уроки по предмету "{subject_title}" '
            f'для {schoolkid.full_name} не найдены.'
        )
        return None

    return Commendation.objects.create(
        text=random.choice(COMMENDATIONS),
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher,
    )
