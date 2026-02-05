from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from .models import HoBoi, DatVe

# 1. Trang chủ (Hiển thị danh sách đẹp cho người dùng)
def trang_chu(request: HttpRequest):
    danh_sach_ho = HoBoi.objects.all()
    return render(request, 'quan_ly_ho_boi/index.html', {'danh_sach_ho': danh_sach_ho})

# 2. Dashboard (Thống kê)
def dashboard(request: HttpRequest):
    tong_ho_boi = HoBoi.objects.count()
    tong_ve_dat = DatVe.objects.count()
    ho_dang_mo = HoBoi.objects.filter(trang_thai='MO').count()
    
    context = {
        'tong_ho_boi': tong_ho_boi,
        'tong_ve_dat': tong_ve_dat,
        'ho_dang_mo': ho_dang_mo,
    }
    return render(request, 'quan_ly_ho_boi/dashboard.html', context)

# 3. Bản đồ GIS (Trang trống chờ code tool của bạn)
def ban_do(request: HttpRequest):
    return render(request, 'quan_ly_ho_boi/map.html')

# 4. Trang Quản lý (Danh sách dạng bảng + Nút Xóa)
def quan_ly_danh_sach(request: HttpRequest):
    danh_sach_ho = HoBoi.objects.all()
    return render(request, 'quan_ly_ho_boi/manage_list.html', {'danh_sach_ho': danh_sach_ho})

# 5. Chức năng Xóa hồ bơi
def xoa_ho_boi(request: HttpRequest, ho_boi_id : int):
    ho_boi = get_object_or_404(HoBoi, id=ho_boi_id)
    if request.method == 'POST':
        ho_boi.delete()
        return redirect('quan_ly')
    return redirect('quan_ly')