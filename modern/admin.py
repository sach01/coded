from django.contrib import admin

# Register your models here.
from modern.models import Floor, Room, Owner, Register, Arreas, Payment, Receiver
from django.contrib import admin
#from django.contrib.admin import AdminSite

admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(Owner)
admin.site.register(Receiver)
admin.site.register(Arreas)
#admin.site.register(Deregister)
admin.site.register(Payment)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ('owner', 'room', 'reg_status', 'start_date', 'end_date', 'note', 'date_registered', 'date_edited')
    search_fields = ['owner__name', 'room__name']  # Add search fields if needed
    list_filter = ('reg_status', 'start_date', 'end_date')  # Add filters if needed

admin.site.register(Register, RegisterAdmin)