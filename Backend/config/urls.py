from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # "api/v1/ 으로 시작하는 주소는 api 폴더 안에 있는 urls.py"
    path('api/v1/', include('api.urls')), 
]