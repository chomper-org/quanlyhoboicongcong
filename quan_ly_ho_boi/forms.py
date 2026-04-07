from django import forms
from .models import HoBoi

class HoBoiForm(forms.ModelForm):
    class Meta:
        model = HoBoi
        fields = [
            'ten_ho',
            'dia_chi',
            'do_sau',
            'suc_chua',
            'vi_do',
            'kinh_do',
            'gia_ve_nguoi_lon',
            'gia_ve_tre_em',
            'trang_thai',
            'hinh_anh',
        ]
        widgets = {
            'ten_ho': forms.TextInput(attrs={'class': 'w-full rounded-xl border border-gray-700 bg-[#0f172a] text-gray-200 px-4 py-3', 'placeholder': 'Tên hồ bơi'}),
            'dia_chi': forms.Textarea(attrs={'class': 'w-full rounded-xl border border-gray-700 bg-[#0f172a] text-gray-200 px-4 py-3', 'rows': 3, 'placeholder': 'Địa chỉ'}),
            'do_sau': forms.NumberInput(attrs={'class': 'w-full rounded-xl border border-gray-700 bg-[#0f172a] text-gray-200 px-4 py-3', 'step': '0.1', 'placeholder': 'Độ sâu (m)'}),
            'suc_chua': forms.NumberInput(attrs={'class': 'w-full rounded-xl border border-gray-700 bg-[#0f172a] text-gray-200 px-4 py-3', 'placeholder': 'Sức chứa'}),
            'vi_do': forms.NumberInput(attrs={'class': 'w-full rounded-xl border border-gray-700 bg-[#0f172a] text-gray-200 px-4 py-3', 'step': '0.000001', 'placeholder': 'Vĩ độ'}),
            'kinh_do': forms.NumberInput(attrs={'class': 'w-full rounded-xl border border-gray-700 bg-[#0f172a] text-gray-200 px-4 py-3', 'step': '0.000001', 'placeholder': 'Kinh độ'}),
            'gia_ve_nguoi_lon': forms.NumberInput(attrs={'class': 'w-full rounded-xl border border-gray-700 bg-[#0f172a] text-gray-200 px-4 py-3', 'placeholder': 'Giá vé người lớn'}),
            'gia_ve_tre_em': forms.NumberInput(attrs={'class': 'w-full rounded-xl border border-gray-700 bg-[#0f172a] text-gray-200 px-4 py-3', 'placeholder': 'Giá vé trẻ em'}),
            'trang_thai': forms.Select(attrs={'class': 'w-full rounded-xl border border-gray-700 bg-[#0f172a] text-gray-200 px-4 py-3'}),
            'hinh_anh': forms.ClearableFileInput(attrs={'class': 'text-gray-200'}),
        }
