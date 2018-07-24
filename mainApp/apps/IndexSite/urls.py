from django.conf.urls import url
from . import views
 
urlpatterns = [
    url(r'^$', views.index),
    url(r'^feedback$', views.feedback),
    url(r'^campus2x$', views.campus2x),
    url(r'^campus3x$', views.campus3x),
]
