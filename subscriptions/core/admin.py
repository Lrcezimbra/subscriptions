from django.contrib import admin

from subscriptions.core.models import Column, Import, Modality, ShirtSize, Subscription

class SubscriptionModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'gender', 'date_of_birth','city', 'team', 'shirt_size', 'modality', 'import_')

    def import_(self, obj):
        return obj.import_t
    import_.short_description = 'Import'

class ImportModelAdmin(admin.ModelAdmin):
    list_display = ('pk','origin',)

class ColumnModelAdmin(admin.ModelAdmin):
    list_display = ('subscription_name', 'file_column',)

class ShirtSizeModelAdmin(admin.ModelAdmin):
    list_display = ('shirt_size', 'file_shirt_size',)

class ModalityModelAdmin(admin.ModelAdmin):
    list_display = ('modality', 'file_modality', )

admin.site.register(Column, ColumnModelAdmin)
admin.site.register(Import, ImportModelAdmin)
admin.site.register(Modality, ModalityModelAdmin)
admin.site.register(ShirtSize, ShirtSizeModelAdmin)
admin.site.register(Subscription, SubscriptionModelAdmin)
