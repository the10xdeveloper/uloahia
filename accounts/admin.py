from django.contrib import admin

from django.contrib import admin

from .models import WebUser, Vendor, Address, Vendee


class AddressInlineAdmin(admin.TabularInline):
    model = Address
    pass


@admin.register(WebUser)
class WebUserAdmin(admin.ModelAdmin):
    list_display = (
        'email', 'first_name', 'last_name', 'admin', 'is_vendee', 'is_vendor', 'is_dispatcher', 'last_login',
    )
    list_filter = (
        'is_superuser', 'staff', 'admin', 'is_vendee', 'is_vendor', 'is_dispatcher', 'is_active',
    )

    raw_id_fields = ('groups', 'user_permissions')
    date_hierarchy = 'updated_at'


class UserInlineAdmin(admin.TabularInline):
    model = WebUser
    pass


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = (
        'business_name', 'user', 'business_type',
    )
    # prepopulated_fields = {'slug': ('slug',)}


@admin.register(Vendee)
class VendeeAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'default_billing_address', 'default_shipping_address'
    )


admin.site.register(Address)
