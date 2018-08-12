from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    #path('guard/new/', views.new_guard, name='new_guard'),

    path('guard/', views.GuardView.as_view(), name='guard'),
    path('guard/guardcreate/', views.GuardCreate.as_view(), name='guard_create'),
    path('guard/guardcreate/done/', views.GuardCreateDone.as_view(), name='guard_create_done'),
    path('guard/<slug:slug>/', views.GuardDetailView.as_view(), name='guard_detail'),
    path('guard/<slug:slug>/update/', views.GuardUpdate.as_view(), name='guard_update'),
    path('guard/<slug:slug>/delete/', views.GuardDelete.as_view(), name='guard_delete'),
    

    path('site/', views.SiteView.as_view(), name='site'),
    path('site/sitecreate/', views.SiteCreate.as_view(), name='site_create'),
    path('site/sitecreate/done/', views.SiteCreateDone.as_view(), name='site_create_done'),
    path('site/<slug:slug>/', views.SiteDetailView.as_view(), name='site_detail'),
    path('site/<slug:slug>/update/', views.SiteUpdate.as_view(), name='site_update'),
    path('site/<slug:slug>/delete/', views.SiteDelete.as_view(), name='site_delete'),
    

    path('schedule/', views.ScheduleView.as_view(), name='schedule'),
    path('schedule/schedulecreate/', views.ScheduleCreate.as_view(), name='schedule_create'),
    path('schedule/schedulecreate/done/', views.ScheduleCreateDone.as_view(), name='schedule_create_done'),
    path('schedule/<slug:slug>/', views.ScheduleDetailView.as_view(), name='schedule_detail'),
    path('schedule/<slug:slug>/update/', views.ScheduleUpdate.as_view(), name='schedule_update'),
    path('schedule/<slug:slug>/delete/', views.ScheduleDelete.as_view(), name='schedule_delete'),
    
]