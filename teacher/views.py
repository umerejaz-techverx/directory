import csv
import zipfile
from io import BytesIO

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect

from .utils import insert_data
from .form import FileUploadForm
from .models import Teacher, Subject


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('upload')
        else:
            error_message = 'Invalid username or password'
    else:
        error_message = ''
    return render(request, 'login.html', {'error_message': error_message})


@login_required(login_url='/login/')
def upload_files(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            images = dict()
            file1 = form.cleaned_data['file1']
            file2 = form.cleaned_data['file2']
            zip_file = zipfile.ZipFile(file2)
            for filename in zip_file.namelist():
                if filename.endswith('.JPG'):
                    image_data = BytesIO(zip_file.read(filename))
                    image_file = InMemoryUploadedFile(image_data, None, filename, 'image/jpeg',
                                                      image_data.getbuffer().nbytes, None)
                    images[filename] = image_file
            reader = csv.DictReader(file1.read().decode('utf-8-sig').splitlines())
            list_of_records = []
            for i in reader:
                if i.get('Email Address'):
                    profile_picture = i.get('Profile picture')
                    if profile_picture:
                        i['Profile picture'] = images.get(profile_picture)
                    total = insert_data(i)
                    if total:
                        tmp_data = {
                            'email': i.get('Email Address'),
                            'total': total}
                        list_of_records.append(tmp_data)
            return render(request, 'upload_stats.html', context={'stats': list_of_records})

    else:
        form = FileUploadForm()

    return render(request, 'upload_files.html', {'form': form})


def records(request):
    if request.method == 'GET':
        records = Teacher.objects.all()
        context = {'records': records}
    return render(request, 'records.html', context)


def record_detail(request, pk):
    if request.method == 'GET':
        record = Teacher.objects.prefetch_related('subjects').get(id=pk)
        subjects = record.subjects.all().values_list('name', flat=True)
        context = {'record': record, 'subjects': subjects}
    return render(request, 'record_detail.html', context)


def search_view(request):
    query = request.GET.get('query')
    criteria = request.GET.get('criteria')
    records = []

    if query and criteria:
        if criteria == 'Last Name':
            records = Teacher.objects.filter(last_name__startswith=query[0])
        elif criteria == 'Subject':
            try:
                subjects = Subject.objects.filter(name__icontains=query)
                for s_query in subjects:
                    records.extend(s_query.teachers.all())
            except Subject.DoesNotExist:
                pass
    context = {
        'records': records,
        'query': query,
    }
    return render(request, 'search.html', context)


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
