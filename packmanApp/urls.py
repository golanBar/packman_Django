from django.conf.urls import patterns, url

from packmanApp import views

urlpatterns = patterns('',
    url(r'^$', views.loginUser, name='loginUser'),
	url(r'^joinTeam/$', views.joinTeam, name='join'),
	url(r'^showStatistics/$', views.showStatistics, name='statistics'),	
	url(r'^persistScore/$', views.persistScore, name='persist')		
)