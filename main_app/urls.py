from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('about', views.about, name='about'),
    path('login', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Admin
    path('admin-places/', views.admin_places, name='admin_places'),
    path('admin-add-place/', views.add_place, name='add_place'),
    path('admin-edit-place/<int:pk>/', views.edit_place, name='edit_place'),
    path('admin-delete-place/<int:pk>/', views.delete_place, name='delete_place'),
    path('admin-users/', views.admin_users, name='admin_users'),

    # User
    path('places/', views.user_places, name='user_places'),

]