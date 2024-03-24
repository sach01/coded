from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime, date
import datetime
import calendar
#from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from account.models import CustomUser
from django.db import models
from django.utils.crypto import get_random_string
from dateutil.relativedelta import relativedelta
from datetime import date
import random
import string

# Create your models here.

    
class Floor(models.Model):
    name = models.CharField(max_length=10, unique=True) 

    def __str__(self):
        return '%s'% (self.name)

class Room(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    #floor = models.CharField(max_length=6, choices=FLOOR_CHOICES)
    room_number = models.CharField(max_length=5, unique=True)
    amount = models.IntegerField()
    room_status = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s %s %s %s %s'% (self.floor, self.room_number, self.amount, self.room_status, self.date_created)
    
class Owner(models.Model):
    name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10, blank=True, null=True)
    id_number = models.CharField(max_length=10, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default='')

    def __str__(self):
        return '%s %s %s %s'% (self.name, self.mobile, self.date_created, self.date_edited)

class Register(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    reg_status = models.BooleanField(default=True)#True > room = True
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)#reason
    date_registered = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default='')
    def __str__(self):
        return '%s %s %s %s %s'% (self.owner.name, self.room.room_number, self.reg_status, self.start_date, self.date_registered)
    
    class Meta:
        # Ensure that a Register is unique based on both owner and room
        unique_together = ['owner', 'room']

def generate_invoice_number():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    #invoice_number = f"{year}{month:02d}{day:02d}-{random_part}"
    invoice_number = f"{day:02d}{month:02d}{year}{random_part}"
    return invoice_number

class Payment(models.Model):
    PAY_STATUS = [
        ('Unpaid', 'Unpaid'),
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        
    ]
    owner = models.ForeignKey(Register, on_delete=models.CASCADE)
    date_paid = models.DateTimeField(auto_now_add=True)
    month_paid = models.DateField()
    pay_status = models.CharField(max_length=7, choices=PAY_STATUS)
    status = models.BooleanField(default=False)
    due_months = models.IntegerField(default=0) 
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    collected_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=20, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '%s %s %s %s %s %s %s'% (self.owner.owner.name, self.owner.room.room_number, self.owner.room.amount,  self.due_months, self.balance, self.month_paid, self.collected_by) 
    
    def save(self, *args, **kwargs):
        # Check if it's the first payment and owner.reg_status is True
        if self.owner.reg_status and Payment.objects.filter(owner=self.owner).count() == 0:
            self.month_paid = self.owner.start_date + relativedelta(months=1)
            self.due_months = 0
        else:
            # Get the last payment made by the owner
            last_payment = Payment.objects.filter(owner=self.owner).order_by('-date_paid').first()
            if last_payment:
                last_month_paid = last_payment.month_paid
                if self.owner.reg_status:
                    self.month_paid = last_month_paid + relativedelta(months=1)
                    self.due_months = (date.today() - self.month_paid).days // 30
                else:
                    self.month_paid = last_month_paid + relativedelta(months=1)
                    self.due_months = (self.owner.end_date - self.month_paid).days // 30

        #created_by = request.user 
        #pay_status = 'Paid'
        # Generate invoice number
        self.invoice_number = generate_invoice_number()
        # Calculate the balance
        date_now = date.today()
        self.due_months = date_now.month - self.month_paid.month + 12 * (date_now.year - self.month_paid.year)
        self.balance = self.owner.room.amount * self.due_months
        """
        # Check if the balance is below zero and raise a ValidationError if it is
        if self.balance < 1500:
            raise ValidationError("Balance cannot be negative")
"""
        super(Payment, self).save(*args, **kwargs)

class Receiver(models.Model):
    collector = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='collector')
    amount_received = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    reference_number = models.CharField(max_length=20, unique=True)
    received_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver')
    date_received = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return '%s %s %s'% (self.collector, self.note, self.received_by, self.date_received)
     
    def save(self, *args, **kwargs):
        # Generate a unique reference number before saving
        if not self.reference_number:
            self.reference_number = self.generate_reference_number()
        super().save(*args, **kwargs)

    def generate_reference_number(self):
        # Implement your logic to generate a unique reference number
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        #invoice_number = f"{year}{month:02d}{day:02d}-{random_part}"
        reference_number = f"{day:02d}{month:02d}{year}{random_part}"
        return reference_number
    
    # def save(self, *args, **kwargs):
    #     if not self.reference_number:
    #         self.reference_number = get_random_string(length=10).upper()
    #     super().save(*args, **kwargs)

class Arreas(models.Model):
    pass
