from django.urls import path
from .views import *


app_name = "channel"
urlpatterns = [
    path('channels/', channelList, name="channelList"),
    path('detail/<int:id>/', channelDetail, name="channelDetail"),
    path("create_channel/", createChannel, name="createChannel"),
    path("update_channel/<int:id>/", updateChannel, name="updateChannel"),
    path("delete_channel/<int:id>/", deleteChannel, name="deleteChannel"),

    # subscriptions
    path('subscriptons/', subscriptionsList, name="subscriptonsList"),

    path('channel/subscribe/<int:id>/', subscribeView, name="subscribeChannel"),

]
