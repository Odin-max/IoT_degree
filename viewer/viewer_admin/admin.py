from django.contrib import admin
from .models import IotData
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

# Завантаження ключа з файлу .env
load_dotenv()
FERNET_KEY = os.getenv('FERNET_KEY')
cipher = Fernet(FERNET_KEY)

@admin.register(IotData)
class IotDataAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp', 
        'last_updated', 
        'get_first_name', 
        'get_last_name', 
        'device_id', 
        'device_type', 
        'manufacturer', 
        'ip_address', 
        'mac_address', 
        'connection_status', 
        'get_critical_data'
    )
    readonly_fields = list_display

    def get_first_name(self, obj):
        return cipher.decrypt(obj.first_name.encode()).decode()
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return cipher.decrypt(obj.last_name.encode()).decode()
    get_last_name.short_description = 'Last Name'

    def get_critical_data(self, obj):
        if obj.critical_data:
            return cipher.decrypt(obj.critical_data.encode()).decode()
        return None
    get_critical_data.short_description = 'Critical Data'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
