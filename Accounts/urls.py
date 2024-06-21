from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('profile', views.profile, name= 'profile'),
    path('profile_image_update', views.profile_image_update, name='profile_image_update'),
    path('profile_bio_update', views.profile_bio_update, name='profile_bio_update'),
    path('create-post', views.create_post, name='create_post'),
    path('update_recommendation/<int:card_id>', views.update_recommendation, name='update_recommendation'),
    path('delete_post/<int:card_id>', views.delete_post, name='delete_post'),
    path('logout', views.custom_logout, name='logout'),
    path('password_reset_in/', views.CustomPasswordResetView.as_view(template_name='registration/password_reset_in.html'), name='password_reset_in'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_ok.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('delete-account/', views.delete_account, name='delete_account'),
]
