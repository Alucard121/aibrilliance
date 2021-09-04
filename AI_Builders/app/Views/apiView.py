from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from ..serializers import *
from rest_framework.pagination import PageNumberPagination  # pagination
from rest_framework.filters import SearchFilter  # for searching
from rest_framework import generics
from ..models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import *
from django.contrib.auth.hashers import make_password
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.db.models import Q
import calendar
from itertools import chain
import datetime
from datetime import date
# Create your views here.
import os
import requests
def otp_generate(obj_id):

    today = datetime.datetime.now()
    print(today)
    print("11111111")
    ts = today.timestamp()
    ts=round(ts/100)
    print("timestamp:-", ts)
    if len(str(obj_id))==1:
        obj_id=str(0)+str(obj_id)
    else:
        pass
    otp = str(obj_id)[-2:] + str(ts)[-3:]

    return otp
def send_otp(request, mobile=None):
    response_data = {}

    user_phone = mobile
    ###########2factor api#################
    try:

        APIKey ="ca2eca79-fc00-11eb-a13b-0200cd936042"

        url = "https://2factor.in/API/V1/"+APIKey+"/SMS/" + user_phone + "/AUTOGEN"
        response = requests.request("GET", url)
        data = response.json()
        print(data)
        if data['Status'] == 'Success':
            request.session['otp_session_data'] = data['Details']
            # otp_session_data is stored in session.
            response_data['Message'] = 'Success'

        else:
            response_data['Message'] = 'Failed'
            response_data['Error'] = data['Details']
        response_data['session_id'] = data['Details']
    except Exception as e:
        response_data['Message'] = 'Failed'
        response_data['Error'] = e
        ###########2factor api end#################

    response_data['Message'] = 'Success'
    return response_data
def Verify_SMS_OTP_Input(request,session_id,otp_input):
    response_data = {}


    ###########2factor api#################
    try:

        APIKey = "ca2eca79-fc00-11eb-a13b-0200cd936042"

        url = "https://2factor.in/API/V1/"+APIKey+"/SMS/VERIFY/"+session_id+"/"+otp_input
        response = requests.request("GET", url)
        data = response.json()
        print(data)
        if data['Status'] == 'Success':
            # request.session['otp_session_data'] = data['Details']
            # # otp_session_data is stored in session.
            # response_data['Message'] = 'Success'
            response_data=data

        else:
            response_data['Message'] = 'Failed'
            response_data['Error'] = data['Details']
        # response_data['session_id'] = data['Details']
    except Exception as e:
        response_data['Message'] = 'Failed'
        response_data['Error'] = e
        ###########2factor api end#################

    response_data['Message'] = 'Success'
    return response_data
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
def success_response_with_data(message,data):
    response_dict = success_response(message)
    results = response_dict['results']
    results['data'] = data
    data = {"results": results}
    return data
class UserSave(APIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser,FileUploadParser)
    serializer_class = userSerializer
    def post(self, request, format=None):
        # de_layout_id =request.data.get('de_layout_id')
        # getdate =request.data.get('date')
        pswd = request.data.get('password')
        from django.core.validators import validate_email
        print(request.data.get('email'))
        print("type",type(request.data.get('phone_number')))
        # pswd="12345678"
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
class verify_otp(generics.ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class = coursesSerializer
    # permission_classes = (IsAuthenticated,)             # <-- And here


    def get_queryset(self):
        code = self.request.query_params.get('code', None)
        mobile = self.request.query_params.get('phone', None)
        if mobile is None:
            response_data={}
        else:
            response_data=send_otp(self.request, mobile)
        response_data['phone']=mobile
        return response_data
    def get(self, request, *args, **kwargs):
        response_data = self.get_queryset()
        print(response_data)
        if response_data == {}:
            message="Fail"
            reason="Please enter valid phone number!"
            response_dict=failed_response(message,reason)
        else:
            response_dict = response_data
        return Response(response_dict)
class verify_otp_input(generics.ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    # permission_classes = (IsAuthenticated,)             # <-- And here


    def get_queryset(self):

        session_id = self.request.query_params.get('session_id', None)
        otp_input =self.request.query_params.get('otp',None)
        if session_id is None or otp_input is None:
            response_data={}
        else:
            response_data=Verify_SMS_OTP_Input(self.request,session_id,otp_input)

        return response_data
    def get(self, request, *args, **kwargs):
        response_data = self.get_queryset()
        print(response_data)
        if response_data == {}:
            message="Fail"
            reason="Please enter valid otp!"
            response_dict=failed_response(message,reason)
        else:
            response_dict = response_data
        return Response(response_dict)
class Login(APIView):
    parser_classes = (JSONParser,MultiPartParser,  FormParser)

    def post(self, request, format=None):
        code=request.data.get('phone_code')
        phone = request.data.get('phone_number')
        email = request.data.get('email')
        password =request.data.get('password')
        print(request.data)
        if phone is not None:
            obj_exists=CustomUser.objects.filter(phone_code=code,phone_number=phone).exists()
            print(obj_exists)
            if obj_exists:
                print("ok")
                encrypt_pass=make_password(password)
                user_check_password_obj_exist=CustomUser.objects.filter(phone_code=code,phone_number=phone,pswd=password).exists()
                if user_check_password_obj_exist:
                    print("yes")

                    obj=CustomUser.objects.filter(phone_code=code,phone_number=phone,pswd=password).last()
                    message = 'Successfully verified'
                    data = {"user_id": obj.id, "name": obj.username, "user_code":obj.user_code}
                    response_dict = success_response_with_data(message, data)
                else:
                    message = 'Verification Failed'
                    reason = 'Incorrect Password '
                    response_dict = failed_response(message, reason)
            else:
                message = 'Verification Failed'
                reason = 'User not exist '
                response_dict = failed_response(message, reason)

        elif email is not None:
            email_obj_exists = CustomUser.objects.filter(email=email).exists()
            if email_obj_exists:
                emailuser_check_password_obj_exist = CustomUser.objects.filter(email=email,
                                                                              pswd=password).exists()
                if emailuser_check_password_obj_exist:

                    obj = CustomUser.objects.filter(email=email,pswd=password).last()
                    message = 'Successfully verified'
                    data = {"user_id": obj.id, "name": obj.username, "user_code": obj.user_code}
                    response_dict = success_response_with_data(message, data)
                else:
                    message = 'Verification Failed'
                    reason = 'Incorrect Password '
                    response_dict = failed_response(message, reason)
            else:
                message = 'Verification Failed'
                reason = 'User not exist '
                response_dict = failed_response(message, reason)
        else:
            message = 'Verification Failed'
            reason = 'Please enter valid email/phone'
            response_dict = failed_response(message, reason)

        return Response(response_dict)
class ForgotPassword(APIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def post(self, request, format=None):
        otp_input = request.data.get('otp', None)
        new_pass= request.data.get('new_pass', None)
        confirm_pass= request.data.get('confirm_pass', None)
        code = request.data.get('code', None)
        phone = request.data.get('number', None)
        session_id=request.data.get('session_id', None)
        print("phonr",phone)
        if new_pass == confirm_pass:
            if session_id is not None:
                check=Verify_SMS_OTP_Input(request, session_id, otp_input)
                if check['Status']=="Success":
                    new_pass_encrypted = make_password(new_pass)
                    user_obj = CustomUser.objects.filter(phone_number=phone, phone_code=code).update(
                        password=new_pass_encrypted)
                    message = "Succesfully updated password"
                    response_dict = success_response(message)
                else:
                    message = 'Failed'
                    reason = 'otp verification failed'
                    response_dict = failed_response(message, reason)
            else:
                message = 'Failed'
                reason = 'Please send otp'
                response_dict = failed_response(message, reason)

        else:
            message = 'Failed'
            reason = 'Password mismatch'
            response_dict = failed_response(message, reason)
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
        task =self.request.query_params.get('task', None)
        print("oooo",recent,type)
        if task is not None and next is not None:
            queryset = Courses.objects.filter(task_id__id=task,soft_delete=False).order_by('-id')[:5]
        if task is not None:
            queryset = Courses.objects.filter(task_id__id=task, soft_delete=False).order_by('-id')
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
class getCategoryList(generics.ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    pagination_class = setPagination
    serializer_class = categorySerializer
    # permission_classes = (IsAuthenticated,)             # <-- And here


    def get_queryset(self):
        queryset = Category.objects.filter(soft_delete=False).order_by('-id')
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
            reason="No Category Added!"
            response_dict=failed_response(message,reason)
        else:
            data=serializer.data
            response_dict = success_response_data_list(data,count)
        return Response(response_dict)
class getTaskList(generics.ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    pagination_class = setPagination
    serializer_class = taskSerializer
    # permission_classes = (IsAuthenticated,)             # <-- And here


    def get_queryset(self):
        queryset = Task.objects.filter(soft_delete=False).order_by('id')
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
            reason="No Tasks Added!"
            response_dict=failed_response(message,reason)
        else:
            data=serializer.data
            response_dict = success_response_data_list(data,count)
        return Response(response_dict)
class getBootcampList(generics.ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    pagination_class = setPagination
    serializer_class = bootcampSerializer
    # permission_classes = (IsAuthenticated,)             # <-- And here


    def get_queryset(self):
        queryset = Bootcamp.objects.filter(soft_delete=False).order_by('id')
        next = self.request.query_params.get('next', None)
        if next == 2:
            queryset=Bootcamp.objects.filter(soft_delete=False,status="Next",date__lte = datetime.datetime.now()).order_by('id')[:2]
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
            reason="No Bootcamp Added!"
            response_dict=failed_response(message,reason)
        else:
            data=serializer.data
            response_dict = success_response_data_list(data,count)
        return Response(response_dict)
class HelpSave(APIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser,FileUploadParser)
    serializer_class = helpSerializer
    def post(self, request, format=None):
        # name =request.data.get('de_layout_id')
        # getdate =request.data.get('date')
        # user = request.data.get('user')

        datas=request.data

        print(datas)
        save_help_data_serializers =helpSerializer(data=datas)
        if save_help_data_serializers.is_valid():
            v=save_help_data_serializers.save()

            print("kkk",save_help_data_serializers.data,v,v.id)

            message = "Succesfully saved"
            response_dict = success_response(message)

        else:
            message="Not Saved"
            reason="Fill all fields"
            response_dict = failed_response(message,reason)
        return Response(response_dict)
class getCoursesDetailsList(generics.ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    # pagination_class = setPagination
    serializer_class = courseDetailsSerializer
    # permission_classes = (IsAuthenticated,)             # <-- And here


    def get_queryset(self):
        queryset = Courses.objects.filter(soft_delete=False).order_by('id')
        course_id = self.request.query_params.get('course_id', None)
        if course_id is not None:
            queryset=Courses.objects.filter(id=course_id)
        return queryset
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        count=queryset.count()
        print(queryset,count)
        if not serializer:
            message="Fail"
            reason="No Course Details Added!"
            response_dict=failed_response(message,reason)
        else:
            data=serializer.data
            response_dict = success_response_data_list(data,count)
        return Response(response_dict)
class getWebinarList(generics.ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    # pagination_class = setPagination
    serializer_class = webinarSerializer
    # permission_classes = (IsAuthenticated,)             # <-- And here


    def get_queryset(self):
        queryset = Webinar.objects.filter(soft_delete=False).order_by('-id')
        type = self.request.query_params.get('type', None)
        if type == "upcoming":
            print("lll")
            status_list =["Live Now","Next"]
            queryset = Webinar.objects.filter(soft_delete=False,status__in=status_list).order_by('-id')[:4]
            print(queryset.count())
        elif type == "past":
            queryset = Webinar.objects.filter(soft_delete=False,status="Completed").order_by('-id')[:4]
        else:
            queryset=Webinar.objects.filter(soft_delete=False).order_by('-id')[:4]


        return queryset
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        # page = self.paginate_queryset(queryset)
        # print("page",page)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        count=queryset.count()
        print(queryset,count)
        if count == 0:
            message="Fail"
            reason="No Webinars Added!"
            response_dict=failed_response(message,reason)
        else:
            data=serializer.data
            response_dict = success_response_data_list(data,count)
        return Response(response_dict)
class getCourseTopicList(generics.ListAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    # pagination_class = setPagination
    serializer_class = courseTopicsSerializer
    # permission_classes = (IsAuthenticated,)             # <-- And here


    def get_queryset(self):
        queryset = CoursesTopics.objects.none()
        course_id = self.request.query_params.get('course_id', None)
        if course_id is not None:

            queryset = CoursesTopics.objects.filter(soft_delete=False,course_id=course_id).order_by('id')
            print(queryset.count())

        return queryset
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        # page = self.paginate_queryset(queryset)
        # print("page",page)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        count=queryset.count()
        print(queryset,count)
        if count == 0:
            message="Fail"
            reason="No CoursesTopics Added!"
            response_dict=failed_response(message,reason)
        else:
            data=serializer.data
            response_dict = success_response_data_list(data,count)
        return Response(response_dict)