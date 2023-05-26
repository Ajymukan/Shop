from django.contrib import admin
from .models import Products,Brand,Comment,Cart,Order
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin

# Register your models here.
class ProductsAdmin(TranslationAdmin):
    list_display = ['name','brand','price', 'size','quant']
    list_filter = ["brand", "size","gender"]
    search_fields = ('name',)
    readonly_fields= ('get_image',)

    def get_image(self,obj):
        return mark_safe(f'<img scr={obj.image.url} width = "40", heigth="40" >')
    

    fieldsets = (

        (None, {"fields" : (
                    ("name",),
                    ("descriptions",),
                    ("price",),
                    ("size",),
                    ("gender",),
                    ("quant",),
        )}),

        ("Brand", {
            "classes" : ("callapse"),
            "fields" : (
                ( "brand",),
                ( "image", "get_image", ),

            )
        }

         )




    )
admin.site.register(Products,ProductsAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    search_fields = ('name',)

admin.site.register(Brand,BrandAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_filter = ("username", "comment")
    search_fields = ('username',)



admin.site.register(Comment,CommentAdmin)

admin.site.register(Cart)
admin.site.register(Order)

