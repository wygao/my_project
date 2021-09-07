#-*coding:utf8
from django.db import models
from django.contrib.auth.models import User

class ProUser(models.Model):
    user = models.OneToOneField(User)
    tel = models.CharField(max_length=20,verbose_name=u'联系方式')
    addr = models.CharField(max_length=50,verbose_name=u'派送地址')
    QQ  = models.CharField(max_length=15,null=True,blank=True,verbose_name=u'QQ')

class Goods(models.Model):
    name       = models.CharField(max_length=20)
    price      = models.FloatField() 
    img        = models.FileField(upload_to="./goodsImg/") 
    category   = models.ForeignKey("Category") 
    def __unicode__(self):
        return self.name

class Category(models.Model):
    category_name = models.CharField(max_length=20)
    p_category    = models.ForeignKey("self",null=True,blank=True)
    def __unicode__(self):
        return self.category_name


'''
class ShopCar(models.Model):
    line_item  = models.ManyToManyField('LineItem')  
    user  = models.ForeignKey(User) 
    def __unicode__(self):
        return self.user.username 
    

    def add_item(self, item):
        line_item.add(item)

    def del_item(self, item):
        line_item

class LineItem(models.Model):  
    good = models.ForeignKey(Good)
    goods_quantity = models.IntegerField()
    def __unicode__(self):
        return self.goods 
'''











