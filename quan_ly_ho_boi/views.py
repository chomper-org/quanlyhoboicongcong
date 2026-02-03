from django.shortcuts import render
from django.http import HttpRequest  
from .models import HoBoi


def trang_chu(request: HttpRequest):
  
    danh_sach_ho = HoBoi.objects.all()
    
    context = {
        'danh_sach_ho': danh_sach_ho
    }

    return render(request, 'quan_ly_ho_boi/index.html', context)