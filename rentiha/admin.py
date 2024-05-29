from django.contrib import admin

from dashboard.models import Category, Iha, Rental

# Register models to manage them in the Django admin interface
admin.site.register(Category)
admin.site.register(Iha)
admin.site.register(Rental)
