from django.db import models

# Create your models here.


class Firmware(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,null=True,unique=True)

    class Meta:
        db_table = 'firmware'

    def __unicode__(self):
        return "id:%s | name:%s" % (self.id,self.name)


class Service(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,null=True)
    version = models.CharField(max_length=10)
    firmware = models.ForeignKey(Firmware, on_delete=models.CASCADE)

    class Meta:
        db_table = 'service'

    def __unicode__(self):
        return 'service:%s | version:%s' % (self.name,self.version)

class Cve(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    des = models.CharField(max_length=400)
    cvss3 = models.FloatField(max_length=5)
    cvss2 = models.FloatField(max_length=5)
    service = models.ForeignKey(Service,on_delete=models.CASCADE)

    class Meta:
        db_table = 'cve'

    def __unicode__(self):
        return 'cve:%s | des:%s' % (self.id,self.des)