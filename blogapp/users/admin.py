from django.contrib import admin
from users.models import Writer


class WriterAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'is_staff', 'is_editor', 'is_active')


admin.site.register(Writer, WriterAdmin)
