from django.urls import path

from admin.views import AdminListView

app_name = 'admins'

urlpatterns = [
    path('users/', AdminListView.as_view(), name='users'),
    path('users/<int:pk>/', AdminListView.as_view(), name='about-user'),


]
