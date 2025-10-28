from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('my-token/<int:token_id>/', views.my_token, name='my_token'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Manage sections
    path('admin-dashboard/services/', views.manage_services, name='manage_services'),
    path('admin-dashboard/organizations/', views.manage_organizations, name='manage_organizations'),

    path('update-status/<int:token_id>/<str:status>/', views.update_status, name='update_status'),
    path('display/', views.display_screen, name='display_screen'),

    # Login/Logout/Register with custom views
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register, name='register'),
    path("delete-token/<int:token_id>/", views.delete_token, name="delete_token"),
]
