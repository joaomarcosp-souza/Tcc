# módulo do Django para criar urls
from django.urls import path, include
from .views import register, profile
from django.contrib.auth import views as auth_views



urlpatterns = [
    # URLS parte do Login
    path('registrar/', register, name="register"),
    path('logar/', auth_views.LoginView.as_view(template_name="users/registration/login.html"), name="login"),
    path('deslogado/', auth_views.LogoutView.as_view(template_name="users/registration/logout.html"), name="logout"),
    path('perfil/', profile, name="profile"),

    path('social-django/', include('social_django.urls', namespace='social')),

    # Password Reset com email
    path('recuperar-senha/', auth_views.PasswordResetView.as_view(template_name="users/resetSenha/password_reset_form.html",
                                                                  html_email_template_name='users/resetSenha/password_reset_email.html'), name='password_reset'),
    path('recuperar-senha/pronto', auth_views.PasswordResetDoneView.as_view(template_name="users/resetSenha/password_reset_done.html"), name='password_reset_done'),
    path('recuperar-senha/resetar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="users/resetSenha/password_reset_confirm.html"), name='password_reset_confirm'),
    path('recuperar-senha/resetar/pronto/', auth_views.PasswordResetCompleteView.as_view(template_name="users/resetSenha/password_reset_complete.html"), name='password_reset_complete'),

    
    # Urls parte da troca de senha já logado no sistema.
    path('alterar-senha/', auth_views.PasswordChangeView.as_view(template_name='users/change-password.html'), name="change"),
    path('alterar-senha/pronto/', auth_views.PasswordChangeDoneView.as_view(template_name='users/registration/password_change_done.html'), name='password_change_done'),
]
