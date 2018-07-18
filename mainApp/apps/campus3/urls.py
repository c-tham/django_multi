from django.conf.urls import url
from . import views

#------------------------------------------------------------------------------
# Codes start here ... Chia Tham
urlpatterns = [
    url(r'^campus3$', views.index),
    url(r'^campus3/$', views.index),
    url(r'^campus3/regUser$', views.regUser),
    url(r'^campus3/login$', views.login),
    url(r'^campus3/dashboard/(?P<userID>\d+)$', views.dashboard),
    url(r'^campus3/admin$', views.admin),
    url(r'^campus3/logout$', views.logout),
    url(r'^campus3/system$', views.system),
    url(r'^campus3/addUserType$', views.addUserType),
    url(r'^campus3/addUserGroup/(?P<userID>\d+)$', views.addUserGroup),
    url(r'^campus3/user/(?P<userID>\d+)$', views.user),
    url(r'^campus3/services/(?P<userID>\d+)$', views.services),
    url(r'^campus3/addMealType$', views.addMealType),
    url(r'^campus3/addMeal/(?P<userID>\d+)$', views.addMeal),
    url(r'^campus3/addBuilding/(?P<userID>\d+)$', views.addBuilding),
    url(r'^campus3/addParking/(?P<userID>\d+)$', views.addParking),
    url(r'^campus3/deleteGroup/(?P<userID>\d+)/(?P<noID>\d+)$', views.deleteGroup),
    url(r'^campus3/deleteMeal/(?P<userID>\d+)/(?P<noID>\d+)$', views.deleteMeal),
    url(r'^campus3/deleteBuilding/(?P<userID>\d+)/(?P<noID>\d+)$', views.deleteBuilding),
    url(r'^campus3/deleteParking/(?P<userID>\d+)/(?P<noID>\d+)$', views.deleteParking),
    url(r'^campus3/updatePhone/(?P<userID>\d+)$', views.updatePhone),
    url(r'^campus3/updateExtNum/(?P<userID>\d+)$', views.updateExtNum),
    url(r'^campus3/updatePersonEmail/(?P<userID>\d+)$', views.updatePersonEmail),
    url(r'^campus3/hack/(?P<userID>\d+)$', views.hack),
    url(r'^campus3/hacking/(?P<userID>\d+)$', views.hacking),
    url(r'^campus3/destory/(?P<userID>\d+)$', views.destory),
    url(r'^campus3/deleteGroupType/(?P<noID>\d+)$', views.deleteGroupType),
    url(r'^campus3/deleteMealType/(?P<noID>\d+)$', views.deleteMealType),
]
