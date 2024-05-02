from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from kisanbasket import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('', include('Home.urls')),
    path('get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('api/register/', views.signup, name='register'),
    path('place/', include('Home.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
