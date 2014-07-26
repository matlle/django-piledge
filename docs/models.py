from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.conf import settings
import subprocess, uuid



class Doc(models.Model):
    doc_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, editable=False)
    doc_title = models.CharField(max_length=100)
    doc_description = models.TextField()
    doc_created_at = models.DateTimeField('Createa at', auto_now_add=True)
    doc_file_name = models.FileField(upload_to="uploads/docs/pdf", max_length=1024)
    doc_slug = models.SlugField(
        verbose_name = _(u'Slug'),
        help_text = _(u'The unique uri component for this commentary'),
        max_length = 255,
        unique = True,
        default = 0,
        editable = False
    )
    doc_thumbnail = models.ImageField(
        upload_to = 'uploads/docs/pdf/thumbnails/',
        max_length = 2024,
        editable=False
    )

    doc_nb_comment = models.IntegerField(default=0, editable=False)

    class Meta:
        db_table = 'docs'


    def save(self):
        self.doc_slug = slugify(self.doc_title)
        thumbnail = "uploads/docs/pdf/thumbnails/%s_%s_%s.png" % ("thumbnail",self.doc_slug, uuid.uuid1().hex,)
        self.doc_thumbnail = thumbnail
        super(Doc, self).save()


    def __unicode__(self):
        return self.doc_title



def doc_post_save(sender, instance=False, **kwargs):
    doc = Doc.objects.get(pk=instance.pk)
    command = "convert -quality 95 -thumbnail 222 -resize 150x200 %s%s[0] %s%s" % (settings.MEDIA_ROOT, doc.doc_file_name, settings.MEDIA_ROOT, doc.doc_thumbnail)

    proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
    stdout_value = proc.communicate()[0]

post_save.connect(doc_post_save, sender=Doc)




class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    doc = models.ForeignKey(Doc)
    author = models.ForeignKey(User)
    comment_body = models.TextField(blank=True, null=True)
    comment_created_at = models.DateTimeField('comment created at', auto_now_add=True)

    class Meta:
        db_table = 'comments'
    
    def __unicode__(self):
        return self.comment_body




class UserProfile(models.Model):
    avatar = models.ImageField("Profile Pic", upload_to="upload/images/users/", blank=True, null=True)
    docs = models.IntegerField(default=0)
    user = models.OneToOneField(User, related_name="profile")
    
    class Meta:
        db_table = 'user_profile'

    def __unicode__(self):
        return self.user

    def increment_docs(self):
        self.docs += 1
        self.save()

    def avatar_image(self):
        return MEDIA_URL + self.avatar.name if self.avatar else None



