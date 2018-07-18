from django.conf.urls import url
from . import views
 
urlpatterns = [
    url(r'^campus2$', views.index),
    url(r'^campus2/regUser$', views.regUser),
    url(r'^campus2/login$', views.login),
    url(r'^campus2/dashboard$', views.dashboard),
    url(r'^campus2/logout$', views.logout),
    url(r'^campus2/system$', views.system),
    url(r'^campus2/addUserType$', views.addUserType),
    url(r'^campus2/addUserGroup/(?P<userID>\d+)$', views.addUserGroup),
    url(r'^campus2/user/(?P<userID>\d+)$', views.user),
    url(r'^campus2/services/(?P<userID>\d+)$', views.services),
    url(r'^campus2/addMealType$', views.addMealType),
    url(r'^campus2/addMeal/(?P<userID>\d+)$', views.addMeal),
    url(r'^campus2/addBuilding/(?P<userID>\d+)$', views.addBuilding),
    url(r'^campus2/addParking/(?P<userID>\d+)$', views.addParking),
    url(r'^campus2/deleteGroup/(?P<userID>\d+)/(?P<noID>\d+)$', views.deleteGroup),
    url(r'^campus2/deleteMeal/(?P<userID>\d+)/(?P<noID>\d+)$', views.deleteMeal),
    url(r'^campus2/deleteBuilding/(?P<userID>\d+)/(?P<noID>\d+)$', views.deleteBuilding),
    url(r'^campus2/deleteParking/(?P<userID>\d+)/(?P<noID>\d+)$', views.deleteParking),
    url(r'^campus2/updatePhone/(?P<userID>\d+)$', views.updatePhone),
    url(r'^campus2/updateExtNum/(?P<userID>\d+)$', views.updateExtNum),
    url(r'^campus2/updatePersonEmail/(?P<userID>\d+)$', views.updatePersonEmail),
]
