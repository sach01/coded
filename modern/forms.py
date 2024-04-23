from django import forms
from .models import Register, Payment, Room, Floor, Owner, Receiver, OwnerType, Bank
from datetime import datetime, date, timedelta
from django.forms import widgets
from django.core.exceptions import ValidationError

from django import forms
from .models import Owner, Room

class OwnerTypeForm(forms.ModelForm):
    class Meta:
        model = OwnerType
        fields = ['name']
# class OwnerForm(forms.ModelForm):
#     class Meta:
#         model = Owner
#         #fields = '__all__'
#         fields = ['name', 'mobile', 'id_number', 'owner_type']
class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['name',  'mobile', 'id_number', 'owner_type']
        widgets = {
            'owner_type': forms.Select(attrs={'class': 'form-control select2'})
        }

    def __init__(self, *args, **kwargs):
        super(OwnerForm, self).__init__(*args, **kwargs)
        self.fields['owner_type'].queryset = OwnerType.objects.all()
    # name = forms.CharField(max_length=255)
    # mobile = forms.CharField(max_length=15, required=False)
    # id_number = forms.CharField(max_length=20, required=False)

class OwnerChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, room):
        return f"{room.floor} ({room.room_number})"
    
class RegisterForm(forms.ModelForm):
    # start_date = forms.DateField(
    #     required=True,
    #     label='Start Date',
    #     widget=forms.DateInput(attrs={'class': 'form-control mb-3'}),
    # )
    owner = forms.ModelChoiceField(
        queryset=Owner.objects.all(),
        label='Owner Name',
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name='id',  # You can specify the field to use as the value for the option
    )
    #floor = forms.ChoiceField(choices=Room.FLOOR_CHOICES, required=True)
    floor = forms.ModelChoiceField(
        queryset=Floor.objects.all(),
        label='Room',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    room = forms.ModelChoiceField(
        queryset=Room.objects.all(),
        label='Room',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Register
        fields = ('owner', 'floor', 'room')
   
'''
    def clean_room(self):
        room = self.cleaned_data.get('room')

        # Check if there is already an owner for the selected room
        if room and Register.objects.filter(room=room).exclude(owner=None).exists():
            raise ValidationError("A stall owner for this room already exists.")

        return room
    '''



class RegisterEditForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['reg_status', 'note']

    end_date = forms.DateField(required=False, widget=forms.HiddenInput())
      
class DateInput(forms.DateInput):
    input_type = 'date'

# class PaymentForm(forms.ModelForm):
#     class Meta:
#         model = Payment
#         fields = ['owner', 'month_paid', 'pay_status', 'status', 'due_months', 'balance', 'collected_by']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['owner'].queryset = Register.objects.all()

# # class PaymentForm(forms.ModelForm):
# #     class Meta:
# #         model = Payment
# #         fields = ['owner'] # Add or remove fields as needed
class PaymentForm(forms.ModelForm):
    owner = forms.ModelChoiceField(queryset=Register.objects.all())   # We'll use JavaScript to autocomplete this field
    
    class Meta:
        model = Payment
        fields = ['owner']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].queryset = Register.objects.order_by('owner__name')

from django import forms
from .models import Payment, Register

# class PaymentForm(forms.ModelForm):
#     owner_name = forms.ModelChoiceField(queryset=Register.objects.all().values_list('owner__name', flat=True).distinct(), label='Owner Name')
#     room_number = forms.ModelChoiceField(queryset=Register.objects.all().values_list('room__room_number', flat=True).distinct(), label='Room Number')

#     # # owner_name = forms.ModelChoiceField(
#     # #     queryset=Register.objects.all().values_list('owner__name', flat=True).distinct(),
#     # #     label='Owner Name'
#     # # )
#     # # room_number = forms.ModelChoiceField(
#     # #     queryset=Register.objects.all().values_list('room__room_number', flat=True).distinct(),
#     # #     label='Room Number'
#     # # )
#     class Meta:
#         model = Payment
#         fields = ['owner_name', 'room_number']  # Add other fields as needed

from django_select2.forms import ModelSelect2Widget
class Payment2Form(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['owner']
        #fields = ['pay_status', 'status']
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['owner'].queryset = Register.objects.all()  # Set the queryset for the owner field to include all registers
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].widget = ModelSelect2Widget(
            model=Register,
            search_fields=['owner__name__icontains'],
            attrs={'data-placeholder': 'Search for owner'}
        )

from django import forms
from .models import Receiver

# class ReceiverForm(forms.ModelForm):
#     class Meta:
#         model = Receiver
#         fields = ['collector', 'amount_received', 'note']

#     def __init__(self, *args, **kwargs):
#         super(ReceiverForm, self).__init__(*args, **kwargs)
#         # If you want to customize form widgets or add additional validation,
#         # you can do so here.
# class ReceiverForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Set choices for the collector field to display usernames
#         self.fields['collector'].queryset = Receiver.objects.all()
#         self.fields['collector'].label_from_instance = lambda obj: obj.collector.collected_by.username

#     class Meta:
#         model = Receiver
#         fields = ['collector', 'amount_received', 'note']

from account.models import CustomUser
from django import forms
from .models import Receiver, Payment
class ReceiverForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['collector'].disabled = True
            self.fields['collector'].widget.attrs['value'] = self.instance.collector.collected_by.username
        else:
            # Configure the queryset to retrieve CustomUser instances
            self.fields['collector'].queryset = CustomUser.objects.all()

    class Meta:
        model = Receiver
        fields = ['collector', 'amount_received', 'note']
class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['receiver', 'amount_banked', 'note']

# class OwnerTypeForm(forms.ModelForm):
#     class Meta:
#         model = OwnerType
#         fields = ['name']


# class ReceiverForm(forms.ModelForm):
#     class Meta:
#         model = Receiver
#         fields = [ 'amount_received', 'note', 'received_by']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # Customize form fields and widgets
#         #self.fields['payment_mode'].widget = forms.Select(choices=GetPayment.payment_mode, attrs={'class': 'form-control'})
#         self.fields['amount_received'].widget = forms.NumberInput(attrs={'class': 'form-control'})
#         self.fields['note'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
#         self.fields['received_by'].widget = forms.Select(attrs={'class': 'form-control'})
        #self.fields['date_received'].widget = forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})

        # You can customize choices for 'payment' and 'received_by' fields if needed
        #self.fields['payment'].queryset = Payment.objects.all()  # Assuming Payment is another model

        # You can also set default values or hide certain fields if needed
        # self.fields['payment'].initial = some_initial_value
        # self.fields['date_received'].widget = forms.HiddenInput()



# class PaymentForm(forms.ModelForm):
#     owner = forms.ModelChoiceField(
#         queryset=Owner.objects.all(),
#         label='Owner Name',
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         to_field_name='id',  # You can specify the field to use as the value for the option
#     )
#     class Meta:
#         model = Payment
#         fields = ['owner',]

#     def clean(self):
#         cleaned_data = super().clean()
#         owner = cleaned_data.get('owner')

#         # Add any custom validation logic here if needed

#         return cleaned_data
class Payment1Form(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

'''    
class PaymentForm(forms.ModelForm):
    month_paid = forms.DateField(
                        required = True,
                        label='month paid',
                        widget=DateInput(attrs={'class': 'form-control mb-3'}),)

    class Meta:
        model = Payment
        #fields = __all__
        fields = ('owner', 'month_paid' )



class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['owner', 'room']

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room')

        if room.room_status:
            raise forms.ValidationError("This room is occupied")

        # Update room_status and reg_status if the room is available
        room.room_status = True
        room.save()
        cleaned_data['reg_status'] = True
        return cleaned_data

'''

'''
class RegisterEditForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['reg_status']

    def clean(self):
        cleaned_data = super().clean()
        reg_status = cleaned_data.get('reg_status')

        if not reg_status:
            room = self.instance.room
            room.room_status = False
            room.save()
            self.instance.end_date = date.today()
            self.instance.save()
        return cleaned_data


class RegisterDraftForm(forms.ModelForm):
    class Meta:
        model = RegisterDraft
        exclude = ['register', 'is_pending']
'''