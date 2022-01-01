from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path(r'^register/$', views.RegisterView.as_view(), name='register'),
    path(r'^$', views.MainView.as_view(), name='main'),
    path(r'^first/$', views.FirstView.as_view(), name='first'),
    path(r'^second/(?P<pk>[0-9]+)/$', views.SecondPhaseView.as_view(), name='second'),
    path(r'^reset/(?P<pk>[0-9]+)/$', views.ResetView.as_view(), name='reset'),
    path(r'^dashboard/$', views.get_data_dashboard, name='dashboard'),
]