from django.db import models


# Create your models here.
class elder(models.Model):

    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=10)

    phone = models.CharField(max_length=11)

    birthday = models.CharField(max_length=50)

    gender=models.CharField(max_length=5)

    id_card = models.CharField(max_length=30)

    fam_name = models.CharField(max_length=30)

    fam_phone = models.CharField(max_length=11)

    def get_photo_path(model,filename):
        return 'elder_photo/%s.jpg' % (model.id)

    photo = models.ImageField(upload_to=get_photo_path, blank=True, null=True)



    def __str__(self):
        dir = {}
        dir['id'] = self.id
        dir['name'] = self.name
        dir['phone'] = self.phone
        dir['photo'] = "elder_photo/"+self.id.__str__()+".jpg"
        dir['birthday'] = self.birthday.__str__()
        dir['id_card'] = self.id_card
        dir['gender'] = self.gender
        dir['fam_name'] = self.fam_name
        dir['fam_phone'] = self.fam_phone
        return dir