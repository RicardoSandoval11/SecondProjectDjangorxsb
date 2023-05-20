from django.db import models
#
from model_utils.models import TimeStampedModel
from ckeditor_uploader.fields import RichTextUploadingField
#
from applications.users.models import User, Interest
from .managers import EntryManager, CategoryManager

class Category(models.Model):

    name = models.CharField(
        max_length=100,
        verbose_name='Category name',
        unique=True,
        blank=False
    )
    description = models.TextField(
        verbose_name='Category description'
    )

    objects = CategoryManager()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return str(self.id)+' - '+self.name
    
class Tag(models.Model):

    name = models.CharField(
        verbose_name='Tag name',
        unique=True,
        blank=False,
        max_length=50
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
    
    def __str__(self):
        return str(self.id)+' - '+self.name

class Entry(TimeStampedModel):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Author'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Category'
    )
    title = models.CharField(max_length=100, verbose_name='Entry title', unique=True)
    tags = models.ManyToManyField(Tag, verbose_name='Tags')
    summary = models.TextField(verbose_name='Summary', blank=False)
    content = RichTextUploadingField('Content')
    public = models.BooleanField()
    image = models.ImageField(
        verbose_name='Image',
        upload_to='Entry'
    )
    interests = models.ManyToManyField(Interest, verbose_name='Interests')

    objects = EntryManager()

    class Meta:
        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'
    
    def __str__(self):
        return str(self.id) +' - '+self.title




