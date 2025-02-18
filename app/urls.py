from django.contrib import admin
from django.urls import path, include
from  app import views 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
    path('SponsorListCreateAPIView/',views.SponsorListCreateAPIView.as_view()),
    path("SponsorDetailandDeleteAPIView/<int:pk>/",views.SponsorDetailandDeleteAPIView.as_view()),
    path('StudentListCretaAPIview/', views.StudentListCretaAPIview.as_view()),
    path("StudentSponsorUpdateAPIView/<int:pk>/",views.StudentSponsorUpdateandDELETE_APIView.as_view()),
    path('StudentSponsorCreateAPIView/',views.StudentSponsorCreateAPIView.as_view()),
    path('UniversityListCreateView/', views.UniversityListCreateView.as_view()),
    path("StudentUpdate_and_delete_view/<int:pk>/",views.StudentUpdate_and_delete_view.as_view()),
    path('dashboard/', views.Dashboard.as_view()),
]

