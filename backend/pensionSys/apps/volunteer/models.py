from django.db import models


# Create your models here.
class volunteer(models.Model):

    id = models.AutoField(primary_key=True)

    name = models.CharField(
        max_length=10
    )

    phone = models.CharField(max_length=11)

    def get_photo_path(model,filename):
        return 'volunteer_photo/%s.jpg' % (model.id)

    photo = models.ImageField(upload_to=get_photo_path, blank=True, null=True)

    birthday = models.CharField(max_length=50)

    gender = models.CharField(max_length=5)

    id_card = models.CharField(max_length=30)

    visitdate = models.CharField(max_length=50)

    def __str__(self):
        dir = {}
        dir['id'] = self.id
        dir['name'] = self.name
        dir['phone'] = self.phone
        dir['photo'] = "volunteer_photo/"+self.id.__str__()+".jpg"
        dir['birthday'] = self.birthday.__str__()
        dir['id_card'] = self.id_card
        dir['gender'] = self.gender
        dir['visitdate'] = self.visitdate.__str__()
        return dir