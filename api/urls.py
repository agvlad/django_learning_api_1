from django.urls import path
from .views import NetworkList, NetworkDetail, RouterList, RouterDetail
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('networks/', NetworkList.as_view(), name='networks'),
    path('networks/<str:pk>', NetworkDetail.as_view(), name='network'),
    path('routers/', RouterList.as_view(), name='routers'),
    path('routers/<str:pk>', RouterDetail.as_view(), name='router'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]