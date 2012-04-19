from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djow.views.home', name='home'),
    # url(r'^djow/', include('djow.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}),
    
    url(r'^insert', 'financial.views.cashflow_edit'),
    url(r'^category/insert', 'financial.views.category_edit'),
    
    url(r'^remove', 'financial.views.cashflow_remove'),
    url(r'^category/remove', 'financial.views.category_remove'),
    
    url(r'^category', 'financial.views.category'),
    url(r'^', 'financial.views.index'),
    
)

urlpatterns += staticfiles_urlpatterns()