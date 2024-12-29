from django.urls import path, include
from django.contrib.auth import views as auth_views
from production import views

urlpatterns = [
    path('', views.index, name='index'),
    path('listParts', views.list_parts, name='listParts'),
    path('produceParts', views.create_parts, name='produceParts'),
    path('assembleAndViewDrones', views.assemble_and_view_drones, name='assemble_and_view_drones'),
    path('accounts/', include('django.contrib.auth.urls')),  # add auth urls(login, logout)
    path('accounts/register/', views.register, name='register'), 
]