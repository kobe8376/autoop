# -*- encoding: utf-8 -*-
from django.shortcuts import render, render_to_response
from models import webuser
from django.http.response import HttpResponse
from django.shortcuts import redirect
from forms import teacher_form,student_form
import time
from app.models import sappinfo,Tappinfo
from sftpmethod import getversion,dosendapp,viapp
import re
from django.forms.formsets import INITIAL_FORM_COUNT


# Create your views here.
def login(request):
    request.session['username'] = None
    request.session['privilege'] = None
    dic = {'status':''}
    if request.method == 'POST':
        print ('get post')
        user = request.POST.get('username',None)
        pwd = request.POST.get('password',None)
        print (user,pwd)
        result = webuser.objects.filter(username=user,password=pwd).count()
        print (result)
        if result != 1:
            dic = {'status':'错误的用户名或者密码'}
        else:
            userpriv = webuser.objects.filter(username=user).values_list('privileges')[0][0]
            print userpriv
            if userpriv == 1:
                request.session['username'] = user
                userinformation = webuser.objects.get(username=user)
                print userinformation
                request.session['privilege'] = userinformation.privileges
                print (request.session)
                return redirect('/getuser/')
            elif userpriv == 2:
                request.session['username'] = user
                userinformation = webuser.objects.get(username=user)
                request.session['privilege'] = userinformation.privileges
                return redirect('/normaluser/')
            else:
                return redirect('/login/')
    return render_to_response('login.html',dic)
    
def normaluser(request):
    privi = request.session.get('privilege',None)
    uname = request.session.get('username',None)
    tcurpage = int(request.GET.get('tcurpage',1))
    tallpage = int(request.GET.get('tallpage',1))
    tpagetype = str(request.GET.get('tpagetype',''))
    scurpage = int(request.GET.get('scurpage',1))
    sallpage = int(request.GET.get('sallpage',1))
    spagetype = str(request.GET.get('spagetype',''))
    app_limit = 5
    if privi == 2:
        tappcount = Tappinfo.objects.count()
        sappcount = sappinfo.objects.count()
        tallpage = divmod(tappcount, app_limit)[0]
        tremind = divmod(tappcount, app_limit)[1]
        print tappcount,tallpage,tremind
        if tremind > 0:
            tallpage += 1
        if tpagetype == 'pageup':
            tcurpage -= 1
        if tpagetype == 'pagedown':
            tcurpage += 1
        tstartapp = (tcurpage - 1)*app_limit
        tendapp = tstartapp + app_limit
        
        sallpage = divmod(sappcount, app_limit)[0]
        sremind = divmod(sappcount, app_limit)[1]
        print sappcount,tallpage,sremind
        if sremind > 0:
            sallpage += 1
        if spagetype == 'pageup':
            scurpage -= 1
        if spagetype == 'pagedown':
            scurpage += 1
        sstartapp = (scurpage - 1)*app_limit
        sendapp = sstartapp + app_limit
        sappinfo_list = sappinfo.objects.all().order_by("-id")[sstartapp:sendapp]
        tappinfo_list = Tappinfo.objects.all().order_by("-id")[tstartapp:tendapp]  
        date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        Tform = teacher_form(initial={'Tdate':date})
        Sform = student_form(initial={'Sdate':date})
        Udic = {'student_form':Sform,'teacher_form':Tform,'sappinfo_list':sappinfo_list,'tappinfo_list':tappinfo_list,'uname':uname,'tcurpage':tcurpage,'tallpage':tallpage,'tpagetype':tpagetype,'scurpage':scurpage,'sallpage':sallpage,'spagetype':spagetype,'tstatus':'','sstatus':''}
        if request.method == 'POST':
            Tform = teacher_form(request.POST,request.FILES)
            Sform = student_form(request.POST,request.FILES)
            print (Sform)
            print (Tform)
            if Tform.is_valid():
                Tver = Tform.cleaned_data['Tversion']
                if re.match('^(\d+)\.(\d+)\.(\d+)',Tver):
                    Td = Tform.cleaned_data['Tdate']
                    Teacker_uploaded_file(request.FILES['Tfile'],Tver,Td)
                    print ('Tok')
                else:
                    Tform = teacher_form(initial={'Tdate':date})
                    Sform = student_form(initial={'Sdate':date})
                    Udic = {'student_form':Sform,'teacher_form':Tform,'sappinfo_list':sappinfo_list,'tappinfo_list':tappinfo_list,'uname':uname,'tcurpage':tcurpage,'tallpage':tallpage,'tpagetype':tpagetype,'scurpage':scurpage,'sallpage':sallpage,'spagetype':spagetype,'tstatus':'版本号只能使用数字.数字.数字的格式，如2.4.1','sstatus':''}
            if Sform.is_valid():
                Sver = Sform.cleaned_data['Sversion']
                if re.match('^(\d+)\.(\d+)\.(\d+)',Sver):
                    Sd = Sform.cleaned_data['Sdate']
                    Student_uploaded_file(request.FILES['Sfile'],Sver,Sd)
                    print('Sok')
                else:
                    Tform = teacher_form(initial={'Tdate':date})
                    Sform = student_form(initial={'Sdate':date})
                    Udic = {'student_form':Sform,'teacher_form':Tform,'sappinfo_list':sappinfo_list,'tappinfo_list':tappinfo_list,'uname':uname,'tcurpage':tcurpage,'tallpage':tallpage,'tpagetype':tpagetype,'scurpage':scurpage,'sallpage':sallpage,'spagetype':spagetype,'tstatus':'','sstatus':'版本号只能使用数字.数字.数字的格式，如2.4.1'}
#        else:
#            Tform = teacher_form(initial={'Tdate':date})
#            Sform = student_form(initial={'Sdate':date})
            
        return render_to_response('normaluserform.html',Udic) 
    else:
        return redirect('/login/')
def user(request):
    app_limit = 5
    privi = request.session.get('privilege',None)
    uname = request.session.get('username',None)
    tcurpage = int(request.GET.get('tcurpage',1))
    tallpage = int(request.GET.get('tallpage',1))
    tpagetype = str(request.GET.get('tpagetype',''))
    scurpage = int(request.GET.get('scurpage',1))
    sallpage = int(request.GET.get('sallpage',1))
    spagetype = str(request.GET.get('spagetype',''))
    print (privi,uname)
    if privi == 1:
        tappcount = Tappinfo.objects.count()
        sappcount = sappinfo.objects.count()
        tallpage = divmod(tappcount, app_limit)[0]
        tremind = divmod(tappcount, app_limit)[1]
        print tappcount,tallpage,tremind
        if tremind > 0:
            tallpage += 1
        if tpagetype == 'pageup':
            tcurpage -= 1
        if tpagetype == 'pagedown':
            tcurpage += 1
        tstartapp = (tcurpage - 1)*app_limit
        tendapp = tstartapp + app_limit
        
        sallpage = divmod(sappcount, app_limit)[0]
        sremind = divmod(sappcount, app_limit)[1]
        print sappcount,tallpage,sremind
        if sremind > 0:
            sallpage += 1
        if spagetype == 'pageup':
            scurpage -= 1
        if spagetype == 'pagedown':
            scurpage += 1
        sstartapp = (scurpage - 1)*app_limit
        sendapp = sstartapp + app_limit
        sappinfo_list = sappinfo.objects.all().order_by("-id")[sstartapp:sendapp]
        tappinfo_list = Tappinfo.objects.all().order_by("-id")[tstartapp:tendapp]  
        date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        Tform = teacher_form(initial={'Tdate':date})
        Sform = student_form(initial={'Sdate':date})
        Udic = {'student_form':Sform,'teacher_form':Tform,'sappinfo_list':sappinfo_list,'tappinfo_list':tappinfo_list,'uname':uname,'tcurpage':tcurpage,'tallpage':tallpage,'tpagetype':tpagetype,'scurpage':scurpage,'sallpage':sallpage,'spagetype':spagetype,'tstatus':'','sstatus':''}
        tdel = request.POST.get('tdel',None)
        sdel = request.POST.get('sdel',None)
        if request.method == 'POST':
            if tdel != None:
                Tappinfo.objects.filter(id=tdel).delete()
                return redirect('/user/')
            elif sdel != None:
                sappinfo.objects.filter(id=sdel).delete()
                return redirect('/user/')
            else:
                Tform = teacher_form(request.POST,request.FILES)
                Sform = student_form(request.POST,request.FILES)
                print (Sform)
                print (Tform)
                if Tform.is_valid():
                    Tver = Tform.cleaned_data['Tversion']
                    if re.match('^(\d+)\.(\d+)\.(\d+)',Tver):
                        Td = Tform.cleaned_data['Tdate']
                        Teacker_uploaded_file(request.FILES['Tfile'],Tver,Td)
                        print ('Tok')
                    else:
                        Tform = teacher_form(initial={'Tdate':date})
                        Sform = student_form(initial={'Sdate':date})                       
                        Udic = {'student_form':Sform,'teacher_form':Tform,'sappinfo_list':sappinfo_list,'tappinfo_list':tappinfo_list,'uname':uname,'tcurpage':tcurpage,'tallpage':tallpage,'tpagetype':tpagetype,'scurpage':scurpage,'sallpage':sallpage,'spagetype':spagetype,'tstatus':'版本号只能使用数字.数字.数字的格式，如2.4.1','sstatus':''}
                if Sform.is_valid():
                    Sver = Sform.cleaned_data['Sversion']
                    if re.match('^(\d+)\.(\d+)\.(\d+)',Sver):
                        Sd = Sform.cleaned_data['Sdate']
                        Student_uploaded_file(request.FILES['Sfile'],Sver,Sd)
                        print('Sok') 
                    else:
                        Tform = teacher_form(initial={'Tdate':date})
                        Sform = student_form(initial={'Sdate':date})                       
                        Udic = {'student_form':Sform,'teacher_form':Tform,'sappinfo_list':sappinfo_list,'tappinfo_list':tappinfo_list,'uname':uname,'tcurpage':tcurpage,'tallpage':tallpage,'tpagetype':tpagetype,'scurpage':scurpage,'sallpage':sallpage,'spagetype':spagetype,'tstatus':'','sstatus':'版本号只能使用数字.数字.数字的格式，如2.4.1'}
        else:
            Tform = teacher_form(initial={'Tdate':date})
            Sform = student_form(initial={'Sdate':date})
            
        return render_to_response('userform.html',Udic)
    else:
        return redirect('/login/')


def Teacker_uploaded_file(f,d,s):
    path = "/upload/"
    f.name = 'LekeTeacher_' + d + '.apk'
    file_name = path + f.name
    addfilename = f.name
    addversion = d
    adddate = s
    print(adddate)
    addpath = file_name
    adds = Tappinfo(filename=addfilename,version=addversion,createdate=adddate,filepath=addpath)    
    adds.save()
    destination = open(file_name, 'wb+')
    print (file_name)
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    
def Student_uploaded_file(f,d,s):
    path = "/upload/"
    f.name = 'LekeStudent_' + d + '.apk'
    file_name = path + f.name
    addfilename = f.name
    addversion = d
    adddate = s
    print(adddate)
    addpath = file_name
    adds = sappinfo(filename=addfilename,version=addversion,createdate=adddate,filepath=addpath)
    adds.save()
    destination = open(file_name, 'wb+')
    print (file_name)
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


def getuser(request):
    user_limit = 5
    privi = request.session.get('privilege',None)
    uname = request.session.get('username',None)
    curpage = int(request.GET.get('curpage',1))
    allpage = int(request.GET.get('allpage',1))
    pagetype = str(request.GET.get('pagetype',''))
    if privi == 1:
        print curpage
        print(curpage,allpage,pagetype)
        if pagetype == 'pagedown':
            curpage += 1
        elif pagetype == 'pageup':
            curpage -= 1
        startpos = (curpage -1)* user_limit
        endpos = startpos + user_limit
        if curpage == 1 and allpage == 1:
            allpostcounts = webuser.objects.count()
            allpage = allpostcounts / user_limit
            remainpost = allpostcounts % user_limit
            if remainpost > 0:
                allpage += 1
        user_list = webuser.objects.all().order_by("-id")[startpos:endpos]
        dic = {'userdata':user_list,'status':'','uname':uname,'allpage':allpage,'curpage':curpage}
        result = render_to_response('admin.html',dic)
        if request.method == 'POST' :
            deleteid =  request.POST.get('dat',None)
            if deleteid != None:
                print deleteid
                webuser.objects.get(id=deleteid).delete()
                return redirect('/getuser/')
            adduser = request.POST.get('adduser',None)
            addpwd = request.POST.get('addpwd',None)
            addprivi = int(request.POST.get('addprivi',None))
            print addprivi
            result = webuser.objects.filter(username=adduser).count()
            if result == 0 and adduser is not None:
                usertable = webuser(username=adduser,password=addpwd,privileges=addprivi)
                usertable.save()
                return redirect('/getuser/')
            
            else:
                dic = {'userdata':user_list,'status':'该用户已存在','allpage':allpage,'curpage':curpage}
                return render_to_response('admin.html',dic)
        return result
    else:
        return redirect('/login/')
    
def usersend(request):
    app_limit = 5
    privi = request.session.get('privilege',None)
    uname = request.session.get('username',None)
    tcurpage = int(request.GET.get('tcurpage',1))
    tallpage = int(request.GET.get('tallpage',1))
    tpagetype = str(request.GET.get('tpagetype',''))
    scurpage = int(request.GET.get('scurpage',1))
    sallpage = int(request.GET.get('sallpage',1))
    spagetype = str(request.GET.get('spagetype',''))
    tappcount = Tappinfo.objects.count()
    sappcount = sappinfo.objects.count()
    tallpage = divmod(tappcount, app_limit)[0]
    tremind = divmod(tappcount, app_limit)[1]
    print tappcount,tallpage,tremind
    if tremind > 0:
        tallpage += 1
    if tpagetype == 'pageup':
        tcurpage -= 1
    if tpagetype == 'pagedown':
        tcurpage += 1
    tstartapp = (tcurpage - 1)*app_limit
    tendapp = tstartapp + app_limit
    
    sallpage = divmod(sappcount, app_limit)[0]
    sremind = divmod(sappcount, app_limit)[1]
    print sappcount,tallpage,sremind
    if sremind > 0:
        sallpage += 1
    if spagetype == 'pageup':
        scurpage -= 1
    if spagetype == 'pagedown':
        scurpage += 1
    sstartapp = (scurpage - 1)*app_limit
    sendapp = sstartapp + app_limit
    
    
    host2='192.168.200.35'
    username1='zhangsongbin'
    password1='zhangsongbin#16888'
    comm1='cat  /opt/mobilegateway/conf/mysvr.conf | grep VERSION_0 | awk -F \'=\' \'{print $2}\''
    comm2='cat  /opt/mobilegateway/conf/mysvr.conf | grep VERSION_1 | awk -F \'=\' \'{print $2}\''
    getold = getversion()
    sshd = getold.ssh_connect(host2,username1,password1,comm1,comm2)
    sftpd = getold.sftp_open(sshd)
    oldsver = sshd[0][0].split()[0]
    oldtver = sshd[1][0].split()[0]
    if privi == 1:
        sappinfo_list = sappinfo.objects.all().order_by("-id")[sstartapp:sendapp]
        tappinfo_list = Tappinfo.objects.all().order_by("-id")[tstartapp:tendapp]
        sendappdic = {'sappinfo_list':sappinfo_list,'tappinfo_list':tappinfo_list,'uname':uname,'oldsver':oldsver,'oldtver':oldtver,'tcurpage':tcurpage,'tallpage':tallpage,'tpagetype':tpagetype,'scurpage':scurpage,'sallpage':sallpage,'spagetype':spagetype}
        if request.method == 'POST':
            tsendoldver = request.POST.get('oldtver',None)
            tsendfile = request.POST.get('tsendfile',None)
            tsenddate = request.POST.get('tsenddate',None)
            tsendver = request.POST.get('tsendver',None)
            ssendfile = request.POST.get('ssendfile',None)
            ssenddate = request.POST.get('ssenddate',None)
            ssendver = request.POST.get('ssendver',None)
            ssendoldver = request.POST.get('oldsver',None)

            if ssendfile == None and ssenddate == None and ssendver == None:
                print ("do teacher")
                tsendapp = dosendapp()
                tviapp17=viapp()
                tviapp35=viapp()
                day = tsenddate
                host1='192.168.200.17'
                host2='192.168.200.35'
                usernamex='zhangsongbin'
                passwordx='zhangsongbin#16888'
                passwordx1='zhangsongbin#16888'
                tversion=tsendver
                toldtversion=tsendoldver
                comm1='sudo mv /var/www/html/exSchool/zongxian/appcenter/3/LekeTeacher_'+ toldtversion +'.apk /var/www/html/exSchool/zongxian/appcenter/3/LekeTeacher_'+ toldtversion +'.apk$(date +%Y-%m-%d).backup'
                comm2='sudo sed -i \'s/VERSION_1='+ toldtversion +'/VERSION_1='+ tversion + '/g\' /opt/mobilegateway/conf/mysvr.conf'
                comm3='sudo sed -i \'s/LekeTeacher_'+ toldtversion +'/LekeTeacher_' + tversion +'/g\' /opt/mobilegateway/conf/mysvr.conf'
                comm4='sudo sed -i \'24 s/^.*$/        "version":"' + tversion + '",/g\' /var/www/html/exSchool/zongxian/appcenter.php'
                comm5='sudo sed -i \'32 s/^.*$/        "updateDate":"' + day + '",/g\' /var/www/html/exSchool/zongxian/appcenter.php'
                comm6='sudo sed -i \'34 s/' + toldtversion + '/' + tversion + '/g\' /var/www/html/exSchool/zongxian/appcenter.php'
                comm8='sudo sh /opt/mobilegateway/start.sh'
                comm7='sudo kill -9 `ps -ef|grep mbgsvr|grep -v grep|awk \'{print $2}\'` '
                comm9='sudo mv /tmp/LekeTeacher_'+ tversion +'.apk /var/www/html/exSchool/zongxian/appcenter/3/LekeTeacher_'+ tversion +'.apk'
                comm10='sudo chmod 777 /var/www/html/exSchool/zongxian/appcenter/3/LekeTeacher_'+ tversion +'.apk'
                tcommd17 = [comm1,comm4,comm5,comm6,comm9,comm10]
                tcommd35 = [comm2,comm3,comm7,comm8]
                tsshd = tsendapp.ssh_connect(host1,usernamex,passwordx)
                tsftpd = tsendapp.sftp_open(tsshd)
                tsendapp.sftp_up(tsftpd,'/upload/LekeTeacher_' + tversion + '.apk','/tmp/LekeTeacher_' + tversion + '.apk')
                #tsendapp.sftp_close(tsshd)               
                for docommd17 in tcommd17:
                    tsshv17=tviapp17.ssh_connect(host1,usernamex,passwordx1,docommd17)
                    tviapp17.ssh_close(tsshv17)
                    print docommd17
                for docommd35 in tcommd35:
                    tsshv35=tviapp35.ssh_connect(host2,usernamex,passwordx,docommd35)
                    tviapp35.ssh_close(tsshv35)
                    print docommd35                                 
                return redirect('/usersend/')
            elif tsendfile == None and tsenddate == None and tsendver == None:
                print ('do student')
                ssendapp = dosendapp()
                sviapp17=viapp()
                sviapp35=viapp()
                day = ssenddate
                host1='192.168.200.17'
                host2='192.168.200.35'
                usernamex='zhangsongbin'
                passwordx='zhangsongbin#16888'
                passwordx1='zhangsongbin#16888'
                sversion=ssendver
                soldsversion=ssendoldver
                comm1='sudo mv /var/www/html/exSchool/zongxian/appcenter/4/LekeStudent_'+ soldsversion +'.apk /var/www/html/exSchool/zongxian/appcenter/4/LekeStudent_'+ soldsversion +'.apk$(date +%Y-%m-%d).backup'
                comm2='sudo sed -i \'s/VERSION_0='+ soldsversion +'/VERSION_0=' + sversion + '/g\' /opt/mobilegateway/conf/mysvr.conf'
                comm3='sudo sed -i \'s/LekeStudent_'+ soldsversion +'/LekeStudent_' + sversion +'/g\' /opt/mobilegateway/conf/mysvr.conf'
                comm4='sudo sed -i \'41 s/^.*$/        "version":"' + sversion + '",/g\' /var/www/html/exSchool/zongxian/appcenter.php'
                comm5='sudo sed -i \'49 s/^.*$/        "updateDate":"' + day + '",/g\' /var/www/html/exSchool/zongxian/appcenter.php'
                comm6='sudo sed -i \'51 s/' + soldsversion + '/' + sversion + '/g\' /var/www/html/exSchool/zongxian/appcenter.php'
                comm8='sudo sh /opt/mobilegateway/start.sh'
                comm7='sudo kill -9 `ps -ef|grep mbgsvr|grep -v grep|awk \'{print $2}\'` '
                comm9='sudo mv /tmp/LekeStudent_'+ sversion +'.apk /var/www/html/exSchool/zongxian/appcenter/4/LekeStudent_'+ sversion +'.apk'
                comm10='sudo chmod 777 /var/www/html/exSchool/zongxian/appcenter/4/LekeStudent_'+ sversion +'.apk'
                scommd17 = [comm1,comm4,comm5,comm6,comm9,comm10]
                scommd35 = [comm2,comm3,comm7,comm8]
                ssshd = ssendapp.ssh_connect(host1,usernamex,passwordx)
                ssftpd = ssendapp.sftp_open(ssshd)
                ssendapp.sftp_up(ssftpd,'/upload/LekeStudent_' + sversion + '.apk','/tmp/LekeStudent_' + sversion + '.apk')
                #tsendapp.sftp_close(ssshd)  
                for docommd17 in scommd17:
                    ssshv17=sviapp17.ssh_connect(host1,usernamex,passwordx1,docommd17)
                    sviapp17.ssh_close(ssshv17)
                for docommd35 in scommd35:
                    ssshv35=sviapp35.ssh_connect(host2,usernamex,passwordx,docommd35)
                    sviapp35.ssh_close(ssshv35)
                return redirect('/usersend/')
        return render_to_response('usersend.html',sendappdic)
    else:
        return redirect('/login/')

def normalusersend(request):
    app_limit = 5
    privi = request.session.get('privilege',None)
    uname = request.session.get('username',None)
    tcurpage = int(request.GET.get('tcurpage',1))
    tallpage = int(request.GET.get('tallpage',1))
    tpagetype = str(request.GET.get('tpagetype',''))
    scurpage = int(request.GET.get('scurpage',1))
    sallpage = int(request.GET.get('sallpage',1))
    spagetype = str(request.GET.get('spagetype',''))
    tappcount = Tappinfo.objects.count()
    sappcount = sappinfo.objects.count()
    tallpage = divmod(tappcount, app_limit)[0]
    tremind = divmod(tappcount, app_limit)[1]
   
    if tremind > 0:
        tallpage += 1
    if tpagetype == 'pageup':
        tcurpage -= 1
    if tpagetype == 'pagedown':
        tcurpage += 1
    tstartapp = (tcurpage - 1)*app_limit
    tendapp = tstartapp + app_limit
    
    sallpage = divmod(sappcount, app_limit)[0]
    sremind = divmod(sappcount, app_limit)[1]
    
    if sremind > 0:
        sallpage += 1
    if spagetype == 'pageup':
        scurpage -= 1
    if spagetype == 'pagedown':
        scurpage += 1
    sstartapp = (scurpage - 1)*app_limit
    sendapp = sstartapp + app_limit
    
    
    host2='192.168.200.35'
    username1='zhangsongbin'
    password1='zhangsongbin#16888'
    comm1='cat  /opt/mobilegateway/conf/mysvr.conf | grep VERSION_0 | awk -F \'=\' \'{print $2}\''
    comm2='cat  /opt/mobilegateway/conf/mysvr.conf | grep VERSION_1 | awk -F \'=\' \'{print $2}\''
    getold = getversion()
    sshd = getold.ssh_connect(host2,username1,password1,comm1,comm2)
    sftpd = getold.sftp_open(sshd)
    oldsver = sshd[0][0].split()[0]
    oldtver = sshd[1][0].split()[0]
    if privi == 2:
        sappinfo_list = sappinfo.objects.all().order_by("-id")[sstartapp:sendapp]
        tappinfo_list = Tappinfo.objects.all().order_by("-id")[tstartapp:tendapp]
        sendappdic = {'sappinfo_list':sappinfo_list,'tappinfo_list':tappinfo_list,'uname':uname,'oldsver':oldsver,'oldtver':oldtver,'tcurpage':tcurpage,'tallpage':tallpage,'tpagetype':tpagetype,'scurpage':scurpage,'sallpage':sallpage,'spagetype':spagetype}
        if request.method == 'POST':
            tsendoldver = request.POST.get('oldtver',None)
            tsendfile = request.POST.get('tsendfile',None)
            tsenddate = request.POST.get('tsenddate',None)
            tsendver = request.POST.get('tsendver',None)
            ssendfile = request.POST.get('ssendfile',None)
            ssenddate = request.POST.get('ssenddate',None)
            ssendver = request.POST.get('ssendver',None)
            ssendoldver = request.POST.get('oldsver',None)
            if ssendfile == None and ssenddate == None and ssendver == None:
                print ("do teacher")
                tsendapp = dosendapp()
                tviapp17=viapp()
                tviapp35=viapp()
                day = tsenddate
                host1='192.168.200.17'
                host2='192.168.200.35'
                usernamex='zhangsongbin'
                passwordx='zhangsongbin#16888'
                passwordx1='zhangsongbin#16888'
                tversion=tsendver
                toldtversion=tsendoldver
                comm1='sudo mv /var/www/html/exSchool/zongxian/appcenter/3/LekeTeacher_'+ toldtversion +'.apk /var/www/html/exSchool/zongxian/appcenter/3/LekeTeacher_'+ toldtversion +'.apk$(date +%Y-%m-%d).backup'
                comm2='sudo sed -i \'s/VERSION_1='+ toldtversion +'/VERSION_1='+ tversion + '/g\' /opt/mobilegateway/conf/mysvr.conf'
                comm3='sudo sed -i \'s/LekeTeacher_'+ toldtversion +'/LekeTeacher_' + tversion +'/g\' /opt/mobilegateway/conf/mysvr.conf'
                comm4='sudo sed -i \'24 s/^.*$/        "version":"' + tversion + '",/g\' /var/www/html/exSchool/zongxian/appcenter.php'
                comm5='sudo sed -i \'32 s/^.*$/        "updateDate":"' + day + '",/g\' /var/www/html/exSchool/zongxian/appcenter.php'
                comm6='sudo sed -i \'34 s/' + toldtversion + '/' + tversion + '/g\' /var/www/html/exSchool/zongxian/appcenter.php'
                comm8='sudo sh /opt/mobilegateway/start.sh'
                comm7='sudo kill -9 `ps -ef|grep mbgsvr|grep -v grep|awk \'{print $2}\'` '
                comm9='sudo mv /tmp/LekeTeacher_'+ tversion +'.apk /var/www/html/exSchool/zongxian/appcenter/3/LekeTeacher_'+ tversion +'.apk'
                comm10='sudo chmod 777 /var/www/html/exSchool/zongxian/appcenter/3/LekeTeacher_'+ tversion +'.apk'
                tcommd17 = [comm1,comm4,comm5,comm6,comm9,comm10]
                tcommd35 = [comm2,comm3,comm7,comm8]
                tsshd = tsendapp.ssh_connect(host1,usernamex,passwordx)
                tsftpd = tsendapp.sftp_open(tsshd)
                tsendapp.sftp_up(tsftpd,'/upload/LekeTeacher_' + tversion + '.apk','/tmp/LekeTeacher_' + tversion + '.apk')
                #tsendapp.sftp_close(tsshd)               
                for docommd17 in tcommd17:
                    tsshv17=tviapp17.ssh_connect(host1,usernamex,passwordx1,docommd17)
                    tviapp17.ssh_close(tsshv17)
                    print docommd17
                for docommd35 in tcommd35:
                    tsshv35=tviapp35.ssh_connect(host2,usernamex,passwordx,docommd35)
                    tviapp35.ssh_close(tsshv35)
                    print docommd35
                return redirect('/normalusersend/')
            elif tsendfile == None and tsenddate == None and tsendver == None:
                print ('do student')
                ssendapp = dosendapp()
                sviapp17=viapp()
                sviapp35=viapp()
                day = ssenddate
                host1='192.168.200.17'
                host2='192.168.200.35'
                usernamex='zhangsongbin'
                passwordx='zhangsongbin#16888'
                passwordx1='zhangsongbin#16888'
                sversion=ssendver
                soldsversion=ssendoldver
                comm1='sudo mv /var/www/html/exSchool/zongxian/appcenter/4/LekeStudent_'+ soldsversion +'.apk /var/www/html/exSchool/zongxian/appcenter/4/LekeStudent_'+ soldsversion +'.apk$(date +%Y-%m-%d).backup'
                comm2='sudo sed -i \'s/VERSION_0='+ soldsversion +'/VERSION_0=' + sversion + '/g\' /opt/mobilegateway/conf/mysvr.conf'
                comm3='sudo sed -i \'s/LekeStudent_'+ soldsversion +'/LekeStudent_' + sversion +'/g\' /opt/mobilegateway/conf/mysvr.conf'
                comm4='sudo sed -i \'41 s/^.*$/        "version":"' + sversion + '",/g\' /var/www/html/exSchool/zongxian/appcenter.php'
                comm5='sudo sed -i \'49 s/^.*$/        "updateDate":"' + day + '",/g\' /var/www/html/exSchool/zongxian/appcenter.php'
                comm6='sudo sed -i \'51 s/' + soldsversion + '/' + sversion + '/g\' /var/www/html/exSchool/zongxian/appcenter.php'
                comm8='sudo sh /opt/mobilegateway/start.sh'
                comm7='sudo kill -9 `ps -ef|grep mbgsvr|grep -v grep|awk \'{print $2}\'` '
                comm9='sudo mv /tmp/LekeStudent_'+ sversion +'.apk /var/www/html/exSchool/zongxian/appcenter/4/LekeStudent_'+ sversion +'.apk'
                comm10='sudo chmod 777 /var/www/html/exSchool/zongxian/appcenter/4/LekeStudent_'+ sversion +'.apk'
                scommd17 = [comm1,comm4,comm5,comm6,comm9,comm10]
                scommd35 = [comm2,comm3,comm7,comm8]
                ssshd = ssendapp.ssh_connect(host1,usernamex,passwordx)
                ssftpd = ssendapp.sftp_open(ssshd)
                ssendapp.sftp_up(ssftpd,'/upload/LekeStudent_' + sversion + '.apk','/tmp/LekeStudent_' + sversion + '.apk')
                #tsendapp.sftp_close(ssshd)  
                for docommd17 in scommd17:
                    ssshv17=sviapp17.ssh_connect(host1,usernamex,passwordx1,docommd17)
                    sviapp17.ssh_close(ssshv17)
                for docommd35 in scommd35:
                    ssshv35=sviapp35.ssh_connect(host2,usernamex,passwordx,docommd35)
                    sviapp35.ssh_close(ssshv35)
                return redirect('/normalusersend/')
        return render_to_response('normalusersend.html',sendappdic)
    else:
        return redirect('/login/')


def logout(request):
    try:
        del request.session['username']
        del request.session['privilege']
    except KeyError:
        pass
    return render_to_response('login.html')










    
