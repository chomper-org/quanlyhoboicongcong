import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.utils.dateparse import parse_date
from .models import HoBoi, DatVe, Payment
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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

# 5. Trang đặt vé cho hồ bơi cụ thể
def dat_ve(request: HttpRequest, ho_boi_id: int):
    ho_boi = get_object_or_404(HoBoi, id=ho_boi_id)
    errors = []
    form_data = {
        'ngay_su_dung': '',
        'so_luong_nguoi_lon': '1',
        'so_luong_tre_em': '0',
    }
    tong_tien = None
    success_message = None

    if request.method == 'POST':
        form_data['ngay_su_dung'] = request.POST.get('ngay_su_dung', '')
        form_data['so_luong_nguoi_lon'] = request.POST.get('so_luong_nguoi_lon', '1')
        form_data['so_luong_tre_em'] = request.POST.get('so_luong_tre_em', '0')

        if not form_data['ngay_su_dung']:
            errors.append('Vui lòng chọn ngày sử dụng.')

        try:
            ngay_su_dung = parse_date(form_data['ngay_su_dung'])
            if ngay_su_dung is None:
                raise ValueError('Ngày không hợp lệ.')
        except ValueError:
            errors.append('Ngày sử dụng không hợp lệ.')
            ngay_su_dung = None

        try:
            so_luong_nguoi_lon = int(form_data['so_luong_nguoi_lon'])
            so_luong_tre_em = int(form_data['so_luong_tre_em'])
            if so_luong_nguoi_lon < 0 or so_luong_tre_em < 0:
                raise ValueError()
        except ValueError:
            errors.append('Số lượng trẻ em và người lớn phải là số nguyên không âm.')
            so_luong_nguoi_lon = 1
            so_luong_tre_em = 0

        if not errors and ngay_su_dung:
            current_user = request.user if request.user.is_authenticated else None
            if current_user is None:
                current_user, _ = User.objects.get_or_create(
                    username='guest',
                    defaults={'first_name': 'Khách ẩn danh'}
                )

            dat_ve = DatVe(
                khach_hang=current_user,
                ho_boi=ho_boi,
                ngay_su_dung=ngay_su_dung,
                so_luong_nguoi_lon=so_luong_nguoi_lon,
                so_luong_tre_em=so_luong_tre_em,
            )
            dat_ve.save()
            return redirect('checkout', datve_id=dat_ve.id)

    else:
        # Tính nhanh tổng tiền hiển thị nếu chỉ có giá vé
        tong_tien = (Decimal(ho_boi.gia_ve_nguoi_lon) * Decimal(form_data['so_luong_nguoi_lon'])
                     + Decimal(ho_boi.gia_ve_tre_em) * Decimal(form_data['so_luong_tre_em']))

    if ho_boi:
        try:
            tong_tien = (Decimal(ho_boi.gia_ve_nguoi_lon) * Decimal(form_data['so_luong_nguoi_lon'])
                         + Decimal(ho_boi.gia_ve_tre_em) * Decimal(form_data['so_luong_tre_em']))
        except Exception:
            tong_tien = None

    return render(request, 'quan_ly_ho_boi/booking.html', {
        'ho_boi': ho_boi,
        'errors': errors,
        'form_data': form_data,
        'tong_tien': tong_tien,
        'success_message': success_message,
    })


def checkout(request: HttpRequest, datve_id: int):
    dat_ve = get_object_or_404(DatVe, id=datve_id)
    payment_message = None
    payment_method = 'Tiền mặt'

    if request.method == 'POST':
        method = request.POST.get('payment_method', 'cash')
        labels = {
            'cash': 'Tiền mặt',
            'card': 'Thẻ ngân hàng',
            'mobile': 'Thanh toán di động',
        }
        payment_method = labels.get(method, 'Tiền mặt')
        payment, created = Payment.objects.get_or_create(
            dat_ve=dat_ve,
            defaults={
                'phuong_thuc': payment_method,
                'so_tien': dat_ve.tong_tien,
                'trang_thai': 'Hoàn thành',
            }
        )
        if not created:
            payment.phuong_thuc = payment_method
            payment.so_tien = dat_ve.tong_tien
            payment.trang_thai = 'Hoàn thành'
            payment.save()

        payment_message = (
            f"Thanh toán thành công bằng phương thức {payment_method}. "
            f"Vé đặt mã #{dat_ve.id} cho hồ bơi '{dat_ve.ho_boi.ten_ho}' đã được xác nhận."
        )

    return render(request, 'quan_ly_ho_boi/checkout.html', {
        'dat_ve': dat_ve,
        'payment_message': payment_message,
        'payment_method': payment_method,
    })

# 6. Lịch sử thanh toán

def lich_su_thanh_toan(request: HttpRequest):
    lich_su = Payment.objects.select_related('dat_ve__ho_boi', 'dat_ve__khach_hang').order_by('-ngay_thanh_toan')
    return render(request, 'quan_ly_ho_boi/payment_history.html', {
        'lich_su': lich_su,
    })

# 7. Chức năng Xóa hồ bơi
def xoa_ho_boi(request: HttpRequest, ho_boi_id : int):
    ho_boi = get_object_or_404(HoBoi, id=ho_boi_id)
    if request.method == 'POST':
        ho_boi.delete()
        return redirect('quan_ly')
    return redirect('quan_ly')
# 6. Lưu xử lí dữ liệu
@csrf_exempt
def luu_ho_boi(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Log kiểm tra dữ liệu đầu vào
            print("Data nhận được:", data)
            
            ho_boi_moi = HoBoi.objects.create(
                ten_ho=data.get('name'),
                vi_do=float(data.get('lat')),
                kinh_do=float(data.get('lng')),
                # Cung cấp giá trị mặc định cho các trường bắt buộc trong Model
                dia_chi="Chưa xác định", 
                do_sau=1.5,
                suc_chua=50,
                trang_thai='MO'
            )
            return JsonResponse({'status': 'success', 'id': ho_boi_moi.id})
        except Exception as e:
            print("Lỗi Server:", str(e)) # Xem lỗi cụ thể tại Terminal
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'failed'}, status=400)
# 7. Xuất dữ liệu hồ
def get_pools(request):
    pools = HoBoi.objects.all()
    data = []
    for p in pools:
        data.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [p.kinh_do, p.vi_do]
            },
            "properties": {
                "id": p.id,
                "name": p.ten_ho,
                "address": p.dia_chi,
                "status_code": p.trang_thai,
                "status": p.get_trang_thai_display(),
                "depth": p.do_sau,
                "capacity": p.suc_chua,
                "price_adult": str(p.gia_ve_nguoi_lon),
                "price_child": str(p.gia_ve_tre_em),
                "image": p.hinh_anh.url if p.hinh_anh else '',
            }
        })
    return JsonResponse({"type": "FeatureCollection", "features": data})