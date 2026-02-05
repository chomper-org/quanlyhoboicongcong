from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from quan_ly_ho_boi.views import trang_chu, dashboard, ban_do, quan_ly_danh_sach, xoa_ho_boi

# --- CẤU HÌNH GIAO DIỆN ADMIN TẠI ĐÂY ---
from django.contrib import admin
admin.site.site_header = "HỆ THỐNG QUẢN LÝ "     # Tiêu đề lớn ở trên cùng
admin.site.site_title = "quản trị viên quản lý hồ bơi"           # Tiêu đề trên thẻ trình duyệt
admin.site.index_title = "Bảng điều khiển quản trị"    # Tiêu đề tại trang chủ admin
# ---------------------------------------

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', trang_chu, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('map/', ban_do, name='map'),
    path('quan-ly/', quan_ly_danh_sach, name='quan_ly'),
    path('quan-ly/xoa/<int:ho_boi_id>/', xoa_ho_boi, name='xoa_ho_boi'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Tắt quảng cáo của thư viện và dùng menu icon
SIMPLEUI_HOME_INFO = False 
SIMPLEUI_ANALYSIS = False 

# Nếu muốn đổi icon cho các mục bên trái (ví dụ)
SIMPLEUI_ICON = {
    'Hồ bơi': 'fas fa-swimming-pool',
    'Vé đặt': 'fas fa-ticket-alt',
    'Người dùng': 'fas fa-user-shield',  # Nhìn sang hơn icon mặc định
    'Nhóm': 'fas fa-users-cog',
}