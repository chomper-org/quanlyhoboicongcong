from django import forms
from .models import HoBoi, DatVe

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
            'gio_mo_cua', 'gio_dong_cua',
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
            'gio_mo_cua': forms.TimeInput(attrs={'class': 'w-full rounded-xl border border-gray-700 bg-[#0f172a] text-gray-200 px-4 py-3', 'type': 'time'}),
            'gio_dong_cua': forms.TimeInput(attrs={'class': 'w-full rounded-xl border border-gray-700 bg-[#0f172a] text-gray-200 px-4 py-3', 'type': 'time'}),
        
        }

class DatVeForm(forms.ModelForm):
    class Meta:
        model = DatVe
        fields = ['ngay_su_dung','gio_su_dung', 'so_luong_nguoi_lon', 'so_luong_tre_em']
        widgets = {
            'ngay_su_dung': forms.DateInput(attrs={'class': 'w-full rounded-xl border border-gray-700 bg-[#0f172a] text-gray-200 px-4 py-3', 'type': 'date'}),
            'so_luong_nguoi_lon': forms.NumberInput(attrs={'class': 'w-full rounded-xl border border-gray-700 bg-[#0f172a] text-gray-200 px-4 py-3', 'min': 0}),
            'so_luong_tre_em': forms.NumberInput(attrs={'class': 'w-full rounded-xl border border-gray-700 bg-[#0f172a] text-gray-200 px-4 py-3', 'min': 0}),
        }
    def clean(self):
        cleaned_data = super().clean()
        gio_su_dung = cleaned_data.get("gio_su_dung")
        
        if self.instance and self.instance.ho_boi:
            ho_boi = self.instance.ho_boi
            if gio_su_dung and (gio_su_dung < ho_boi.gio_mo_cua or gio_su_dung > ho_boi.gio_dong_cua):
                raise forms.ValidationError(f"Hồ bơi chỉ hoạt động từ {ho_boi.gio_mo_cua.strftime('%H:%M')} đến {ho_boi.gio_dong_cua.strftime('%H:%M')}.")
        return cleaned_data
