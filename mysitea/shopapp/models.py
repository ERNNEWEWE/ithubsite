from django.contrib.auth.models import User
from django.db import models
def product_preview_directory_path(instance: "Product", filename: str) -> str:
    return "products/product_{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )
class Product(models.Model):
    class Meta:
        ordering = ["name", "price"]
    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    views_count = models.DecimalField(default=0, max_digits=8, decimal_places=0)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=100, null=False, blank=True)
    first_name = models.CharField(max_length=100, null=False, blank=True)
    email = models.CharField(max_length=100, null=False, blank=True)
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user}'s cart"
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    class Meta:
        unique_together = ('cart', 'product')
    def __str__(self):
        return f"{self.quantity} x {self.product}"
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return f"{self.user}'s order #{self.id}"
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    class Meta:
        unique_together = ('order', 'product')
    def __str__(self):
        return f"{self.quantity} x {self.product}"

class Parameter(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
class ProductParameter(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    value = models.CharField(max_length=200)
    def __str__(self):
        return f'{self.product} - {self.parameter}: {self.value}'




