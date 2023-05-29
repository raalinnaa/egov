from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from users.models import User
from utils import messages


class UserRegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        required=True,
        min_length=2,
        max_length=128,
    )
    last_name = serializers.CharField(
        required=False,
        min_length=2,
        max_length=128,
    )
    phone = serializers.CharField(
        required=False,
        min_length=5,
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^\+?77(\d{9})$',
            ),
            UniqueValidator(
                queryset=User.objects.all(),
            )
        ],
    )
    email = serializers.EmailField(
        required=True,
        min_length=3,
        max_length=255,
        validators=[
            UniqueValidator(
                queryset=User.objects.all()
            )
        ],
    )
    password = serializers.CharField(
        required=False,
        min_length=8,
        max_length=64,
        write_only=True,
    )
    token = serializers.CharField(
        read_only=True,
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'phone',
            'email',
            'password',
            'token',
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.get_or_create(user=user)
        token, _ = Token.objects.get_or_create(user=user)
        user.token = token.key
        return user

    def create_staff_user(self, validated_data):
        user = User.objects.create_staff_user(**validated_data)
        Token.objects.get_or_create(user=user)
        token, _ = Token.objects.get_or_create(user=user)
        user.token = token.key
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        min_length=3,
        max_length=255,
        write_only=True,
    )
    password = serializers.CharField(
        required=True,
        min_length=8,
        max_length=64,
        write_only=True,
    )
    token = serializers.CharField(
        required=False,
        read_only=True,
    )

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'token',
        )

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        user = User.objects.filter(
            email=email
        ).first()
        if user is None:
            raise serializers.ValidationError(
                messages.USER_NOT_FOUND
            )
        if not user.is_active:
            raise serializers.ValidationError(
                messages.USER_NOT_ACTIVE
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                messages.INVALID_PASSWORD
            )
        token, _ = Token.objects.get_or_create(user=user)
        data['token'] = token.key
        return data


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(
        required=False,
        min_length=5,
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^\+?77(\d{9})$',
            ),
        ],
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'phone',
        )


class UserUpdatePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        required=True,
        min_length=8,
        max_length=64,
        write_only=True,
    )

    new_password = serializers.CharField(
        required=True,
        min_length=8,
        max_length=64,
        write_only=True,
    )
    repeat_password = serializers.CharField(
        required=True,
        min_length=8,
        max_length=64,
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            'old_password',
            'new_password',
            'repeat_password',
        )

    def validate(self, attrs):
        old_password = attrs.get('old_password', None)
        new_password = attrs.get('new_password', None)
        repeat_password = attrs.get('repeat_password', None)
        if not self.context['request'].user.check_password(old_password):
            raise serializers.ValidationError(
                messages.INVALID_PASSWORD
            )
        if new_password != repeat_password:
            raise serializers.ValidationError(
                messages.PASSWORDS_NOT_MATCH
            )
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
