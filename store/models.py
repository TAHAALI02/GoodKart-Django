from django.db import models
from category.models import category
from django.shortcuts import reverse

# Create your models here.
class product(models.Model):
    product_name         = models.CharField(max_length=200)
    slug            = models.SlugField(max_length=200)
    description     = models.TextField()
    price           = models.IntegerField()
    image           = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(category,on_delete=models.CASCADE)
    created_at      = models.DateTimeField(auto_now_add=True)
    modified_at     = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_details',args=[self.category.slug,self.slug])

    def __str__(self):
        return self.product_name