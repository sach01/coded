from django.contrib import admin

# Register your models here.
from modern.models import Floor, Room, Owner, Register, Arreas, Payment, Receiver, OwnerType
from django.contrib import admin
#from django.contrib.admin import AdminSite
from import_export.admin import ImportExportModelAdmin
import random
from datetime import date, timedelta
import csv
from datetime import datetime
from django.contrib.auth.models import User




class OwnerAdmin(ImportExportModelAdmin):
    list_display = ('name', 'mobile', 'id_number', 'date_created', 'date_edited', 'created_by')
    list_filter = ('date_created', 'date_edited')
    search_fields = ('name', 'mobile', 'id_number', 'created_by__username')

admin.site.register(Owner, OwnerAdmin)

# class RegisterAdmin(admin.ModelAdmin):
#     list_display = ('owner', 'room', 'reg_status', 'start_date', 'end_date', 'note', 'date_registered', 'date_edited', 'created_by')
#     list_filter = ('reg_status', 'start_date', 'end_date', 'date_registered', 'date_edited')
#     search_fields = ('owner__name', 'room__name', 'note', 'created_by__username')
#     actions = ['import_csv_data']

#     def import_csv_data(self, request, queryset):
#         for register in queryset:
#             file_path = '/Videos/coded/New Folder/New Folder/file.csv'  # Replace with the actual file path
#             try:
#                 with open(file_path, 'r') as csv_file:
#                     csv_reader = csv.DictReader(csv_file)
#                     for row in csv_reader:
#                         owner_name = row.get('owner')
#                         room_name = row.get('room')
#                         username = row.get('created_by')
#                         start_date = datetime.strptime(row.get('start_date'), '%Y-%m-%d')
#                         end_date = datetime.strptime(row.get('end_date'), '%Y-%m-%d') if row.get('end_date') else None

#                         owner, _ = Owner.objects.get_or_create(name=owner_name)
#                         room, _ = Room.objects.get_or_create(name=room_name)
#                         user, _ = User.objects.get_or_create(username=username)

#                         new_register = Register.objects.create(
#                             owner=owner,
#                             room=room,
#                             reg_status=row.get('reg_status'),
#                             start_date=start_date,
#                             end_date=end_date,
#                             note=row.get('note'),
#                             created_by=user
#                         )

#                 self.message_user(request, f"CSV data imported successfully for register: {register.id}")
#             except Exception as e:
#                 self.message_user(request, f"Error importing CSV data for register {register.id}: {str(e)}", level='error')

#     import_csv_data.short_description = "Import CSV Data for Selected Registers"

# admin.site.register(Register, RegisterAdmin)

class RegisterAdmin(ImportExportModelAdmin):
    list_display = ('owner', 'room', 'reg_status', 'start_date', 'end_date', 'note', 'date_registered', 'date_edited', 'created_by')
    list_filter = ('reg_status', 'start_date', 'end_date', 'date_registered', 'date_edited')
    search_fields = ('owner__name', 'room__room_number', 'note', 'created_by__username')

    def import_obj(self, obj, **data):
        owner_name = data.get('owner')
        room_number = data.get('room')

        # Find the Owner object based on the owner name
        try:
            owner = Owner.objects.get(name=owner_name)
            obj.owner = owner
        except Owner.DoesNotExist:
            # Handle the case where the owner does not exist
            pass

        # Find the Room object based on the room number
        try:
            room = Room.objects.get(room_number=room_number)
            obj.room = room
        except Room.DoesNotExist:
            # Handle the case where the room does not exist
            pass

        # Your other import logic...

        return super().import_obj(obj, **data)

admin.site.register(Register, RegisterAdmin)

admin.site.register(Floor)
admin.site.register(Room)

admin.site.register(Receiver)
admin.site.register(Arreas)
#admin.site.register(Deregister)
admin.site.register(Payment)
admin.site.register(OwnerType)