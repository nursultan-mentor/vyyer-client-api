from django.urls import path

from . import views

urlpatterns = [
    path('scan/get/', views.ScanListAPIView.as_view(), name='scan-list'),
    path('scan/getById/<int:pk>/', views.ScanDetailAPIView.as_view(), name='scan-detail'),
    path('identity/get/', views.IdentityListAPIView.as_view(), name='identity-list'),
    path('identity/getById/<int:pk>/', views.IdentityDetailAPIView.as_view(), name='identity-detail'),
]
