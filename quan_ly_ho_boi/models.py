from django.db import models
from django.contrib.auth.models import User

# Model Há»“ BÆ¡i
class HoBoi(models.Model):
    TRANG_THAI_CHOICES = [
        ('MO', 'Äang má»Ÿ'),
        ('BAO_TRI', 'Báº£o trÃ¬'),
        ('DONG', 'ÄÃ³ng cá»­a'),
    ]
    
    ten_ho = models.CharField(max_length=200, verbose_name="TÃªn há»“ bÆ¡i")
    dia_chi = models.TextField(verbose_name="Äá»‹a chá»‰")
    do_sau = models.FloatField(help_text="Äá»™ sÃ¢u tÃ­nh báº±ng mÃ©t", verbose_name="Äá»™ sÃ¢u (m)")
    suc_chua = models.IntegerField(verbose_name="Sá»©c chá»©a tá»‘i Ä‘a")
    gia_ve_nguoi_lon = models.DecimalField(max_digits=10, decimal_places=0, default=50000)
    gia_ve_tre_em = models.DecimalField(max_digits=10, decimal_places=0, default=30000)
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='MO')
    hinh_anh = models.ImageField(upload_to='ho_boi/', blank=True, null=True)

    def __str__(self):
        return self.ten_ho

# Model VÃ©/Äáº·t chá»—
class DatVe(models.Model):
    khach_hang = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="KhÃ¡ch hÃ ng")
    ho_boi = models.ForeignKey(HoBoi, on_delete=models.CASCADE, verbose_name="Há»“ bÆ¡i")
    ngay_dat = models.DateTimeField(auto_now_add=True)
    ngay_su_dung = models.DateField(verbose_name="NgÃ y bÆ¡i")
    so_luong_nguoi_lon = models.IntegerField(default=1)
    so_luong_tre_em = models.IntegerField(default=0)
    tong_tien = models.DecimalField(max_digits=12, decimal_places=0, editable=False)

    def save(self, *args, **kwargs):
        self.tong_tien = (self.so_luong_nguoi_lon * self.ho_boi.gia_ve_nguoi_lon) + \
                         (self.so_luong_tre_em * self.ho_boi.gia_ve_tre_em)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.khach_hang.username} - {self.ho_boi.ten_ho} ({self.ngay_su_dung})"
