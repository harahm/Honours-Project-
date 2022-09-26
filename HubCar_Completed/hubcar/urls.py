from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from hubcarapp import views, apis

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),

    # Garage
    url(r'^garage/sign-in/$', auth_views.login,
        {'template_name': 'garage/sign_in.html'},
        name = 'garage-sign-in'),
    url(r'^garage/sign-out', auth_views.logout,
        {'next_page': '/'},
        name = 'garage-sign-out'),
    url(r'^garage/sign-up', views.garage_sign_up,
        name = 'garage-sign-up'),
    url(r'^garage/$', views.garage_home, name = 'garage-home'),

    url(r'^garage/account/$', views.garage_account, name = 'garage-account'),
    url(r'^garage/item/$', views.garage_item, name = 'garage-item'),
    url(r'^garage/item/add/$', views.garage_add_item, name = 'garage-add-item'),
    url(r'^garage/item/edit/(?P<item_id>\d+)/$', views.garage_edit_item, name = 'garage-edit-item'),
    url(r'^garage/order/$', views.garage_order, name = 'garage-order'),
    url(r'^garage/report/$', views.garage_report, name = 'garage-report'),

    # Sign In/ Sign Up/ Sign Out
    url(r'^api/social/', include('rest_framework_social_oauth2.urls')),
    # /convert-token (sign in/ sign up)
    # /revoke-token (sign out)
    url(r'^api/garage/order/notification/(?P<last_request_time>.+)/$', apis.garage_order_notification),


    # APIs for CUSTOMERS
    url(r'^api/customer/garages/$', apis.customer_get_garages),
    url(r'^api/customer/items/(?P<garage_id>\d+)/$', apis.customer_get_items),
    url(r'^api/customer/order/add/$', apis.customer_add_order),
    url(r'^api/customer/order/latest/$', apis.customer_get_latest_order),
    url(r'^api/customer/driver/location/$', apis.customer_driver_location),


    # APIs for DRIVERS
    url(r'^api/driver/orders/ready/$', apis.driver_get_ready_orders),
    url(r'^api/driver/order/pick/$', apis.driver_pick_order),
    url(r'^api/driver/order/latest/$', apis.driver_get_latest_order),
    url(r'^api/driver/order/complete/$', apis.driver_complete_order),
    url(r'^api/driver/revenue/$', apis.driver_get_revenue),
    url(r'^api/driver/location/update/$', apis.driver_update_location),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
