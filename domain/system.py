from django.core.cache import cache
from domain.models import User,Jump
from django.utils.deprecation import MiddlewareMixin
import dns.resolver

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



"""更新redis"""
class FuncMiddleware:
    def UserModel(self):
        userlist=User.objects.all().filter(is_superuser=False)
        """用户列表及目标"""
        cache.set("userdata",userlist,60 * 5)
        return {"data": 0}


    def JumpModel(self):
        """单独目标"""
        jumplist = Jump.objects.all()
        cache.set("jumpdata", jumplist, 60 * 5)
        return {"data":0}



class Permission:
    """权限判定"""
    def is_permiss(self,request):
        if request.user.is_authenticated:
            if not request.user.is_superuser:
                pathlist=["/shop/tbsearch/mainindexdata/","/shop/tbsearch/mainindex/","/shop/tbsearch/parentlogin/"]
                if request.path in pathlist:
                    return 'error'
                else:
                    pass

class ModeUrlA:
    @staticmethod
    def publicdomain(record_list,domain):
        cacheuserdata=cache.get('userdata')
        cachejumpdata=cache.get('jumpdata')
        for mm in record_list:
            userone=cacheuserdata.filter(username=mm).first()
            if userone is not None:
                if userone.mode=="1":
                    return userone.target
                elif userone.mode=="2":
                    jumpone=cachejumpdata.filter(name=domain).first()
                    if jumpone is not None:
                        return userone.target
        return "error"

    @classmethod
    def showdomain(cls,request):
        # domain = request.META.get('HTTP_HOST', "unknown")
        domain="www.baidu.com"
        list_url = domain.strip().split('.')
        if list_url[0] != "www":
            domain = "www." + domain
        cachejumpdata = cache.get('jumpdata')
        is_jump_url=cachejumpdata.filter(name=domain).first()
        if is_jump_url is not None:
            if is_jump_url.jumptarget != None and is_jump_url.is_jump==True:
                return is_jump_url.jumptarget
        try:
            A = dns.resolver.query(domain, 'A')
        except Exception as e:
            return "error"
        record_list=[]
        for ii in A.response.answer:
            record_list.append(str(ii[0])[0:-1])
        resdata = ModeUrlB.publicdomain(record_list,domain)
        # print(resdata)
        return resdata

class ModeUrlB:
    @staticmethod
    def publicdomain(record_list,domain):
        cacheuserdata=cache.get('userdata')
        cachejumpdata=cache.get('jumpdata')
        for mm in record_list:
            userone=cacheuserdata.filter(username=mm).first()
            if userone is not None:
                if userone.mode=="1":
                    return userone.target
                elif userone.mode=="2":
                    jumpone=cachejumpdata.filter(name=domain).first()
                    if jumpone is not None:
                        return userone.target
        return "error"


    @classmethod
    def showdomain(cls,request):
        domain = request.META.get('HTTP_HOST', "unknown")
        domain_url = request.META.get('HTTP_REFERER', 'unknown')
        domain = str(domain_url)[7:][:-1]
        list_url = domain.strip().split('.')
        if list_url[0] != "www":
            domain = "www." + domain
        cachejumpdata = cache.get('jumpdata')
        is_jump_url=cachejumpdata.filter(name=domain).first()
        if is_jump_url is not None:
            if is_jump_url.jumptarget != None and is_jump_url.is_jump==True:
                return is_jump_url.jumptarget
        try:
            A = dns.resolver.query(domain, 'A')
        except Exception as e:
            return "error"
        record_list=[]
        for ii in A.response.answer:
            record_list.append(str(ii[0])[0:-1])
        resdata = ModeUrlB.publicdomain(record_list,domain)
        # print(resdata)
        return resdata

class ModeUrlC:
    @staticmethod
    def publicdomain(record_list,domain):
        cacheuserdata=cache.get('userdata')
        cachejumpdata=cache.get('jumpdata')
        for mm in record_list:
            userone=cacheuserdata.filter(username=mm).first()
            if userone is not None:
                if userone.mode=="1":
                    return userone.target
                elif userone.mode=="2":
                    jumpone=cachejumpdata.filter(name=domain).first()
                    if jumpone is not None:
                        return userone.target
        return "error"


    @classmethod
    def showdomain(cls,request):
        domain_url = request.META.get('HTTP_REFERER',"unknown")
        if domain_url=="unknown":
            domain = request.META.get('HTTP_HOST', "unknown")
            if domain=="unknown":
                return "error"
        else:
            domain = str(domain_url)[7:][:-1]
        list_url = domain.strip().split('.')
        if list_url[0] != "www":
            domain = "www." + domain
        cachejumpdata = cache.get('jumpdata')
        is_jump_url=cachejumpdata.filter(name=domain).first()
        if is_jump_url is not None:
            if is_jump_url.jumptarget != None and is_jump_url.is_jump==True:
                return is_jump_url.jumptarget
        try:
            A = dns.resolver.query(domain, 'A')
        except Exception as e:
            return "error"
        record_list=[]
        for ii in A.response.answer:
            record_list.append(str(ii[0])[0:-1])
        resdata = ModeUrlB.publicdomain(record_list,domain)
        # print(resdata)
        return resdata
