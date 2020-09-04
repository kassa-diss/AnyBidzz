from django.contrib import admin
from .models import Adds,UserProfile,Bids

# Register your models here.
class AddCreate(admin.ModelAdmin):
    readonly_fields = ('pub_date',)


admin.site.register(Adds, AddCreate)
admin.site.register(UserProfile)
admin.site.register(Bids)
