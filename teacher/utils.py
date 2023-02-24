from .models import Teacher, Subject
from django.db import IntegrityError


def insert_data(data):
    obj = None
    temp = {
        'first_name': data['First Name'].strip(),
        'last_name': data['Last Name'].strip(),
        'profile_picture': data['Profile picture'],
        'email': data['Email Address'],
        'phone_number': data['Phone Number'],
        'room_number': data['Room Number']
    }
    try:
        obj = Teacher.objects.get(
            **{'first_name': data['First Name'], 'last_name': data['Last Name'], 'email': data['Email Address']})
    except Teacher.DoesNotExist:
        try:
            obj = Teacher.objects.create(**temp)
        except IntegrityError as e:
            print(e)
    if obj:
        count = obj.subjects.all().count()
        subjects = data['Subjects taught'].split(',')
        for s_subject in subjects:
            if count < 5:
                s_obj, status = Subject.objects.get_or_create(**{'name': s_subject.strip()})
                obj.subjects.add(s_obj)
                if status:
                    count += 1
        return count
    else:
        return None
