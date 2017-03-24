from django.conf.urls import url
from app import views
from django.conf import settings
from django.conf.urls.static import static



app_name = 'app'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'week/$', views.index_week, name='index_week'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^register/$',views.register,name='register'),
    url(r'about/$', views.about, name='about'),
    url(r'profile/$', views.profile, name='profile'),
    url(r'SquadZ/$', views.SquadZ, name='SquadZ'),
    url(r'^class/(?P<classId>[\w\-]+)/$', views.showClass, name='showClass'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
