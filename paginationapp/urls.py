from django.urls import path
from . import views

urlpatterns = [
    path('contacts/', views.ContactView.as_view(), name="contacts")
]