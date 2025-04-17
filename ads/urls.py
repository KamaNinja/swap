from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('my_ads/', views.my_ads, name='my_ads'),
    path('ad_details/<int:ad_pk>/', views.ad_details, name='ad_details'),
    path('add_ad/', views.add_ad, name='add_ad'),
    path('update_ad/<int:ad_pk>/', views.update_ad, name='update_ad'),
    path('delete_ad/<int:ad_pk>/', views.delete_ad, name='delete_ad'),

    path('exchange/<int:ad_pk>/', views.suggest_exchange, name='suggest_exchange'),
    path('my_proposals/', views.my_proposals, name='my_proposals'),
    path('proposal_details/<int:proposal_pk>/', views.proposal_details, name='proposal_details'),
    path('exchange_action/<int:proposal_pk>/', views.exchange_action, name='exchange_action'),
]
