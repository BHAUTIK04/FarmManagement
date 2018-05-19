from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^createfarmer$', views.createFarmerDetail),
    url(r'^createfarm$', views.createFarm),
    url(r'^createschedule$', views.createSchedule),
    url(r'^listallfarmer$', views.listAllFarmer),
    url(r'^listallfarm$', views.listAllFarm),
    url(r'^due$', views.allDue),
]