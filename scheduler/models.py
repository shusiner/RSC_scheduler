from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
import datetime
from calendar import monthrange
from django.template.defaultfilters import slugify

# Create your models here.

class User(AbstractUser):
    is_guard = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)




class Guard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    site = models.ForeignKey('Site', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    age = models.CharField(max_length=200, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    position = models.CharField(max_length=200, blank=True)
    shift = models.CharField(max_length=200, blank=True)
    last_active = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(null= True)

    gender_type = (('m', 'male'), ('f', 'female'), )

    gender = models.CharField(
        max_length=1,
        choices=gender_type,
        blank=True,
        default='m',
        help_text='gender',
    )

    # Foreign Key used because guard can only have one manager, but manager can have multiple guards
    # Manager as a string rather than object because it hasn't been declared yet in the file.

    def test2(self):
        yr = datetime.datetime.now().date().year
        mth = datetime.datetime.now().date().month
        num = monthrange(yr, mth)[1]
        dt = datetime.date(yr,mth,1)
        for i in range(num):
            a = dt + datetime.timedelta(i)
            if(self.date.month == mth):
                break
            Date.objects.create(date = a)
        return reverse('home')

    def save(self, *args, **kwargs):
        yr = datetime.datetime.now().date().year
        mth = datetime.datetime.now().date().month
        num = monthrange(yr, mth)[1]
        dt = datetime.date(yr,mth,1)
        schedule = Schedule.objects.filter(guard=self).order_by('date')
        schedule = schedule.last()
        for i in range(num):
            e = dt + datetime.timedelta(i)
            if(schedule):
                if(schedule.date.month == mth):
                    break
            #if (e.date - dt).days>=0:
            Schedule.objects.create(guard=self, date = e)
        self.slug = slugify(self.name)
        super(Guard, self).save(*args, **kwargs) # Call the real save() method

    def get_absolute_url(self):
        """Returns the url to access a detail record for this site."""
        return reverse('guard_detail', args=[str(self.slug)])

    def update(self):
        """Returns the url to update a particular author instance."""
        return reverse('guard_update', args=[str(self.slug)])

    def delete1(self):
        """Returns the url to update a particular author instance."""
        return reverse('guard_delete', args=[str(self.slug)])

    def delete(self, *args, **kwargs):
        self.user.delete()                # When user is deleted, guard is deleted on cascade
        #super().delete(*args, **kwargs)  # Call the "real" delete() method.


    def __str__(self):
        """String for representing the Model object."""
        return self.user.username

    class Meta:
        permissions = (("guard_view", "Guard View"),)


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200, help_text='Enter your name:')

    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
    class Meta:
        permissions = (("manager_view", "Manager View"),)


class Site(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    slug = models.SlugField(null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this site."""
        return reverse('site_detail', args=[str(self.slug)])

    def update(self):
        """Returns the url to update a particular author instance."""
        return reverse('site_update', args=[str(self.slug)])

    def delete1(self):
        """Returns the url to update a particular author instance."""
        return reverse('site_delete', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Site, self).save(*args, **kwargs) # Call the real save() method




class Schedule(models.Model):
    date = models.DateField(null=True, blank=True)
    slug = models.SlugField(null=True)
    
    is_day = models.BooleanField(default=False)
    is_night = models.BooleanField(default=False)

    guard = models.ForeignKey('Guard', on_delete=models.CASCADE)

    def __str__(self):
        """String for representing the Model object."""
        return self.date.strftime('%b. %d, %Y')

    def str1(self):
        return self.date.strftime('%d/%m')

    def month(self):
        return self.date.month
    
    def day(self):
        return self.date.day

    def update(self):
        """Returns the url to update a particular author instance."""
        return reverse('schedule_update', args=[str(self.slug)])

    def delete1(self):
        """Returns the url to update a particular author instance."""
        return reverse('schedule_delete', args=[str(self.slug)])

    def get_absolute_url(self):
        """Returns the url to access a detail record for this site."""
        return reverse('schedule_detail', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        temp = slugify(self.date)
        self.slug = slugify(self.guard.name+" "+str(temp))
        super(Schedule, self).save(*args, **kwargs) # Call the real save() method

    