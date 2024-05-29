from django.urls import path
from . import views

urlpatterns = [
    path('', views.ihas_view, name='dashboard'),
    path('rentals/', views.rentals_view, name='rentals'),
    path('rentals/<int:id>/', views.rental_view, name='rental'),
    path('members/', views.members_view, name='members'),
    path('members/<int:id>', views.member_view, name='member'),
    path('categories/', views.iha_categories_view, name='categories'),
    path('ihas/', views.ihas_view, name='ihas'),
    path('ihas/<int:id>', views.iha_view, name='iha'),
]
