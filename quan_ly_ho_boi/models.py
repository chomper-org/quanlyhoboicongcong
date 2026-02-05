from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal # <--- 1. Import thêm cái này
from typing import Any      # <--- 2. Import thêm cái này

# Model Hồ Bơi
class HoBoi(models.Model):
    TRANG_THAI_CHOICES = [
        ('MO', 'Đang mở'),
        ('BAO_TRI', 'Bảo trì'),
        ('DONG', 'Đóng cửa'),
    ]
    
    ten_ho = models.CharField(max_length=200, verbose_name="Tên hồ bơi")
    dia_chi = models.TextField(verbose_name="Địa chỉ")
    do_sau = models.FloatField(help_text="Độ sâu tính bằng mét", verbose_name="Độ sâu (m)")
    suc_chua = models.IntegerField(verbose_name="Sức chứa tối đa")
    vi_do = models.FloatField(verbose_name="Vĩ độ")
    kinh_do = models.FloatField(verbose_name="Kinh độ")
    
    # 3. Sửa lỗi Decimal: Bọc số tiền trong Decimal()
    gia_ve_nguoi_lon = models.DecimalField(max_digits=10, decimal_places=0, default=Decimal('50000'), verbose_name="Giá vé người lớn")
    gia_ve_tre_em = models.DecimalField(max_digits=10, decimal_places=0, default=Decimal('30000'), verbose_name="Giá vé trẻ em")
    
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='MO', verbose_name="Trạng thái")
    hinh_anh = models.ImageField(upload_to='ho_boi/', blank=True, null=True, verbose_name="Hình ảnh")

    class Meta:
        verbose_name = "Hồ bơi"
        verbose_name_plural = "Danh sách Hồ bơi"

    def __str__(self):
        return str(self.ten_ho) # Ép kiểu string cho chắc chắn

# Model Vé/Đặt chỗ
class DatVe(models.Model):
    khach_hang = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Khách hàng")
    ho_boi = models.ForeignKey(HoBoi, on_delete=models.CASCADE, verbose_name="Hồ bơi")
    ngay_dat = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đặt")
    ngay_su_dung = models.DateField(verbose_name="Ngày bơi")
    so_luong_nguoi_lon = models.IntegerField(default=1, verbose_name="Số người lớn")
    so_luong_tre_em = models.IntegerField(default=0, verbose_name="Số trẻ em")
    tong_tien = models.DecimalField(max_digits=12, decimal_places=0, editable=False, verbose_name="Tổng tiền")

    # 4. Sửa lỗi args/kwargs: Khai báo kiểu :Any
    def save(self, *args: Any, **kwargs: Any):
        # Tính toán dùng Decimal để tránh lỗi
        gia_nl = self.ho_boi.gia_ve_nguoi_lon
        gia_te = self.ho_boi.gia_ve_tre_em
        
        self.tong_tien = (Decimal(self.so_luong_nguoi_lon) * gia_nl) + \
                         (Decimal(self.so_luong_tre_em) * gia_te)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Vé đặt"
        verbose_name_plural = "Danh sách Vé đặt"

    def __str__(self):
        return f"{self.khach_hang.username} - {self.ho_boi.ten_ho} ({self.ngay_su_dung})"