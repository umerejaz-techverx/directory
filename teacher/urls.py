from django.urls import re_path as url, path
from teacher import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url("upload/$", views.upload_files, name='upload'),
    url("records/$", views.records, name='records'),
    path("records/<int:pk>/", views.record_detail, name='record_detail'),
    path("search/", views.search_view, name='search'),
    path("login/", views.login_view, name='login'),
    path("", views.index, name='index'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout')

]
