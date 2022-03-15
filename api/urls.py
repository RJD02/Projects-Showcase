from django.urls import path

from api.views import getProject, getProjects, getRoutes, removeTag, voteProject
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', getRoutes),
    path('projects/', getProjects),
    path('projects/<str:pk>/', getProject),
    path('projects/<str:pk>/vote/', voteProject),

    path('remove-tag/', removeTag)
]
