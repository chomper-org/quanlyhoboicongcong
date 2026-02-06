"""
Django settings for PoolManager project.
Cấu hình chuẩn cho giao diện SIMPLEUI.
"""

from pathlib import Path
import os 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)q55+tfp057uwxb93dhb=z)4tf&*c*g^a@xckpqd-!dn2zb1e2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'simpleui', # Giao diện đẹp (Phải để dòng đầu tiên)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'quan_ly_ho_boi.apps.QuanLyHoBoiConfig', # App của bạn
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PoolManager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'PoolManager.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# --- CẤU HÌNH NGÔN NGỮ & GIỜ (QUAN TRỌNG) ---
LANGUAGE_CODE = 'vi' # Chuyển sang Tiếng Việt
TIME_ZONE = 'Asia/Ho_Chi_Minh' # Giờ Việt Nam
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static') 

# Cấu hình đường dẫn lưu ảnh (Media)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- CẤU HÌNH GIAO DIỆN SIMPLEUI ---
SIMPLEUI_HOME_INFO = False  # Tắt thông tin server ở trang chủ cho gọn
SIMPLEUI_ANALYSIS = False   # Tắt thu thập phân tích

# Logo và Tiêu đề trang Admin
SIMPLEUI_LOGO = 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png'
SIMPLEUI_HOME_TITLE = 'HỒ BƠI CÔNG CỘNG' 
SIMPLEUI_DEFAULT_THEME = 'admin.lte.css' # Theme màu mặc định (Giống AdminLTE)

# Cấu hình Icon (Mapping theo tên verbose_name trong models.py)
SIMPLEUI_ICON = {
    'Hồ bơi': 'fas fa-swimming-pool',  # Icon người bơi
    'Vé đặt': 'fas fa-ticket-alt',     # Icon vé
    'Users': 'fas fa-user',            
    'Groups': 'fas fa-users'           
}

# Tắt quảng cáo/link rác của SimpleUI
SIMPLEUI_HOME_QUICK = True
SIMPLEUI_HOME_ACTION = True