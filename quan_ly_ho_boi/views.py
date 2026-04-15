import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils.dateparse import parse_date
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum
from .models import HoBoi, DatVe, Payment, Review
from .forms import HoBoiForm, DatVeForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db.models import Avg, Count
from django.http import JsonResponse


def gioi_thieu(request):
    return render(request, 'quan_ly_ho_boi/gioi_thieu.html')


# 3. Bản đồ GIS (Trang trống chờ code tool của bạn)
def ban_do(request: HttpRequest):
    return render(request, 'quan_ly_ho_boi/map.html')



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


# 8. Trang admin tùy chỉnh (Tổng hợp quản lý)
@login_required
def admin_home(request: HttpRequest):
    if not request.user.is_staff:
        return redirect('home')  # Chỉ cho phép staff truy cập
    
    # --- DỮ LIỆU CHO TAB THỐNG KÊ (DASHBOARD) ---
    tong_ho_boi = HoBoi.objects.count()
    tong_ve_dat = DatVe.objects.count()
    ho_dang_mo = HoBoi.objects.filter(trang_thai='MO').count()
    tong_doanh_thu = Payment.objects.filter(trang_thai='Hoàn thành').aggregate(total=Sum('so_tien'))['total'] or 0
    ho_boi_gan_day = HoBoi.objects.order_by('-id')[:5]
    ve_dat_gan_day = DatVe.objects.select_related('ho_boi', 'khach_hang').order_by('-ngay_dat')[:10]
    
    # --- DỮ LIỆU CHO TAB QUẢN LÝ HỒ BƠI ---
    danh_sach_ho = HoBoi.objects.all()
    
    context = {
        'tong_ho_boi': tong_ho_boi,
        'tong_ve_dat': tong_ve_dat,
        'ho_dang_mo': ho_dang_mo,
        'tong_doanh_thu': tong_doanh_thu,
        'ho_boi_gan_day': ho_boi_gan_day,
        've_dat_gan_day': ve_dat_gan_day,
        'danh_sach_ho': danh_sach_ho, # Đã thêm dữ liệu này
    }
    return render(request, 'quan_ly_ho_boi/admin_panel.html', context)

# 8.1. Login cho admin panel
def login_admin(request: HttpRequest):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_panel')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_panel')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng, hoặc bạn không có quyền truy cập.')
    
    return render(request, 'quan_ly_ho_boi/login_admin.html')

# 8.2. Logout cho admin panel
def logout_admin(request: HttpRequest):
    logout(request)
    return redirect('login_admin')

# 9. Chức năng Xóa hồ bơi
def xoa_ho_boi(request: HttpRequest, ho_boi_id : int):
    ho_boi = get_object_or_404(HoBoi, id=ho_boi_id)
    if request.method == 'POST':
        ho_boi.delete()
        return redirect('admin_panel')
    return redirect('admin_panel')

@login_required
def xoa_dat_ve(request: HttpRequest, datve_id: int):
    if not request.user.is_staff:
        return redirect('home')

    dat_ve = get_object_or_404(DatVe, id=datve_id)
    if request.method == 'POST':
        dat_ve.delete()
        messages.success(request, 'Vé đặt đã được xóa.')
        return redirect('admin_panel')
    return redirect('admin_panel')

# 10. Tạo hồ bơi mới trong admin
@login_required
def tao_ho_boi(request: HttpRequest):
    if not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        form = HoBoiForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hồ bơi đã được tạo thành công.')
            return redirect('admin_panel')
    else:
        form = HoBoiForm()

    return render(request, 'quan_ly_ho_boi/admin_pool_form.html', {
        'form': form,
    })

# 11. Chỉnh sửa hồ bơi trong admin
@login_required
def chinh_sua_ho_boi(request: HttpRequest, ho_boi_id: int):
    if not request.user.is_staff:
        return redirect('home')

    ho_boi = get_object_or_404(HoBoi, id=ho_boi_id)
    if request.method == 'POST':
        form = HoBoiForm(request.POST, request.FILES, instance=ho_boi)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thông tin hồ bơi đã được cập nhật.')
            return redirect('admin_panel')
    else:
        form = HoBoiForm(instance=ho_boi)

    return render(request, 'quan_ly_ho_boi/admin_pool_form.html', {
        'form': form,
    })

@login_required
def chinh_sua_dat_ve(request: HttpRequest, datve_id: int):
    if not request.user.is_staff:
        return redirect('home')

    dat_ve = get_object_or_404(DatVe, id=datve_id)
    if request.method == 'POST':
        form = DatVeForm(request.POST, instance=dat_ve)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thông tin vé đã được cập nhật.')
            return redirect('admin_panel')
    else:
        form = DatVeForm(instance=dat_ve)

    return render(request, 'quan_ly_ho_boi/admin_edit_booking.html', {
        'form': form,
        'dat_ve': dat_ve,
    })

# 12. Trang chủ công khai (Home Page)
def home_page(request: HttpRequest):
    """Trang chủ cho khách hàng công khai"""
    danh_sach_ho = HoBoi.objects.all()
    ho_dang_mo = HoBoi.objects.filter(trang_thai='MO').count()
    context = {
        'danh_sach_ho': danh_sach_ho,
        'ho_dang_mo': ho_dang_mo,
    }
    return render(request, 'quan_ly_ho_boi/home.html', context)

# 11. Trang cá nhân (User Profile)
@login_required(login_url='/login/')
def user_profile(request: HttpRequest):
    """Trang thông tin cá nhân của người dùng (Bắt buộc đăng nhập)"""
    user = request.user
    # Lịch sử vé đặt của người dùng
    lich_su_ve = DatVe.objects.filter(khach_hang=user).select_related('ho_boi').order_by('-ngay_dat')[:10]
    # Lịch sử thanh toán của người dùng
    lich_su_thanh_toan = Payment.objects.filter(dat_ve__khach_hang=user).select_related('dat_ve__ho_boi').order_by('-ngay_thanh_toan')[:5]
    
    context = {
        'user': user,
        'lich_su_ve': lich_su_ve,
        'lich_su_thanh_toan': lich_su_thanh_toan,
        'tong_ve_da_dat': lich_su_ve.count(),
    }
    return render(request, 'quan_ly_ho_boi/profile.html', context)

# Custom 404 page handler
def page_not_found_view(request, exception=None):
    return render(request, 'quan_ly_ho_boi/404.html', status=404)

# 12. Đăng nhập cho user bình thường
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'quan_ly_ho_boi/login_user.html', {'error': 'Tên đăng nhập hoặc mật khẩu không đúng.'})
    return render(request, 'quan_ly_ho_boi/login_user.html')

# 13. Đăng xuất user
def logout_user(request):
    logout(request)
    return redirect('home')

# 14. Đăng ký user
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False
            user.is_superuser = False
            user.save()
            return redirect('login_user')
    else:
        form = UserCreationForm()
    return render(request, 'quan_ly_ho_boi/register.html', {'form': form})

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

def pool_list(request):
    # Lấy danh sách hồ bơi, TỰ ĐỘNG đính kèm Điểm trung bình và Tổng số đánh giá
    pools = Pool.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).order_by('-avg_rating') # Mặc định sắp xếp ưu tiên hồ bơi điểm cao

    context = {
        'pools': pools
    }
    return render(request, 'quan_ly_ho_boi/pool_list.html')
def pool_list(request):
    # Lấy tất cả HoBoi, tính điểm trung bình (avg_rating) 
    # và số lượng đánh giá (review_count) cho mỗi hồ
    pools = HoBoi.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).all()
    
    return render(request, 'quan_ly_ho_boi/pool_list.html', {'pools': pools})

@login_required
def add_review(request, ho_boi_id):
    if request.method == 'POST':
        ho_boi = get_object_or_404(HoBoi, id=ho_boi_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        Review.objects.create(
            ho_boi=ho_boi,
            user=request.user,
            rating=rating,
            comment=comment
        )
        messages.success(request, "Cảm ơn bạn đã đánh giá!")
    return redirect('pool_list')
def submit_review(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Bạn cần đăng nhập!'}, status=403)
            
        try:
            data = json.loads(request.body)
            # Tìm hồ bơi theo ID
            ho_boi = HoBoi.objects.get(id=data['pool_id'])
            
            # Tạo đánh giá liên kết với HoBoi
            Review.objects.create(
                ho_boi=ho_boi,
                user=request.user,
                rating=data['rating'],
                comment=data['comment']
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
            
    return JsonResponse({'status': 'error', 'message': 'Yêu cầu không hợp lệ'}, status=400)

def test_payment_api(request):
    """API giả lập cổng thanh toán ngân hàng"""
    if request.method == 'POST':
        try:
            # Lấy dữ liệu từ Frontend gửi lên
            data = json.loads(request.body)
            so_the = data.get('card_number')
            
            # GIẢ LẬP LOGIC NGÂN HÀNG:
            # Quy ước: Chỉ thẻ có đuôi "9999" mới thanh toán thành công, còn lại báo lỗi (để test cả 2 trường hợp)
            if so_the and so_the.endswith('9999'):
                return JsonResponse({
                    'status': 'success', 
                    'transaction_id': 'TEST_' + str(request.user.id) + '_8888',
                    'message': 'Thanh toán qua thẻ thành công!'
                })
            else:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Thẻ không hợp lệ hoặc số dư không đủ. (Gợi ý: Dùng thẻ đuôi 9999)'
                })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
            
    return JsonResponse({'status': 'error', 'message': 'Yêu cầu không hợp lệ'}, status=400)