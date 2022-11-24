from django.contrib import admin
from . import models


class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('service', 'quantity', 'price', 'total', 'order')
    ordering = ('order', 'id')
    list_filter = ('order', )


class OrderLineInline(admin.TabularInline):
    model = models.OrderLine
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineInline,)
    list_filter = ('date', 'status', 'user')  
    list_display = ('id', 'date', 'total', 'car', 'user', 'return_date')
    readonly_fields = ('is_overdue',)


class CarAdmin(admin.ModelAdmin):
    list_display = ('client', 'car_model', 'plate', 'vin')
    list_filter = ('client', 'car_model')


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('vin', 'plate') 


admin.site.register(models.Car, CarAdmin)
admin.site.register(models.CarModel)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderLine, OrderLineAdmin)
admin.site.register(models.OrderReview)
