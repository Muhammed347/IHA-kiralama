from django.urls import path
from production import views

urlpatterns = [
    path('', views.index, name='index'),
    path('listParts', views.list_parts, name='listParts'),
    path('produceParts', views.create_parts, name='produceParts'),
    path('assembleAndViewDrones', views.assemble_and_view_drones, name='assemble_and_view_drones'),
]