"""
URL configuration for PoolManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# Import các view mới
from quan_ly_ho_boi.views import trang_chu, dashboard, ban_do, quan_ly_danh_sach, xoa_ho_boi

urlpatterns = [ # type: ignore
    path('admin/', admin.site.urls),
    path('', trang_chu, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('map/', ban_do, name='map'),
    path('quan-ly/', quan_ly_danh_sach, name='quan_ly'),
    path('quan-ly/xoa/<int:ho_boi_id>/', xoa_ho_boi, name='xoa_ho_boi'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # type: ignore