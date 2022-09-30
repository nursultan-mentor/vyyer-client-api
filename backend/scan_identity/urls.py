from django.urls import path

from . import views

urlpatterns = [
    path('scan/get/', views.ScanListAPIView.as_view(), name='scan-list'),
    path('scan/get/<int:pk>/', views.ScanDetailAPIView.as_view(), name='scan-detail'),
    path('identity/get/', views.IdentityListAPIView.as_view(), name='identity-list'),
    path('identity/get/<int:pk>/', views.IdentityDetailAPIView.as_view(), name='identity-detail'),
    path('scan/range/', views.ScanListRangeAPIView.as_view(), name='scan-list-range'),
    path('identity/range/', views.IdentityListRangeAPIView.as_view(), name='identity-list-range'),

    path('generate_data/', views.generate_data, name='generate_data'),
]
