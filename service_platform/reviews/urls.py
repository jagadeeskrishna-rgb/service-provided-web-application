from django.urls import path
from . import views

urlpatterns = [path("booking/<int:booking_id>/", views.review_create, name="review_create")]
