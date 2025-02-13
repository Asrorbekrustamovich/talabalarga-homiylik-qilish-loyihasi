
from rest_framework import status
from app.models import *
from .serializers import *
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from .models import Sponsor, StudentSponsor
from rest_framework import generics
from rest_framework.views import Response
from . import serializers
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from .permissions import CustomPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
#for Sponsor create and get
class SponsorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Sponsor.objects.all()
    filter_backends=[DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ('status', 'amount')
    search_fields = ['full_name', 'phone']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        return serializers.SponsorSerializer if self.request.method == 'POST' else serializers.SponsorListSerializer
    # def get_permissions(self):
    #     if self.request.method=='POST':
    #         self.permission_classes=[permissions.AllowAny]
    #     else:
    #         self.permission_classes=[CustomPermission]
        
    #     return super().get_permissions()

class SponsorDetailandDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = serializers.SponsorListSerializer

class StudentListCretaAPIview(generics.ListCreateAPIView):
    permission_classes=[AllowAny]
    queryset=Student.objects.all()
    filter_backends=[DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ('university', 'type')
    search_fields = ['full_name','university__name']
    
    def get_serializer_class(self):
        return serializers.StudentSerializer if self.request.method=='POST' else serializers.StudentListSerializer

class StudentUpdate_and_delete_view(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer


class StudentSponsorCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset=StudentSponsor.objects.all()
    def get_serializer_class(self):
        return serializers.StudentSponsorSerializer if self.request.method=='POST' else serializers.StudentSponsorListserializer
    serializer_class = serializers.StudentSponsorSerializer



class StudentSponsorUpdateandDELETE_APIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = StudentSponsor.objects.all()
    serializer_class = serializers.StudentSponsorUpdateSerializer

class UniversityListCreateView(generics.ListCreateAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

class Dashboard(APIView):
    def get(self, request):
        this_year = timezone.now().year


        students_per_month = (
            Student.objects.filter(created_at__year = this_year).annotate(month = TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month') or None
        )
        sponser_per_month = (
            Sponsor.objects.filter(created_at__year = this_year).annotate(month = TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month') or None
        )

        formatted_data_sponser = [
            {"month": entry["month"].strftime("%Y-%m-%d"), "count": entry["count"] or None}
            for entry in sponser_per_month
        ]

        formatted_data_student = [
            {"month": entry['month'].strftime("%Y-%m-%d"), "count": entry["count"] or None}
            for entry in students_per_month
        ]

        response_date= {
            "Sponser": formatted_data_sponser or None,
            "Student": formatted_data_student or None,
        }

        return Response(response_date or None)