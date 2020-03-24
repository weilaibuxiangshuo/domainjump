#-*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import View
from .models import (User,Jump)
from django.http import JsonResponse,QueryDict
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required
from django.utils.deprecation import MiddlewareMixin
from django.utils.decorators import method_decorator
from domain.system import (FuncMiddleware,ModeUrlA,ModeUrlB,ModeUrlC,Permission)
from django.core.cache import cache
import random,json,math,re


class IsMiddleware(MiddlewareMixin):
    def process_request(self,request):
        cacheuserdata=cache.get('userdata','')
        cachejumpdata=cache.get('jumpdata','')
        if cacheuserdata=="":
            mainmiddleware=FuncMiddleware()
            mainmiddleware.UserModel()
        if cachejumpdata=="":
            mainmiddleware=FuncMiddleware()
            mainmiddleware.JumpModel()


class IsDomain(MiddlewareMixin):
    def process_request(self, request):
        perpath=Permission().is_permiss(request)
        if perpath=="error":
            return HttpResponse(status=403)
        else:
            pass
        """方式A"""
        request_url=request.path
        # print(request_url)
        pattern = re.compile(r'.*/shop/tbsearch/.*')
        mm=pattern.findall(request_url)
        # print(mm)
        if len(mm)!=0:
            pass
        else:
            """方式A"""
            #resdata = ModeUrlA().showdomain(request)
            resdata = ModeUrlC().showdomain(request)
            """方式B"""
            # resdata = ModeUrlB().showdomain(request)
            if resdata=="error":
                return HttpResponse(status=403)
            else:
                #print(resdata)
                return redirect(resdata)

class ParentLogin(View):
    def get(self,request):
        # userone=User.objects.create_superuser(username="parentadmin",password="parentpython123",is_staff=True,is_active=True,is_superuser=True)
        return render(request, 'parentlogin.html')

    def post(self,request):
        username=request.POST.get('username','')
        password=request.POST.get('password','')
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            if user.is_superuser:
                return redirect('/shop/tbsearch/mainindex/')
            else:
                return redirect('/shop/tbsearch/index/')
        else:
            return redirect('/shop/tbsearch/parentlogin/')


class ParentData(View):
    def delete(self,request):
        del_data=QueryDict(request.body)
        res=del_data.get('data','')
        User.objects.filter(username=res).delete()
        mainmiddleware = FuncMiddleware()
        mainmiddleware.UserModel()
        mainmiddleware.JumpModel()
        return JsonResponse({"code":0})



class Login(View):
    def get(self,request):
        return render(request, 'login.html')

    def post(self,request):
        username = request.POST.get('username', '')
        user = authenticate(username=username, password=username)
        if user and not user.is_superuser:
            login(request, user)
            if int(user.mode)==3:
                return redirect('/shop/tbsearch/jumpindex/')
            else:
                return redirect('/shop/tbsearch/index/')
        else:
            return redirect('/shop/tbsearch/login/')

@method_decorator(login_required(login_url='/shop/tbsearch/login/'),name='dispatch')
class Index(View):
    def get(self,request):
        return render(request,'index.html',{'data':request.user.username})

@method_decorator(login_required(login_url='/shop/tbsearch/login/'),name='dispatch')
class IndexData(View):
    """显示对应地址"""
    def get(self,request):
        setuser=request.GET.get('setuser','')
        if setuser =="":
            user_one = User.objects.filter(is_superuser=False).filter(username=request.user.username).first()
        else:
            user_one = User.objects.filter(is_superuser=False).filter(username=setuser).first()
        if user_one is not None:
            if user_one.mode == "3":
                temp = user_one.jump_target.all().filter(jumptarget__isnull=False,is_jump=True)
            else:
                temp = user_one.jump_target.all()
            dataPagination = pagination(temp, request)
            tempdata = dataPagination.control()
            if tempdata is None:
                return render(request, 'error.html')
            data = []
            for i in tempdata:
                if user_one.mode=="3":
                    target_temp=i.jumptarget
                else:
                    target_temp=user_one.target
                dict = {"id": i.id, "username": i.name, "target": target_temp}
                data.append(dict)
            surplus = int(user_one.number) - int(temp.count())
            defaultData = {
                "usercount": user_one.number,
                "userurl": user_one.target,
                "surplus": surplus,
                "usermode": user_one.mode,
                "code": 0,
                "msg": "",
                "count": temp.count(),
            }
            defaultData.update({"data": data})
            return JsonResponse(defaultData)
        defaultData = {
            "code": 0,
            "msg": "",
            "count": 0,
        }
        return JsonResponse(defaultData)

    def post(self,request):
        """添加对应数目"""
        data=request.POST.get('data','')
        if data == "" or data is None:
            return JsonResponse({'code':0})
        else:
            data=json.loads(data)
            url_list=str(data[0]).strip().split("\n")
            for url_temp_one in url_list:
                res=url_temp_one.split(".")
                if len(res)>2:
                    url_temp="".join(["www.",res[1],".",res[2]])
                    url_temp=url_temp.strip()
                else:
                    url_temp_one = "www."+url_temp_one
                    url_temp=url_temp_one.strip()
                url_temp=url_temp.strip()
                url_one=Jump.objects.filter(name=url_temp).first()
                if url_one is None:
                    user_one = User.objects.filter(username=data[1]).first()
                    if user_one is not None:
                        """判断是否超出条件"""
                        temporary=int(user_one.number)-len(user_one.jump_target.all())
                        if temporary !=0 and temporary > 0:
                            if user_one.mode=="5":
                                Jump.objects.create(name=url_temp, jumptarget=user_one.target,is_jump=True,relationship=user_one)
                            else:
                                Jump.objects.create(name=url_temp,relationship=user_one)
                            mainmiddleware = FuncMiddleware()
                            mainmiddleware.UserModel()
                            mainmiddleware.JumpModel()
                        else:
                            return JsonResponse({'code': "添加失败已达数目上限"})
                    else:
                        return JsonResponse({'code': 0})
                else:
                    return JsonResponse({'code': 0})
            return JsonResponse({'code': 0})

    def delete(self,request):
        del_data=QueryDict(request.body)
        res=del_data.get('data','')
        print(res,'ppp')
        Jump.objects.filter(id=res).delete()
        mainmiddleware = FuncMiddleware()
        mainmiddleware.UserModel()
        mainmiddleware.JumpModel()
        return JsonResponse({"code":0})

@method_decorator(login_required(login_url='/shop/tbsearch/login/'),name='dispatch')
class MainIndex(View):
    def get(self,request):
        user_list=User.objects.filter(is_superuser=False)
        return render(request,'main.html',{"data":user_list})


@method_decorator(login_required(login_url='/shop/tbsearch/login/'),name='dispatch')
class MainIndexData(View):
    def get(self,request):
        user_id=request.GET.get('data',[])
        if len(user_id)!=0:
            user_one=User.objects.filter(is_superuser=False).filter(id=user_id).first()
            if user_one is not None:
                #print(user_one)
                temp=user_one.jump_target.all()
                dataPagination = pagination(temp, request)
                tempdata = dataPagination.control()
                if tempdata is None:
                    return render(request, 'error.html')
                data = []
                for i in tempdata:
                    dict = {"id": i.id, "username": i.name,"target":user_one.target}
                    data.append(dict)
                surplus=int(user_one.number)-int(temp.count())
                defaultData = {
                    "usercount":user_one.number,
                    "userurl":user_one.target,
                    "surplus":surplus,
                    "usermode":user_one.mode,
                    "code": 0,
                    "msg": "",
                    "count": temp.count(),
                }
                defaultData.update({"data": data})
                return JsonResponse(defaultData)
        defaultData = {
            "usercount": 0,
            "userurl":"" ,
            "surplus":0 ,
            "usermode": 0,
            "code": 0,
            "msg": "",
            "count": 0,
        }
        return JsonResponse(defaultData)

    def post(self,request):
        """添加用户与更新用户"""
        data=request.POST.get('data','')
        if data == "" or data is None:
            return JsonResponse({'code':0})
        else:
            data=json.loads(data)
            user_one=User.objects.filter(username=data[0]).first()
            if user_one is None:
                User.objects.create_user(username=data[0],password=data[0],is_staff=True,is_active=True,target=data[1],mode=data[2],number=int(data[3]))
                mainmiddleware = FuncMiddleware()
                mainmiddleware.UserModel()
                mainmiddleware.JumpModel()
            else:
                user_one.mode=data[2]
                user_one.target=data[1]
                user_one.number=data[3]
                user_one.save()
                mainmiddleware = FuncMiddleware()
                mainmiddleware.UserModel()
                mainmiddleware.JumpModel()
            off_mode = User.objects.filter(username=data[0]).first()
            if off_mode is not None:
                if off_mode.mode=="3" or off_mode.mode=="5":
                    off_mode.jump_target.all().update(jumptarget=off_mode.target,is_jump=True)
                else:
                    off_mode.jump_target.all().update(jumptarget=None, is_jump=False)
            else:
                pass
            return JsonResponse({'code': 0})

    def delete(self,request):
        del_data=QueryDict(request.body)
        res=del_data.get('data','')
        if res != "":
            res=json.loads(res)
            #print(res)
            for i in res:
                Jump.objects.filter(id=i).delete()
        mainmiddleware = FuncMiddleware()
        mainmiddleware.UserModel()
        mainmiddleware.JumpModel()
        return JsonResponse({"code":0})


@method_decorator(login_required(login_url='/shop/tbsearch/login/'),name='dispatch')
class CreateMain(View):
    def get(self,request):
        return render(request,'createmain.html')

@method_decorator(login_required(login_url='/shop/tbsearch/login/'),name='dispatch')
class CreateIndex(View):
    def get(self,request):
        return render(request,'createindex.html')

@method_decorator(login_required(login_url='/shop/tbsearch/login/'),name='dispatch')
class EditMain(View):
    def get(self,request):
        return render(request,'editmain.html')


@method_decorator(login_required(login_url='/shop/tbsearch/login/'),name='dispatch')
class JumpIndex(View):
    def get(self,request):
        return render(request,'jump.html',{'data':request.user.username})

@method_decorator(login_required(login_url='/shop/tbsearch/login/'),name='dispatch')
class JumpIndexData(View):
    """显示对应地址"""
    def get(self,request):
        setuser = request.GET.get('setuser', '')
        if setuser == "":
            user_one = User.objects.filter(is_superuser=False).filter(username=request.user.username).first()
        else:
            user_one = User.objects.filter(is_superuser=False).filter(username=setuser).first()
        if user_one is not None:
            temp = user_one.jump_target.all().filter(is_jump=True)
            dataPagination = pagination(temp, request)
            tempdata = dataPagination.control()
            if tempdata is None:
                return render(request, 'error.html')
            data = []
            for i in tempdata:
                dict = {"id": i.id, "username": i.name, "target": i.jumptarget}
                data.append(dict)
            surplus = int(user_one.number) - int(temp.count())
            defaultData = {
                "usercount": user_one.number,
                "userurl": user_one.target,
                "surplus": surplus,
                "usermode": user_one.mode,
                "code": 0,
                "msg": "",
                "count": temp.count(),
            }
            defaultData.update({"data": data})
            return JsonResponse(defaultData)
        defaultData = {
            "code": 0,
            "msg": "",
            "count": 0,
        }
        return JsonResponse(defaultData)

    def post(self,request):
        """
        添加对应数目
        data[0]:内容
        data[1]:用户
        data[2]:目标
        """
        data=request.POST.get('data','')
        if data == "" or data is None:
            return JsonResponse({'code':0})
        else:
            data=json.loads(data)
            url_list=str(data[0]).strip().split("\n")
            target_one=str(data[2]).strip()
            for url_temp_one in url_list:
                res=url_temp_one.split(".")
                if len(res)>2:
                    url_temp = "".join(["www.", res[1], ".", res[2]])
                    url_temp=url_temp.strip()
                else:
                    url_temp_one = "www." + url_temp_one
                    url_temp = url_temp_one.strip()
                url_temp=url_temp.strip()
                url_one=Jump.objects.filter(name=url_temp).first()
                if url_one is None:
                    user_one = User.objects.filter(username=data[1]).first()
                    if user_one is not None:
                        """判断是否超出条件"""
                        temporary=int(user_one.number)-len(user_one.jump_target.all().filter(is_jump=True))
                        if temporary !=0 and temporary > 0:
                            Jump.objects.create(name=url_temp,jumptarget=target_one,is_jump=True,relationship=user_one)
                            mainmiddleware = FuncMiddleware()
                            mainmiddleware.UserModel()
                            mainmiddleware.JumpModel()
                        else:
                            return JsonResponse({'code': "添加失败已达数目上限"})
                    else:
                        return JsonResponse({'code': 0})
                else:
                    return JsonResponse({'code': 0})
            return JsonResponse({'code': 0})

    def delete(self,request):
        del_data=QueryDict(request.body)
        res=del_data.get('data','')
        Jump.objects.filter(id=res).delete()
        mainmiddleware = FuncMiddleware()
        mainmiddleware.UserModel()
        mainmiddleware.JumpModel()
        return JsonResponse({"code":0})


@method_decorator(login_required(login_url='/shop/tbsearch/login/'),name='dispatch')
class CreateJump(View):
    def get(self,request):
        return render(request,'createjump.html')





class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('/shop/tbsearch/login/')

#分页
class pagination:
    def __init__(self,*args,**kwargs):
        self.args=args[0]
        self.total=args[0].count()
        self.data=args[1]
        self.page=0
        self.limit=0

    def control(self):
        try:
            self.page=int(self.data.GET['page'])
            self.limit=int(self.data.GET['limit'])
        except:
            return None
        if self.page>math.ceil(self.total/self.limit) or self.limit > self.total:
            self.page=1
        slice=self.args[(self.page-1)*self.limit:self.page*self.limit]
        return slice
