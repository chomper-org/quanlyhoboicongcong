from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from quan_ly_ho_boi import views
from quan_ly_ho_boi.views import trang_chu, dashboard, ban_do, quan_ly_danh_sach, xoa_ho_boi, admin_home, login_admin, logout_admin, home_page, user_profile, login_user, logout_user, register_user, tao_ho_boi, chinh_sua_ho_boi

# --- CẤU HÌNH GIAO DIỆN ADMIN TẠI ĐÂY ---
from django.contrib import admin
admin.site.site_header = "HỆ THỐNG QUẢN LÝ "     # Tiêu đề lớn ở trên cùng
admin.site.site_title = "quản trị viên quản lý hồ bơi"           # Tiêu đề trên thẻ trình duyệt
admin.site.index_title = "Bảng điều khiển quản trị"    # Tiêu đề tại trang chủ admin
# ---------------------------------------

urlpatterns = [
    # path('admin/', admin.site.urls),  # Tắt admin Django
    path('', home_page, name='home'),
    path('profile/', user_profile, name='profile'),
    path('dashboard/', dashboard, name='dashboard'),
    path('map/', ban_do, name='map'),   
    path('quan-ly/', quan_ly_danh_sach, name='quan_ly'),
    path('quan-ly/xoa/<int:ho_boi_id>/', xoa_ho_boi, name='xoa_ho_boi'),
    path('admin-panel/ho-boi/them/', tao_ho_boi, name='tao_ho_boi'),
    path('admin-panel/ho-boi/<int:ho_boi_id>/sua/', chinh_sua_ho_boi, name='chinh_sua_ho_boi'),
    path('dat-ve/<int:ho_boi_id>/', views.dat_ve, name='dat_ve'),
    path('checkout/<int:datve_id>/', views.checkout, name='checkout'),
    path('lich-su-thanh-toan/', views.lich_su_thanh_toan, name='payment_history'),
    path('luu-ho-boi/', views.luu_ho_boi, name='luu_ho_boi'),
    path('api/get-pools/', views.get_pools, name='get_pools'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('register/', register_user, name='register_user'),
    path('admin-panel/login/', login_admin, name='login_admin'),
    path('admin-panel/logout/', logout_admin, name='logout_admin'),
    path('admin-panel/', admin_home, name='admin_panel'),
]

handler404 = 'quan_ly_ho_boi.views.page_not_found_view'

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