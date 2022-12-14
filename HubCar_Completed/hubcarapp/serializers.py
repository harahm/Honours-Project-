from rest_framework import serializers

from hubcarapp.models import Garage, \
    Item, \
    Customer, \
    Driver, \
    Order, \
    OrderDetails

class GarageSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self, garage):
        request = self.context.get('request')
        logo_url = garage.logo.url
        return request.build_absolute_uri(logo_url)

    class Meta:
        model = Garage
        fields = ("id", "name", "phone", "address", "logo")

class ItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, item):
        request = self.context.get('request')
        image_url = item.image.url
        return request.build_absolute_uri(image_url)

    class Meta:
        model = Item
        fields = ("id", "name", "short_description", "image", "price")

# ORDER SERIALIZER
class OrderCustomerSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.get_full_name")

    class Meta:
        model = Customer
        fields = ("id", "name", "avatar", "phone", "address")

class OrderDriverSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.get_full_name")

    class Meta:
        model = Customer
        fields = ("id", "name", "avatar", "phone", "address")

class OrderGarageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garage
        fields = ("id", "name", "phone", "address")

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "name", "price")

class OrderDetailsSerializer(serializers.ModelSerializer):
    item = OrderItemSerializer()

    class Meta:
        model = OrderDetails
        fields = ("id", "item", "quantity", "sub_total")

class OrderSerializer(serializers.ModelSerializer):
    customer = OrderCustomerSerializer()
    driver = OrderDriverSerializer()
    garage = OrderGarageSerializer()
    order_details = OrderDetailsSerializer(many = True)
    status = serializers.ReadOnlyField(source = "get_status_display")

    class Meta:
        model = Order
        fields = ("id", "customer", "garage", "driver", "order_details", "total", "status", "address")
