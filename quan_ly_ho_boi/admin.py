from django.contrib import admin
from .models import HoBoi, DatVe

# Thêm # type: ignore vào cuối dòng class để tắt cảnh báo Pylance
@admin.register(HoBoi)
class HoBoiAdmin(admin.ModelAdmin): # type: ignore
    list_display = ('ten_ho', 'dia_chi', 'trang_thai', 'suc_chua')
    search_fields = ('ten_ho', 'dia_chi')
    list_filter = ('trang_thai',)

@admin.register(DatVe)
class DatVeAdmin(admin.ModelAdmin): # type: ignore
    list_display = ('khach_hang', 'ho_boi', 'ngay_su_dung', 'tong_tien')
    list_filter = ('ngay_su_dung', 'ho_boi')
    search_fields = ('khach_hang__username', 'ho_boi__ten_ho')