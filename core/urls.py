from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('suppliers/', views.get_recipients, name='suppliers'),
    path('create-recipient/', views.create_recipient, name='create_recipient'),
    path('create-transfer/<int:id>/', views.create_transfer_by_id,
         name='create_transfer_by_id'),
    path('update-recipient/<int:id>/', views.update_recipient,
         name='update_recipient'),
    path('delete-recipient/<int:id>/', views.delete_recipient,
         name='delete_recipient'),
    path('create-transfer/', views.create_transfer,
         name='create_transfer'),
]
