from django.contrib import admin
from .models import HoBoi, DatVe

@admin.register(HoBoi)
class HoBoiAdmin(admin.ModelAdmin):
    list_display = ('ten_ho', 'dia_chi', 'trang_thai', 'suc_chua')
    search_fields = ('ten_ho', 'dia_chi')

@admin.register(DatVe)
class DatVeAdmin(admin.ModelAdmin):
    list_display = ('khach_hang', 'ho_boi', 'ngay_su_dung', 'tong_tien')
    list_filter = ('ngay_su_dung', 'ho_boi')
