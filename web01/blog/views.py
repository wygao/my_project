#-*coding:utf8
from django.http import HttpResponse
from django.shortcuts import render_to_response,render
from blog.models import ProUser,Goods,Category
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django import forms
from django.http import HttpResponseRedirect
#from django.utils import json

class RegistUserForm(forms.ModelForm):
    username = forms.CharField(label=u'用户名')
    password = forms.CharField(label=u'口令',widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','password') 

class RegistProUserForm(forms.ModelForm):
    class Meta:
        model = ProUser
        fields = ('tel','addr','QQ')

def index(req):
    goods_list    = Goods.objects.all()   #显示所有商品
    category_list = Category.objects.all() 
    categorys     = [category for category in category_list if category.p_category is None]

    goodlist = req.session.get('goodlist')
    if req.user.is_authenticated():
        return render(req,"index.html",{'user':req.user,'goods_list':goods_list,'categorys':categorys, 'goodlist':goodlist})
    else:
        return render(req,"index.html",{'goods_list':goods_list,'categorys':categorys, 'goodlist':goodlist})

def regist_user(req):
    if req.method == "POST":
        rf1 = RegistUserForm(req.POST)
        rf2 = RegistProUserForm(req.POST)
        if rf1.is_valid() and rf2.is_valid():
            rf1.instance.is_staff = True
            rf1.instance.set_password(rf1.cleaned_data['password'])
            rf1.save()
            rf2.instance.user = rf1.instance 
            rf2.save()
            return HttpResponse("<h2>亲,你已经注册成功了哦!<br />到首页<b>登寻</b>找宝贝去吧~~</h2>")
    else:
        rf1 = RegistUserForm()
        rf2 = RegistProUserForm()
    return render(req,'regist.html',{'rf1':rf1,'rf2':rf2})
    
def login_user(req):
    username = req.POST.get('username')
    password = req.POST.get('password')
    user = authenticate(username=username,password=password)
    if user is not None:
        #print user.username 
        login(req,user)
        return HttpResponse(username)
    else:
        return HttpResponseRedirect('/index/')

def disp_goods(req):
    goodlist      = req.session.get("goodlist")
    category_list = Category.objects.all() 
    categorys     = [category for category in category_list if category.p_category is None]   #取得一级目录,即,最上层.
    type_id       = req.GET.get("type_id")
    goods_type    = Category.objects.get(id=type_id) 
    goods_list    = goods_type.goods_set.all()   #一种类型所对应的商品.
    return render(req,"index.html",{'categorys':categorys,'goods_list':goods_list,'goodlist':goodlist})

def buy_goods(req):
    goodlist = req.POST.get("goodlist")
    exec "goodlist = %s"%goodlist        # 经过计算对json字符串进行python 转化.
    '''
    for item  in goodlist:
        goods_id = item["goods_id"]
        goods    = Goods.objects.get(id=goods_id)
        ShopCar.objects.create(goods=goods user= )
        '''
    req.session['goodlist'] = goodlist    #  设置session .
    return HttpResponse("ok")

def order(req):
    goodlist = req.session.get("goodlist")
    if req.user.is_authenticated():
        return render(req,"order.html",{'user':req.user,'goodlist':goodlist})
def pay(req):
    if req.user.is_authenticated():
        return render_to_response("pay.html",{'user':req.user})

def logout_user(req):
    logout(req)    
    return HttpResponse("亲,下次再见哦!")

def contact(req):
	return render_to_response('contact.html',{})







'''
class ShopCar(object):  
    def __init__(self, *args, **kwargs):  
        self.items = []  
        self.total_price = 0  
    def add_product(self,product):  
        self.total_price += goods.price  
        for item in self.items:  
            if item.goods.id == goods.id:  
                item.quantity += 1   
                return  
        self.items.append(LineItem(product=product,goods_price=goods.price,quantity=1))
'''



   
