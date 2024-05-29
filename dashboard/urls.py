from django.urls import path

from dashboard import views

urlpatterns = [
    path('', views.ihas_view, name='dashboard'),

    path('rentals/', views.rentals_view, name='rentals'),
    path('rentals/<int:id>/', views.rental_view, name='rental'),

    path('members/', views.members_view, name='members'),
    path('members/<int:id>', views.member_view, name='member'),

    path('categories/', views.iha_categories_view, name='categories'),
    path('categories/<int:id>', views.iha_category_view, name='category'),

    path('ihas/', views.ihas_view, name='ihas'),
    path('ihas/<str:category>', views.categorized_ihas_view, name='categorizied_ihas'),
    path('ihas/<int:id>', views.iha_view, name='iha'),
]
