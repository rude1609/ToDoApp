from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.customerLoginView.as_view(), name='login'),
    path('register/', views.RegistrationForm.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.TodoView.as_view(), name='tasks'),
    path('task/<int:pk>/', views.TodoDetail.as_view(), name='detail'),
    path('create/', views.TodoCreate.as_view(), name='create'),
    path('update/<int:pk>/', views.TodoUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', views.DeleteView.as_view(), name='delete')
]
