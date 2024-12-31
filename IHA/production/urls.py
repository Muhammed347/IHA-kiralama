from django.urls import path, include
from django.contrib.auth import views as auth_views
from production import views

urlpatterns = [
    path('', views.index, name='index'),
    path('listParts', views.list_parts, name='listParts'),
    path('produceParts', views.produce_parts, name='produceParts'),
    path('assembleAndViewDrones', views.assemble_and_view_drones, name='assemble_and_view_drones'),
    path('accounts/', include('django.contrib.auth.urls')),  # add auth urls(login, logout)
    path('accounts/register/', views.register, name='register'),
    path('addWingPart', views.add_wing_part, name='add_wing_part'),
    path('addBodyPart', views.add_body_part, name='add_body_part'),
    path('addTailPart', views.add_tail_part, name='add_tail_part'),
    path('addAvionicsPart', views.add_avionik_part, name='add_avionik_part'),
    path('deletePart/<int:part_id>/', views.delete_part, name='delete_part'), 
]