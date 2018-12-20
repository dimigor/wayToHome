from django.urls import path, re_path

from custom_user.views import signup, registration_confirm

urlpatterns = [
    path('register', signup, name='signup'),
    re_path(r'^activate/(?P<token>.+)$', registration_confirm, name='confirm_signup'),
]
