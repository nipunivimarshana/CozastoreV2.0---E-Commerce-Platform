from django.db import models
from django.urls import reverse # This import is necessary

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    # It's also good practice to give the Category a URL
    def get_absolute_url(self):
        # This assumes you might create a page to list products by category later
        # We can just use a placeholder for now if you don't have this URL yet
        return "#" # Or return reverse('products:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    # --- THIS IS THE METHOD YOU NEED TO ADD ---
    def get_absolute_url(self):
        """
        Returns the canonical URL for a single product.
        """
        return reverse('products:product_detail', args=[self.slug])
    # ----------------------------------------