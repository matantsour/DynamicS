
from django import urls
from django.core import validators
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.deletion import CASCADE


from django.urls import reverse
# Create your models here.


class User_Type(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_type = models.ForeignKey(User_Type, on_delete=models.CASCADE,related_name='users')
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=12, blank=True)
    dob = models.DateField(max_length=8, blank=True, null=True)
    dor = models.DateField(max_length=8, blank=True, null=True,
                           editable=False, auto_now_add=True)  # date of registration
    organization = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return "-".join([self.fname, self.lname, self.user_type.type])


class Employee(models.Model):
    u_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,related_name="employee"
    )
    title = models.CharField(max_length=100)
    WAGE_METHOD_CHOICES = [
        ('1', 'Hourly'),
        ('2', 'Monthly'),
        ('3', 'Flexible'),
        ('4', 'Per Project'),
        ('5', 'Unknown'),
    ]
    wage_method = models.CharField(
        max_length=1,
        choices=WAGE_METHOD_CHOICES,
        default='Hourly',
    )
    wage = models.FloatField()
    date_of_start = models.DateField(max_length=8)

    def __str__(self):
        return "-".join([self.u_id.fname+" "+self.u_id.lname, self.title, self.u_id.user_type.type])


class Login_Details(models.Model):
    u_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,related_name="login_details"
    )
    email = models.EmailField(max_length=254)
    # read more how to apply as a password in forms.py
    password = models.CharField(max_length=50)

    def __str__(self):
        return "-".join([self.u_id.fname, self.u_id.lname, self.email])

##


class WorkingHour(models.Model):
    id = models.AutoField(primary_key=True)
    e_id = models.ForeignKey(Employee, on_delete=CASCADE,related_name="working_hours")
    working_date = models.DateField()
    stime = models.TimeField()
    etime = models.TimeField()

    def __str__(self):
        return " | ".join([str(i) for i in [self.e_id, self.working_date, self.stime, self.etime]])


class Status(models.Model):
    id = models.AutoField(primary_key=True)
    desc = models.CharField(max_length=100)

    def __str__(self):
        return self.desc





class Album(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,unique=True)
    release_date = models.DateField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True, editable=False)
    length = models.FloatField(blank=True, null=True, editable=False)

    def __str__(self):
        return "-".join([self.name])


class Creation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,default='')
    creator = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,related_name="creations")
    creation_date = models.DateField(blank=True, null=False, auto_now_add=True)
    album_id = models.ForeignKey(
        Album, null=True, blank=True, on_delete=models.SET_NULL,related_name="creations")
    profit = models.FloatField()
    def __str__(self):
        crtor = self.creator.fname+" "+self.creator.lname
        return "-".join([self.name, crtor])

    def get_last_phase(self):
        try:
            inner_qs=Creation.objects.filter(id=self.id)
            phases=list(Phase.objects.filter(creation_id__in=inner_qs))
            last_phase=phases[-1]
            last_phase_placement=last_phase.placement
            return last_phase_placement
        except:
            return 0
    class Meta:
        unique_together = ('name', 'creator',)






class Resource(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    unit_cost = models.FloatField()

    def __str__(self):
        return self.name


class Phase(models.Model):
    phase_id=models.CharField(db_column='phase_id',max_length=10,blank=True,primary_key=True,editable=False)
    #id = models.AutoField(blank=True)
    #id = models.IntegerField(blank=True,null=True)
    creation_id = models.ForeignKey(Creation, on_delete=models.CASCADE,related_name="phases")
    status = models.ForeignKey(Status, on_delete=models.CASCADE,default=1,related_name="phases")
    placement = models.IntegerField(blank=True,editable=False)
    name = models.CharField(max_length=100)
    resources = models.ManyToManyField(
        Resource, null=False, blank=True, through='Phase_Resources') #no related name yet

    def __str__(self):
        return "-".join([self.creation_id.name,str(self.placement),self.name, self.status.desc])
    
    def save(self, *args, **kwargs):
        self.placement=int(self.creation_id.get_last_phase())+1
        self.phase_id = str(self.creation_id.id)+"_"+str(self.placement)
        super(Phase,self).save(*args, **kwargs)

        class Meta:
            managed = False
            db_table = 'phase_id'


class Phase_Resources(models.Model):
    phase = models.ForeignKey(Phase,to_field='phase_id', on_delete=CASCADE)
    resource = models.ForeignKey(Resource, on_delete=CASCADE)
    resource_quantity = models.FloatField()

    def __str__(self):
        return "-".join([str(self.phase.phase_id), self.resource.name, str(self.resource_quantity)])

class File(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField(max_length=300)
    file_creation_date = models.DateField(
        null=False, blank=True, editable=False, auto_now=True)
    creation = models.ForeignKey(
        Creation, null=True, blank=True, on_delete=models.SET_NULL,related_name="files")
    def __str__(self):
        return str(self.file_creation_date)+"|"+self.url

class Meeting(models.Model):
    id = models.AutoField(primary_key=True)
    phase_id = models.ForeignKey(Phase,to_field='phase_id', on_delete=CASCADE,related_name="meetings")
    attendees = models.ManyToManyField(User,related_name="meetings") #no related name yet
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    topic = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    # https://djangotricks.blogspot.com/2019/10/working-with-dates-and-times-in-forms.html

    def __str__(self):
        attendees_number = str(len(list(self.attendees.all())))+" attendees"
        return "-".join([str(i) for i in [self.topic, self.start_date, self.start_time, attendees_number]])


class File_Deletion_History(models.Model):
    id = models.AutoField(primary_key=True)
    creation_id = models.ForeignKey(Creation, on_delete=models.CASCADE,related_name="deleted_files")
    url = models.URLField(max_length=300, blank=True, null=False)
    deletion_date = models.DateField(
        auto_now=True, editable=False, null=False, blank=True)

    def __str__(self):
        return "-".join([str(self.id), str(self.creation_id.name), str(self.phase_id.name)])
