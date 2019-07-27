from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('suppliers/', views.get_recipients, name='suppliers'),
    path('create-recipient/', views.create_recipient, name='create_recipient'),
    # path('github/client/', views.github_client, name='github_client'),
    # path('oxford/', views.oxford, name='oxford'),
]
