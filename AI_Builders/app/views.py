from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from .serializers import *
from rest_framework.pagination import PageNumberPagination  # pagination
from rest_framework.filters import SearchFilter  # for searching
from rest_framework import generics
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import *
from .serializers import *
from django.contrib.auth.hashers import make_password
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.db.models import Q
import calendar
from itertools import chain

from datetime import date
# Create your views here.
import os
def index(request):

    return render(request,'temp/ind.html')
def success_response(message):
    dictionary={}
    dictionary['status_code']=200
    dictionary['message']=message
    data = {"results": dictionary}
    return data
def failed_response(message,reason):

    dictionary={}

    dictionary['status_code']=401
    dictionary['message']=message
    dictionary['reason']=reason
    data = {"results": dictionary}
    return data
def success_response_data_list(data,count):
    message= "Success"
    response_dict = success_response(message)
    result = response_dict['results']
    result['count'] = count
    result['data'] = data
    data = {"results": result}
    return data
class UserSave(APIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser,FileUploadParser)
    serializer_class = userSerializer
    def post(self, request, format=None):
        # de_layout_id =request.data.get('de_layout_id')
        # getdate =request.data.get('date')
        # user = request.data.get('user')
        pswd="12345678"
        password=make_password(pswd)
        datas=request.data
        datas['pswd']=pswd
        datas['password']=password
        # datas['usertype'] = "1"
        datas['status']=True
        print(datas)
        save_user_data_serializers =userSerializer(data=datas)
        if save_user_data_serializers.is_valid():
            v=save_user_data_serializers.save()

            print("kkk",save_user_data_serializers.data,v,v.id)

            message = "Succesfully saved"
            response_dict = success_response(message)

        else:
            message="Not Saved"
            reason="Fill all fields"
            response_dict = failed_response(message,reason)
        return Response(response_dict)

from rest_framework.pagination import PageNumberPagination  # pagination

class setPagination(PageNumberPagination):
    page_size = 20
from rest_framework.permissions import IsAuthenticated  # <-- Here
class getCoursesList(generics.ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    pagination_class = setPagination
    serializer_class = coursesSerializer
    # permission_classes = (IsAuthenticated,)             # <-- And here


    def get_queryset(self):
        # queryset = Sites.objects.all().order_by('-id')
        queryset = Courses.objects.filter(soft_delete=False).order_by('-id')
        recent = self.request.query_params.get('recent', None)
        type = self.request.query_params.get('type', None)
        print("oooo",recent,type)
        if recent is not None:
            get_recent_courses=Courses.objects.filter(soft_delete=False).exists()
            if get_recent_courses:
                queryset = Courses.objects.filter(soft_delete=False).order_by('-id')[:5]
        if type is not None:
            get_by_type_courses=Courses.objects.filter(soft_delete=False).exists()
            if get_by_type_courses:
                if type == "paid":
                    queryset = Courses.objects.filter(soft_delete=False,course_type="Paid").order_by('-id')
                elif type == "free":
                    queryset = Courses.objects.filter(soft_delete=False,course_type="Free").order_by('-id')
                else:
                    queryset = Courses.objects.none()

        return queryset
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        print("page",page)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        count=queryset.count()
        print(queryset,count)
        if count == 0:
            message="Fail"
            reason="No Courses Added!"
            response_dict=failed_response(message,reason)
        else:
            data=serializer.data
            response_dict = success_response_data_list(data,count)
        return Response(response_dict)
