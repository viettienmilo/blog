from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView,
)


from . import views

app_name = 'users'

urlpatterns = [
                path('register/', views.register, name='register'),
                path('login/', LoginView.as_view(), name='login'),
                path('logout/', LogoutView.as_view(), name='logout'),
                path('password-reset/', PasswordResetView.as_view(
                        success_url=reverse_lazy('users:password_reset_done')),
                     name='password_reset'),
                path('password-reset/done/', PasswordResetDoneView.as_view(),
                     name='password_reset_done'),
                path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
                        success_url=reverse_lazy('users:password_reset_complete')),
                     name='password_reset_confirm'),
                path('password-reset-complete/', PasswordResetCompleteView.as_view(),
                     name='password_reset_complete'),
                path('password-change/', PasswordChangeView.as_view(
                        success_url=reverse_lazy('users:password_change_done')),
                     name='password_change'),
                path('password-change/done/', PasswordChangeDoneView.as_view(),
                     name='password_change_done'),
                path('profile/', views.profile, name='profile'),
]