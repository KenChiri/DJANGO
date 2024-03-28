from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'emergency'
urlpatterns = [
    path('home', views.report_emergency, name='home'),
    path('alerts', views.accident_alerts, name='alerts'), 
    path('abstract', views.abstract, name='abstratct'),
    path('chargesheet', views.charges, name='chargesheet'),
    path('medical', views.medical, name='medical')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
