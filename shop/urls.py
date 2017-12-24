from django.conf.urls import url, include
from django.contrib.auth.views import login as login, logout as logout, logout_then_login as logout_login
from . import views


urlpatterns = [
    url(r'^$', views.product_list, name='product_list'),
    # url(r'^login/$', login, name='login'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
]
