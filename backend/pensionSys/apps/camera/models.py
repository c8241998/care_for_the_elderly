from django.db import models

# Create your models here.
class stranger_log(models.Model):

    id = models.AutoField(primary_key=True)

    gender = models.CharField(max_length=100)

    upper_wear_fg  = models.CharField(max_length=100)

    cellphone  = models.CharField(max_length=100)

    orientation  = models.CharField(max_length=100)

    headwear  = models.CharField(max_length=100)

    age  = models.CharField(max_length=100)

    glasses  = models.CharField(max_length=100)

    bag  = models.CharField(max_length=100)

    upper_wear_texture  = models.CharField(max_length=100)

    lower_wear  = models.CharField(max_length=100)

    upper_color  = models.CharField(max_length=100)

    time = models.DateTimeField(auto_now_add=True)

    def get_path(model,filename):
        return 'stranger_log/%s.jpg' % (model.id)

    picture = models.ImageField(upload_to=get_path, blank=True, null=True)

    def __str__(self):
        dir = {}
        dir['id'] = self.id
        dir['gender'] = self.gender
        dir['upper_wear_fg'] = self.upper_wear_fg
        dir['cellphone'] = self.cellphone
        dir['orientation'] = self.orientation
        dir['headwear'] = self.headwear
        dir['age'] = self.age
        dir['glasses'] = self.glasses
        dir['bag'] = self.bag
        dir['upper_wear_texture'] = self.upper_wear_texture
        dir['lower_wear'] = self.lower_wear
        dir['upper_color'] = self.upper_color
        dir['time'] = self.time.__str__()
        dir['photo'] = "../media/stranger_log/"+self.id.__str__()+".jpg"
        return dir

class area_log(models.Model):

    id = models.AutoField(primary_key=True)

    gender = models.CharField(max_length=100)

    upper_wear_fg  = models.CharField(max_length=100)

    cellphone  = models.CharField(max_length=100)

    orientation  = models.CharField(max_length=100)

    headwear  = models.CharField(max_length=100)

    age  = models.CharField(max_length=100)

    glasses  = models.CharField(max_length=100)

    bag  = models.CharField(max_length=100)

    upper_wear_texture  = models.CharField(max_length=100)

    lower_wear  = models.CharField(max_length=100)

    upper_color  = models.CharField(max_length=100)

    time = models.DateTimeField(auto_now_add=True)

    def get_path(model,filename):
        return 'area_log/%s.jpg' % (model.id)

    picture = models.ImageField(upload_to=get_path, blank=True, null=True)

    def __str__(self):
        dir = {}
        dir['id'] = self.id
        dir['gender'] = self.gender
        dir['upper_wear_fg'] = self.upper_wear_fg
        dir['cellphone'] = self.cellphone
        dir['orientation'] = self.orientation
        dir['headwear'] = self.headwear
        dir['age'] = self.age
        dir['glasses'] = self.glasses
        dir['bag'] = self.bag
        dir['upper_wear_texture'] = self.upper_wear_texture
        dir['lower_wear'] = self.lower_wear
        dir['upper_color'] = self.upper_color
        dir['time'] = self.time.__str__()
        dir['photo'] = "../media/area_log/"+self.id.__str__()+".jpg"
        return dir

class emotion_log(models.Model):

    id = models.AutoField(primary_key=True)

    elder = models.CharField(max_length=100)

    label = models.CharField(max_length=100)

    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        dir = {}
        dir['id'] = self.id
        dir['elder'] = self.elder
        dir['label'] = self.label
        dir['time'] = self.time.__str__()
        dir['photo'] = "../media/emotion_log/"+self.id.__str__()+".jpg"
        return dir

class fall_log(models.Model):

    id = models.AutoField(primary_key=True)

    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        dir = {}
        dir['id'] = self.id
        dir['time'] = self.time.__str__()
        dir['photo'] = "../media/fall_log/"+self.id.__str__()+".jpg"
        return dir

class interaction_log(models.Model):

    id = models.AutoField(primary_key=True)

    time = models.DateTimeField(auto_now_add=True)

    volunteer = models.CharField(max_length=100)

    elder = models.CharField(max_length=100)

    def __str__(self):
        dir = {}
        dir['id'] = self.id
        dir['volunteer'] = self.volunteer
        dir['elder'] = self.elder
        dir['time'] = self.time.__str__()
        dir['photo'] = "../media/interaction_log/"+self.id.__str__()+".jpg"
        return dir