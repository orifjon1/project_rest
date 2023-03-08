from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserView, SectorView, TaskView, TaskDisplayView, TaskReviewView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('sector/', SectorView.as_view(), name='sector'),
    path('signup/', UserView.as_view(), name='signup'),
    path('task/', TaskView.as_view(), name='task'),
    path('task/review/<int:id>/', TaskReviewView.as_view(), name='review'),
    path('status/', TaskDisplayView.as_view(), name='status'),
]
