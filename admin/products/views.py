import random

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product, User
from products.producer import publish
from products.serializers import ProductSerializer


class ProductViewSet(viewsets.ViewSet):
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(Product, pk=pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = get_object_or_404(Product, pk=pk)
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            publish('product_updated', serializer.data)
            return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            publish('product_created', serializer.data)
            return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = get_object_or_404(Product, pk=pk)
        instance.delete()
        publish('product_deleted', pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAPIView(APIView):

    def get(self, _):
        users = User.objects.all()
        user = random.choice(users)
        return Response({"id": user.id})
