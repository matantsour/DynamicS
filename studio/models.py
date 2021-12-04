from django import urls
from django.core import validators
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.deletion import CASCADE


from django.urls import reverse
# Create your models here.


class User_Type(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_type = models.ForeignKey(User_Type, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    dob = models.DateField(max_length=8)
    dor = models.DateField(max_length=8)  # date of registration
    organization = models.CharField(max_length=100)

    def __str__(self):
        return "-".join([self.fname+" "+self.lname, self.id, self.user_type])


class Employee(models.Model):
    u_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    title = models.CharField(max_length=100)
    wage_method = models.IntegerChoices(
        'Hourly', 'Per_Project', 'Dynamic', 'Monthly', 'Unknown')
    wage = models.FloatField()
    date_of_start = models.DateField(max_length=8)

    def __str__(self):
        return "-".join([self.u_id.fname+" "+self.u_id.lname, self.id, self.title, self.u_id.user_type])


class Login_Details(models.Model):
    u_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    email = models.EmailField(max_length=254)
    # read more how to apply as a password in forms.py
    password = models.CharField(max_length=50)

    def __str__(self):
        return "-".join([self.u_id, self.email, self.password])

##


class WorkingHour(models.Model):
    id = models.AutoField(primary_key=True)
    u_id=models.ForeignKey(User,on_delete=CASCADE)
    working_date=models.DateField()
    stime=models.TimeField()
    etime=models.TimeField()

    def __str__(self):
        return self.type


class Status(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class Status(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class File(models.Model):
    id = models.AutoField(primary_key=True)
    urls = models.URLField(max_length=300)
    file_creation_date=models.DateField()

    def __str__(self):
        return self.type


class Album(models.Model):
    id = models.AutoField(primary_key=True)
    album_name = models.CharField(max_length=100)
    release_date=models.DateField()
    size=models.IntegerField()
    length=models.FloatField()

    def __str__(self):
        return "-".join([self.id, self.album_name])


class Creation(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.CharField(max_length=100)
    creation_date=models.DateField()
    creator = models.CharField(max_length=100)
    album_id=models.ForeignKey(Album,on_delete=CASCADE)
    current_file = models.ForeignKey(File, null=True, blank=True, on_delete=models.SET_NULL)
    previous_file=models.ForeignKey(File, null=True, blank=True, on_delete=models.SET_NULL)
    profit=models.FloatField()

    def __str__(self):
        return self.type


class Resource(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    unit_cost=models.FloatField()

    def __str__(self):
        return self.type


class Phase(models.Model):
    id = models.AutoField(primary_key=True)
    creation_id = models.ForeignKey(Creation,on_delete=CASCADE)
    creation_id = models.ForeignKey(Creation,on_delete=CASCADE)
    status=models.ForeignKey(Status,on_delete=models.SET_NULL)
    placement=models.IntegerField()
    name=models.CharField(max_length=100)
    resources = models.ManyToManyField(Resource, through='Phase_Resources')

    def __str__(self):
        return self.type


class Phase_Resources(models.Model):
    phase = models.ForeignKey(Phase,on_delete=CASCADE)
    resource = models.ForeignKey(Resource,on_delete=CASCADE)
    resource_quantity = models.FloatField()

    def __str__(self):
        return "-".join([self.phase, self.resource, self.resource_quantity])


class Meeting(models.Model):
    id = models.AutoField(primary_key=True)
    phase_id=models.ForeignKey(Phase,on_delete=CASCADE)
    attendees=models.ManyToManyField(User)
    start_date=models.DateField()
    end_date=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    #https://djangotricks.blogspot.com/2019/10/working-with-dates-and-times-in-forms.html
    


    def __str__(self):
        return self.type


class File_Deletion_History(models.Model):
    id = models.AutoField(primary_key=True)
    creation_id = models.models.ForeignKey(Creation, on_delete=models.CASCADE)
    phase_id = models.models.ForeignKey(Phase, on_delete=models.CASCADE)
    deletion_date = models.DateField()
