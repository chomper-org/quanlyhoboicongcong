from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from typing import Any
from datetime import time

# 1. Model Hồ Bơi (Chính - Đã xóa phần trùng lặp ở dưới)
class HoBoi(models.Model):
    TRANG_THAI_CHOICES = [
        ('MO', 'Đang mở'),
        ('BAO_TRI', 'Bảo trì'),
        ('DONG', 'Đóng cửa'),
    ]
    

    gio_mo_cua = models.TimeField(default=time(6, 0), verbose_name="Giờ mở cửa")
    gio_dong_cua = models.TimeField(default=time(20, 0), verbose_name="Giờ đóng cửa")

    ten_ho = models.CharField(max_length=200, verbose_name="Tên hồ bơi")
    dia_chi = models.TextField(verbose_name="Địa chỉ")
    do_sau = models.FloatField(help_text="Độ sâu tính bằng mét", verbose_name="Độ sâu (m)")
    suc_chua = models.IntegerField(verbose_name="Sức chứa tối đa")
    vi_do = models.FloatField(verbose_name="Vĩ độ")
    kinh_do = models.FloatField(verbose_name="Kinh độ")
    
    gia_ve_nguoi_lon = models.DecimalField(max_digits=10, decimal_places=0, default=Decimal('50000'), verbose_name="Giá vé người lớn")
    gia_ve_tre_em = models.DecimalField(max_digits=10, decimal_places=0, default=Decimal('30000'), verbose_name="Giá vé trẻ em")
    
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='MO', verbose_name="Trạng thái")
    hinh_anh = models.ImageField(upload_to='ho_boi/', blank=True, null=True, verbose_name="Hình ảnh")

    class Meta:
        verbose_name = "Hồ bơi"
        verbose_name_plural = "Danh sách Hồ bơi"

    def __str__(self):
        return str(self.ten_ho)

class HinhAnhHoBoi(models.Model):
    ho_boi = models.ForeignKey(HoBoi, on_delete=models.CASCADE, related_name='danh_sach_hinh_anh', verbose_name="Hồ bơi")
    hinh_anh = models.ImageField(upload_to='ho_boi_gallery/', verbose_name="Hình ảnh")

    class Meta:
        verbose_name = "Hình ảnh hồ bơi"
        verbose_name_plural = "Bộ sưu tập ảnh hồ bơi"

    def __str__(self):
        return f"Ảnh của {self.ho_boi.ten_ho}"

# 2. Model Vé/Đặt chỗ
class DatVe(models.Model):
    khach_hang = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Khách hàng")
    ho_boi = models.ForeignKey(HoBoi, on_delete=models.CASCADE, verbose_name="Hồ bơi")
    ngay_dat = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đặt")
    ngay_su_dung = models.DateField(verbose_name="Ngày bơi")
    so_luong_nguoi_lon = models.IntegerField(default=1, verbose_name="Số người lớn")
    so_luong_tre_em = models.IntegerField(default=0, verbose_name="Số trẻ em")
    tong_tien = models.DecimalField(max_digits=12, decimal_places=0, editable=False, verbose_name="Tổng tiền")
    gio_su_dung = models.TimeField(default=time(8, 0), verbose_name="Giờ bơi")

    def save(self, *args: Any, **kwargs: Any):
        gia_nl = self.ho_boi.gia_ve_nguoi_lon
        gia_te = self.ho_boi.gia_ve_tre_em
        
        self.tong_tien = (Decimal(self.so_luong_nguoi_lon) * gia_nl) + \
                         (Decimal(self.so_luong_tre_em) * gia_te)
        super().save(*args, **kwargs)

    @property
    def tong_tien_dich_vu(self):
        return sum((item.so_luong * item.don_gia_thuc_te for item in self.chitietdichvu_set.all()), Decimal('0'))

    @property
    def tong_thanh_toan_cuoi(self):
        tong_ve = self.tong_tien if self.tong_tien else Decimal('0')
        return tong_ve + self.tong_tien_dich_vu

    class Meta:
        verbose_name = "Vé đặt"
        verbose_name_plural = "Danh sách Vé đặt"

    def __str__(self):
        return f"{self.khach_hang.username} - {self.ho_boi.ten_ho} ({self.ngay_su_dung})"

# 3. Model Thanh toán lịch sử
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Tiền mặt', 'Tiền mặt'),
        ('Thẻ ngân hàng', 'Thẻ ngân hàng'),
        ('Thanh toán di động', 'Thanh toán di động'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('Hoàn thành', 'Hoàn thành'),
        ('Đang chờ', 'Đang chờ'),
        ('Hủy', 'Hủy'),
    ]

    dat_ve = models.OneToOneField(DatVe, on_delete=models.CASCADE, verbose_name="Vé đặt")
    phuong_thuc = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='Tiền mặt', verbose_name='Phương thức')
    so_tien = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='Số tiền')
    ngay_thanh_toan = models.DateTimeField(auto_now_add=True, verbose_name='Ngày thanh toán')
    trang_thai = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Hoàn thành', verbose_name='Trạng thái')

    class Meta:
        verbose_name = "Lịch sử thanh toán"
        verbose_name_plural = "Lịch sử thanh toán"

    def __str__(self):
        return f"Thanh toán #{self.id} - {self.dat_ve} - {self.trang_thai}"

# 4. Model Đánh Giá (Review)
class Review(models.Model):
    ho_boi = models.ForeignKey(HoBoi, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người dùng")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        verbose_name="Điểm số (1-5)"
    )
    comment = models.TextField(blank=True, null=True, verbose_name="Nội dung bình luận")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đánh giá")

    def __str__(self):
        return f"{self.user.username} đánh giá {self.ho_boi.ten_ho} ({self.rating} sao)"

# Ghi chú: Mình đã gỡ bỏ class Pool vì nó đang dư thừa và gây nhầm lẫn với class HoBoi

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# 5. Model Dịch Vụ và Chi Tiết Dịch Vụ
class DichVu(models.Model):
    HINH_THUC_CHOICES = [
        ('THUE', 'Cho thuê'),
        ('BAN', 'Bán đứt'),
    ]
    ten_dich_vu = models.CharField(max_length=200, verbose_name="Tên dịch vụ")
    hinh_thuc = models.CharField(max_length=10, choices=HINH_THUC_CHOICES, verbose_name="Hình thức")
    don_vi_tinh = models.CharField(max_length=50, default='món', verbose_name="Đơn vị tính")
    so_luong_kho = models.IntegerField(default=0, verbose_name="Số lượng trong kho")
    don_gia = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Đơn giá")

    class Meta:
        verbose_name = "Dịch vụ"
        verbose_name_plural = "Dịch vụ"

    def __str__(self):
        return f"{self.ten_dich_vu} ({self.get_hinh_thuc_display()})"


class ChiTietDichVu(models.Model):
    TRANG_THAI_CHOICES = [
        ('DANG_MUON', 'Đang mượn'),
        ('DA_TRA', 'Đã trả'),
        ('HONG_MAT', 'Hỏng/Mất'),
        ('KHONG_AP_DUNG', 'Không áp dụng'),
    ]
    dat_ve = models.ForeignKey(DatVe, on_delete=models.CASCADE, verbose_name="Vé đặt")
    dich_vu = models.ForeignKey(DichVu, on_delete=models.CASCADE, verbose_name="Dịch vụ")
    so_luong = models.IntegerField(default=1, verbose_name="Số lượng")
    don_gia_thuc_te = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Đơn giá thực tế", blank=True, null=True)
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, verbose_name="Trạng thái", blank=True)

    class Meta:
        verbose_name = "Chi tiết dịch vụ"
        verbose_name_plural = "Chi tiết dịch vụ"

    def save(self, *args, **kwargs):
        if not self.don_gia_thuc_te:
            self.don_gia_thuc_te = self.dich_vu.don_gia
            
        if not self.pk:
            if self.dich_vu.hinh_thuc == 'BAN':
                self.trang_thai = 'KHONG_AP_DUNG'
            elif self.dich_vu.hinh_thuc == 'THUE':
                self.trang_thai = 'DANG_MUON'
                
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.dich_vu.ten_dich_vu} - SL: {self.so_luong} - {self.get_trang_thai_display()}"


# Signal quản lý kho
@receiver(pre_save, sender=ChiTietDichVu)
def track_old_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = ChiTietDichVu.objects.get(pk=instance.pk)
            instance._old_trang_thai = old_instance.trang_thai
        except ChiTietDichVu.DoesNotExist:
            instance._old_trang_thai = None
    else:
        instance._old_trang_thai = None

@receiver(post_save, sender=ChiTietDichVu)
def update_inventory_on_save(sender, instance, created, **kwargs):
    dich_vu = instance.dich_vu
    if created:
        # Khi tạo mới
        if instance.trang_thai in ['DANG_MUON', 'KHONG_AP_DUNG']:
            dich_vu.so_luong_kho -= instance.so_luong
            dich_vu.save()
    else:
        # Khi update
        old_trang_thai = getattr(instance, '_old_trang_thai', None)
        if old_trang_thai == 'DANG_MUON' and instance.trang_thai == 'DA_TRA':
            dich_vu.so_luong_kho += instance.so_luong
            dich_vu.save()