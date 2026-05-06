from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, Seller, SellerWallet, Client, Cart, Favorite, Tag, LeadStatus
from django.contrib.auth import get_user_model,authenticate


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "date_of_birth",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.is_verified = False
        user.save()
        return user


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)


class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = "__all__"


class SellerWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerWallet
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class LeadStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadStatus
        fields = "__all__"
    

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "phone_number", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_phone_number(self, value):
        if not value.startswith("+"):
            raise serializers.ValidationError("Phone must start with +")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError("Wrong username or password")
        return user
    
def create(self, validated_data):
    user = User.objects.create_user(**validated_data)

    if user.role == "user":
        Client.objects.create(user=user)
    elif user.role == "seller":
        Seller.objects.create(user=user, name=user.username)

    return user