import os
import re

directory = r'd:\code\visual studio code\poolweb\quanlyhoboicongcong\quan_ly_ho_boi\templates\quan_ly_ho_boi'
files_to_modify = [
    'admin_edit_booking.html',
    'admin_panel.html',
    'checkout.html',
    'invoice.html',
    'pool_list.html',
    'profile.html',
    'user_edit_booking.html'
]

for filename in files_to_modify:
    path = os.path.join(directory, filename)
    if not os.path.exists(path):
        continue
        
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Thêm load humanize ở đầu file
    if '{% load humanize %}' not in content:
        if '{% extends' in content:
            # Thêm ngay sau extends
            content = re.sub(r'({% extends [^}]+ %})', r'\1\n{% load humanize %}', content, count=1)
        else:
            # Thêm ngay sau thẻ doctype hoặc đầu file
            if '<!DOCTYPE html>' in content:
                content = content.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n{% load humanize %}')
            else:
                content = '{% load humanize %}\n' + content

    # Tìm các {{ var_name }} theo sau bởi khoảng trắng và đ
    content = re.sub(r'({{\s*[^}|]+)\s*}}([ ]*đ)', r'\1|intcomma }}\2', content)

    # cho pool_list.html: {{ pool.gia_ve_nguoi_lon|default:"0" }}đ
    content = re.sub(r'({{\s*[^}]+)\|default:\"0\"\s*}}([ ]*đ)', r'\1|default:\"0\"|intcomma }}\2', content)

    # Cho admin_edit_booking.html widthratio
    content = re.sub(r'({% widthratio item\.so_luong 1 item\.don_gia_thuc_te %})([ ]*đ)', r'{% widthratio item.so_luong 1 item.don_gia_thuc_te as subtotal %}{{ subtotal|intcomma }}\2', content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
print('Done!')
