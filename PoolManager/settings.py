"""
Django settings for PoolManager project.
Cấu hình chuẩn cho giao diện SIMPLEUI (Phiên bản đẹp & Gọn).
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
    'simpleui', # SimpleUI phải luôn nằm đầu tiên
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

# --- CẤU HÌNH NGÔN NGỮ & GIỜ ---
LANGUAGE_CODE = 'vi' # Tiếng Việt
TIME_ZONE = 'Asia/Ho_Chi_Minh' # Giờ VN
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static') 

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ==========================================
# --- CẤU HÌNH GIAO DIỆN SIMPLEUI (ĐÃ FIX LỖI MẤT MENU) ---
# ==========================================

# 1. Thông tin cơ bản
SIMPLEUI_HOME_INFO = False  
SIMPLEUI_ANALYSIS = False   
SIMPLEUI_LOADING = True     

# 2. Logo & Tiêu đề
SIMPLEUI_LOGO = 'https://cdn-icons-png.flaticon.com/512/2972/2972166.png'
SIMPLEUI_HOME_TITLE = 'QUẢN TRỊ HỒ BƠI' 
SIMPLEUI_HOME_ICON = 'fas fa-water' 

# 3. Giao diện (Theme)
SIMPLEUI_DEFAULT_THEME = 'admin.lte.css' 

# 4. Icon Menu (FontAwesome)
SIMPLEUI_ICON = {
    'Hồ bơi': 'fas fa-swimming-pool',    
    'Vé đặt': 'fas fa-file-invoice-dollar', 
    'Users': 'fas fa-user-tie',          
    'Groups': 'fas fa-users-cog',        
}

SIMPLEUI_HOME_QUICK = True   
SIMPLEUI_HOME_ACTION = False 

# QUAN TRỌNG: Đã xóa phần SIMPLEUI_CONFIG gây lỗi mất menu