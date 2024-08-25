from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from inventory.serializers import ProductSerializer
from inventory.models import Product, Stock
from sentence_transformers import SentenceTransformer
from pgvector.django import CosineDistance, L2Distance
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


class SearchProduct(APIView, LimitOffsetPagination):
    product_serializer = ProductSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, query):
        model = SentenceTransformer("all-MiniLM-L6-v2")
        query_vector = model.encode(query)
        results = (
            Product.objects.with_wishlist_status(request.user)
            .annotate(distance=CosineDistance("embedding", query_vector))
            .filter(
                distance__lte=0.75,
            )
            .order_by("distance")[:25]
        )
        serializer = self.product_serializer(results, many=True)

        return Response({"products": serializer.data})


class completion(APIView, LimitOffsetPagination):
    product_serializer = ProductSerializer

    def get(self, request, format=None):
        results = Product.objects.all().values_list("name", flat=True)
        return Response({"message": results})


class supplierSearchProduct(APIView, LimitOffsetPagination):
    product_serializer = ProductSerializer

    def get(self, request, query):
        results = Product.objects.filter(
            name__icontains=query, supplier=request.user.supplierprofile
        )
        serializer = self.product_serializer(instance=results, many=True)
        return Response(serializer.data)


class FiltersList(APIView):
    product_serializer = ProductSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        filters = {}
        if "min_price" in request.data:
            filters["main_price__gte"] = request.data["min_price"]
        if "max_price" in request.data:
            filters["main_price__lte"] = request.data["max_price"]
        if "size" in request.data:
            filters["product_detail__size__in"] = request.data["size"]
        if "brand" in request.data:
            filters["brand__in"] = request.data["brand"]
        filters["category__slug"] = request.data["category"]
        filter_q = Q(**filters)

        queryset = (
            Product.objects.with_wishlist_status(request.user)
            .filter(filter_q)
            .distinct()
        )
        serializer = ProductSerializer(instance=queryset, many=True)
        return Response({"products": serializer.data})


class change_embedding(APIView):
    product_serializer = ProductSerializer

    def get(self, request, format=None):
        model = SentenceTransformer("all-MiniLM-L6-v2")
        all_products = Product.objects.all()
        for product in all_products:
            product.embedding = model.encode(product.name)
            product.save()
        print(all_products[0].embedding)
        return Response({"message": " created embeddings successfully."})


class bestsellers(APIView):
    def get(self, request, format=None):
        products = Product.objects.order_by(
            "product_detail__stock__products_sold"
        ).distinct()
        serializer = ProductSerializer(instance=products, many=True)
        return Response(serializer.data)


class Newly_added(APIView):
    def get(self, request, format=None):
        products = Product.objects.with_wishlist_status(request.user).order_by(
            "date_created"
        )
        serializer = ProductSerializer(instance=products, many=True)
        return Response({"new products": serializer.data})


class Highest_rating(APIView):
    def get(self, request, format=None):
        products = Product.objects.with_wishlist_status(request.user).order_by(
            "-average_rating"
        )
        serializer = ProductSerializer(instance=products, many=True)
        return Response({"best_rating": serializer.data})
