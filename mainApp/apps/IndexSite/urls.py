from django.conf.urls import url
from . import views
 
urlpatterns = [
    url(r'^$', views.index),
    url(r'^feedback$', views.feedback),
    url(r'^campus2$', views.campus2),
    url(r'^campus3$', views.campus3),
]
