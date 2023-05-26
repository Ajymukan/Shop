from modeltranslation.translator import register, TranslationOptions
from .models import Products

@register(Products)
class ProductsTranslationOptions(TranslationOptions):
    fields = ('name','descriptions','gender')
    
