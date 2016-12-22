from django.conf.urls import patterns, include, url
from django.contrib import admin
from app.views import login,getuser,user,normaluser,logout,usersend,normalusersend

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', login),
    url(r'^getuser/$', getuser),
    url(r'^user/$', user),
    url(r'^normaluser/$', normaluser),
    url(r'^logout/', logout),
    url(r'^usersend/$', usersend),
    url(r'^normalusersend/$',normalusersend),
    url(r'^$',login)
)
