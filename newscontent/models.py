from django.db import models

from django.contrib.auth.models import User

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(blank=True,verbose_name ='e-mail')

    def __str__(self):
        return u'%s %s' % (self.first_name, self.last_name)

class Newscontent(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField(blank=True, null=True)
    content_type = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

class SiteUser(models.Model):
        
    ## required to associate Author model with User model (Important)
    user = models.OneToOneField(User, null=True, blank=True)

    ## additional fields
    phone = models.IntegerField(blank=True, default=0)    
    activation_key = models.CharField(max_length=255, default=1)
    activation_key2 = models.CharField(max_length=255, default=1)
    zipper = models.CharField(max_length=5, default=1)
    email_validated = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('post_by_author', args=[self.user.username])

class ZipCodes(models.Model):
    id = models.CharField(max_length=5, blank=True, null=False,primary_key=True,default='0')
    zipcode = models.CharField(max_length=5, blank=True, null=True)
    zip_class = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'zip_codes'
