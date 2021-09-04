from rest_framework import serializers
from .models import *
def stored_date_format(getdate):
    import datetime
    cr_date = datetime.datetime.strptime(getdate, "%Y-%m-%d")
    new_format = "%d/%m/%Y"
    date = cr_date.strftime(new_format)
    return date
def stored_time_format(gettime):
    import datetime
    cr_date = datetime.datetime.strptime(gettime, "%H:%M:%S")
    new_format = "%I:%M%p"
    date = cr_date.strftime(new_format)
    return date
def datetime_format_change(getdate):
    import datetime
    cr_date = datetime.datetime.strptime(getdate, "%Y-%m-%dT%H:%M:%S")
    date_format = "%Y-%m-%d"
    date_formated = cr_date.strftime(date_format)
    date=stored_date_format(date_formated)
    return date

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields ='__all__'
        fields = ('email', 'username','pswd','password','usertype','status','phone_code',
                  'phone_number')
class coursesSerializer(serializers.ModelSerializer):
    # site_id = serializers.ReadOnlyField(source='site_id.id')
    # rank = serializers.ReadOnlyField(source='siterole_id.rank')
    # siterole = serializers.ReadOnlyField(source='siterole_id.name')
    # start_date= serializers.ReadOnlyField(source='site_id.start_date')
    # site_name=serializers.ReadOnlyField(source='site_id.name')
    class Meta:
        model = Courses
        fields =('id', 'name','category_id','course_image','course_code','course_type',
                 'author_id','sub_name')


    def to_representation(self, instance):
        ret = super(coursesSerializer, self).to_representation(instance)
        # is_list_view = isinstance(self.instance, list)
        # extra_ret = {'siteuser_id':ret['id']}
        # ret.update(extra_ret)
        # del ret['id']
        request = self.context.get("request")
        if instance.author_id:
            atr_img ="http://" + str(request.get_host() + str(instance.author_id.profile_image.url))
            ret['author_image']=atr_img
            ret['author_position']=instance.author_id.position
            ret['author_name']=instance.author_id.username
        else:
            ret['author_image']=None
            ret['author_position']=None
            ret['author_name']=None
        if instance.course_image:

            img = "http://" + str(request.get_host() + str(instance.course_image.url))
            ret['course_image'] = img
        ret['users_count']=CourseMembers.objects.filter(id=instance.id).count()
        return ret
class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
class taskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name')
    def to_representation(self, instance):
        ret = super(taskSerializer, self).to_representation(instance)
        if instance.id == 2:
            ret['active']="course-cat-active"
        else:
            ret['active'] = ""
        return ret
class bootcampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bootcamp
        fields = ('id', 'date','price','name','image','sub_name','subject','task')
    def to_representation(self, instance):
        ret = super(bootcampSerializer, self).to_representation(instance)
        request = self.context.get("request")
        if instance.date is not None:
            t = instance.date.time()
            formated_t = str(t.hour) + ":" + str(t.minute) + ":" + str(t.second)
            d = instance.date.date()
            time_date = str(stored_date_format(str(d))) + " : " + str(stored_time_format(str(formated_t)))
            ret['date']=time_date
        if instance.image:

            img = "http://" + str(request.get_host() + str(instance.image.url))
            ret['image'] = img
        if instance.task:
            ret['task_name']=instance.task.name
        del ret['task']
        return ret
class helpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = ('name', 'email','query')
class courseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ['name','sub_name','author_id','description','total_length_course','preview_video']
    def to_representation(self, instance):
        ret = super(courseDetailsSerializer, self).to_representation(instance)
        request = self.context.get("request")
        if instance.author_id:
            atr_img ="http://" + str(request.get_host() + str(instance.author_id.profile_image.url))
            ret['author_image']=atr_img
            ret['author_position']=instance.author_id.position
            ret['author_name']=instance.author_id.username
        else:
            ret['author_image']=None
            ret['author_position']=None
            ret['author_name']=None
        if instance.course_image:

            img = "http://" + str(request.get_host() + str(instance.course_image.url))
            ret['course_image'] = img
        if instance.preview_video:

            video = "http://" + str(request.get_host() + str(instance.preview_video.url))
            ret['preview_video'] = video
        ret['users_count']=CourseMembers.objects.filter(id=instance.id).count()
        ret['module_count']=Module.objects.filter(course_id=instance.id).count()
        ret['miniproject_count'] = MiniProject.objects.filter(course_id=instance.id).count()
        ret['majorproject_count'] = MajorProject.objects.filter(course_id=instance.id).count()
        t=CoursesTopics.objects.filter(course_id=instance.id)
        dict_data={}
        list_data=[]
        for tpic in t:
            sub_topics=CoursesTopicsDetails.objects.filter(topic_id=tpic.id)
            for s in sub_topics:
                list_data.append(s.sub_topic_name)
            dict_data[tpic.topic_name]=list_data
        topics=dict_data
        ret['course_topics']=topics
        return ret
class webinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webinar
        fields = ['date','image','name','webinar_link']
    def to_representation(self, instance):
        ret = super(webinarSerializer, self).to_representation(instance)
        request = self.context.get("request")
        if instance.date is not None:
            t = instance.date.time()
            formated_t = str(t.hour) + ":" + str(t.minute) + ":" + str(t.second)
            d = instance.date.date()
            time_date = str(stored_date_format(str(d))) + " : " + str(stored_time_format(str(formated_t)))
            ret['date']=time_date
            ret['time']=str(stored_time_format(str(formated_t)))
        else:
            ret['time']=None
        if instance.image:

            img = "http://" + str(request.get_host() + str(instance.image.url))
            ret['image'] = img

        return ret
class courseTopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursesTopics
        fields = ['date','topic_name','batch_id']
    def to_representation(self, instance):
        ret = super(courseTopicsSerializer, self).to_representation(instance)
        request = self.context.get("request")
        if instance.date is not None:

            d = instance.date.date()
            date = str(stored_date_format(str(d)))
            ret['date']=date
        if instance.batch_id:
            ret['batch_name']=instance.batch_id.batch_name
        else:
            ret['batch_name'] =None


        return ret