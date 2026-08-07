from django.urls import path
from . import views

urlpatterns = [
    path("", views.category_list, name="category_list"),
    path("manage/", views.service_type_manage, name="service_type_manage"),
    path("manage/add/", views.service_type_create, name="service_type_create"),
    path("manage/<int:pk>/edit/", views.service_type_update, name="service_type_update"),
    path("manage/<int:pk>/remove/", views.service_type_delete, name="service_type_delete"),
]
