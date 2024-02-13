from django.contrib.auth import authenticate
from rest_framework import serializers

from Nedelapare_site.models import User as CustomUser, Student, Teacher, University, Faculty, UniversityToFaculty, \
    Lesson, Group as ClassGroup


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'name', 'position')


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'required': True}
        }

    def validate(self, attrs):
        exist_flag = False
        email = attrs.get('email', '').strip().lower()
        attrs['email'] = email
        user = CustomUser.objects.filter(email=email)
        if user.exists():
            exist_flag = True
        user = user.filter(confirmed_email=True)
        if user.exists():
            raise serializers.ValidationError('User with this email id already exists.')
        attrs['confirmed_email'] = False
        position = attrs.get('position', 0)
        if position < 0 or position > 2:
            raise serializers.ValidationError('Недопустимое значение')
        return attrs, exist_flag

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email').lower()
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Please give both email and password.")

        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email does not exist.')

        user = authenticate(request=self.context.get('request'), email=email,
                            password=password)
        if not user:
            raise serializers.ValidationError("Wrong Credentials.")

        if not user.confirmed_email:
            raise serializers.ValidationError('Email not confirmed')

        attrs['user'] = user
        return attrs


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'


class UniversityToFacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityToFaculty
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassGroup
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
