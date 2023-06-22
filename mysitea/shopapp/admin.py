from django.contrib import admin
from .models import Product, Profile, ProductParameter, Parameter

admin.site.register(Product),
admin.site.register(Parameter),
admin.site.register(Profile),
admin.site.register(ProductParameter),
