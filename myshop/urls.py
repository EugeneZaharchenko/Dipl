from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login as login, logout as logout, logout_then_login as logout_login
from django.contrib.sitemaps.views import sitemap
from shop.sitemaps import ProductSitemap

sitemaps = {
    'products': ProductSitemap,
}


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    #url(r'^payment/', include('payment.urls', namespace='payment')),
    # url(r'^login/$', login, name='login'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^logout-then-login/$', logout_login, name='logout_then_login'),
    url(r'^', include('shop.urls', namespace='shop'), ),
    # sign_in/sign_out via FB
    url(r'^api/social/', include('rest_framework_social_oauth2.urls')),
    url('social-auth/', include('social.apps.django_app.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
