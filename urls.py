from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'frame.views.index', name='index'),
    url(r'login$', 'frame.views.signup', name='signup'),
    url(r'register$', 'frame.views.register', name='register'),
    url(r'user_info$', 'frame.views.user_info', name='user_info'),
    url(r'add_task/$', 'frame.views.add_task', name='add_task'),
    url(r'del_task/$', 'frame.views.del_task', name='del_task'),
    url(r'update_task/$', 'frame.views.update_task', name='update_task'),
    url(r'tasks/$', 'frame.views.tasks', name='tasks'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),   
)
