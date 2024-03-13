from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.Login.as_view(), name='login'), # Login 
    path('register/', views.Register.as_view(), name='register'), # Register
    path('logout/', views.Logout.as_view(), name='logout'), # Register
    
    path('', views.UserList.as_view(), name='users_list'), # User List
    path('<int:pk>/', views.UserDetail.as_view(), name='users_detail'), # User Detail
]

