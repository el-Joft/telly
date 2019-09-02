from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from api_v1.views.user import UserViewSet
from api_v1.views.userinfo import UserInfoViewSet
from django.urls import path

api_router = DefaultRouter()
api_router.register('register', UserViewSet, 'register')
app_name = 'api_v1'
urlpatterns = [
    path('', include(api_router.urls), name='api_v1'),
    path('activate/<uidb64>/<token>/',
         UserViewSet.as_view({'get': 'activate'}), name='activate'),
    path('auth/', include('rest_auth.urls')),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('usersinfo',
         UserInfoViewSet.as_view({'get': 'list'}), name='userinfo')
]
