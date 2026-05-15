from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django_summernote.admin import SummernoteModelAdmin


class CustomModelExemptedAdmin(ImportExportModelAdmin, SummernoteModelAdmin): # type: ignore
    """
    Django Admin mixin for models that not inherit from `AbstractBaseModel` (i.e. 3rd party apps models).
    
    Used just to be able to perform basic actions like:
        - Import/Export
        - Rich text editing
    """
    
    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_staff



class AbstractBaseTabularInlineModelAdmin(admin.TabularInline):
    can_delete = True
    classes = ("collapse",)
    readonly_fields = ("created_on", "updated_on")
    extra = 1


class AbstractBaseStackedInlineModelAdmin(admin.StackedInline):
    can_delete = True
    classes = ("collapse",)
    inline_classes = ("collapse",)
    readonly_fields = ("created_on", "updated_on",)
    extra = 1




class AbstractBaseModelAdmin(CustomModelExemptedAdmin):
    list_display = ("created_on",)
    readonly_fields = ("uuid", "is_deleted", "created_on", "updated_on", "obj_created_by", "extra_data_pretty",
        *CustomModelExemptedAdmin.readonly_fields)
    list_filter = ("created_on", "is_deleted", *CustomModelExemptedAdmin.list_filter)
    search_fields = ("uuid", "created_on", "updated_on", "is_deleted", *CustomModelExemptedAdmin.search_fields)
    date_hierarchy = "created_on"
    actions = ()
    inlines = ()
