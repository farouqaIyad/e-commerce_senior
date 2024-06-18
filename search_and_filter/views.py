from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from catalog.serializers import ProductSerializer
from catalog.models import Product, Stock
from sentence_transformers import SentenceTransformer
from pgvector.django import CosineDistance


class SearchProduct(APIView, LimitOffsetPagination):
    product_serializer = ProductSerializer

    def get(self, request, query):
        model = SentenceTransformer("all-MiniLM-L6-v2")

        query_vector = model.encode(query)
        results = Product.objects.annotate(
            distance=CosineDistance("embedding", query_vector)
        ).filter(distance__lte=0.75).order_by("distance")[:25]
        serializer = self.product_serializer(results, many=True)
        
        return Response(serializer.data)


class completion(APIView, LimitOffsetPagination):
    product_serializer = ProductSerializer

    def get(self, request, query):
        results = Product.objects.filter(name__icontains=query)[:5].values("name")
        return Response({"message": results})


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
        products = Product.objects.order_by("date_created")[:20]
        serializer = ProductSerializer(instance=products, many=True)
        return Response(serializer.data)


class Highest_rating(APIView):
    def get(self, request, format=None):
        products = Product.objects.order_by("average_rating")[:20]
        serializer = ProductSerializer(instance=products, many=True)
        return Response(serializer.data)
