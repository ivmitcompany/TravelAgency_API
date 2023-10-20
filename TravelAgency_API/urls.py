"""
URL configuration for TravelAgency_API project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from django.conf import settings
from travel_api import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/tours', views.ToursList.as_view()),
    path('api/v1/tours/', views.TourSearch.as_view()),
    path('api/v1/tours/featured', views.FeaturedTours.as_view()),
    path('api/v1/tours/<int:id>/', views.DetailsTour.as_view()),
    path(r'pay', views.PayView.as_view(), name='pay_view'),
    path(r'pay-callback', views.PayCallbackView.as_view(), name='pay_callback'),
    path('api/v1/tours/<int:tour_id>/order/payment', views.OrderPaymentView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)