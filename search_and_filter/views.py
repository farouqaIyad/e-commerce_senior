from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from catalog.serializers import ProductSerializer
from catalog.models import Product, Stock
from sentence_transformers import SentenceTransformer
from pgvector.django import CosineDistance
import json


class SearchProduct(APIView, LimitOffsetPagination):
    product_serializer = ProductSerializer

    def get(self, request, query):
        model = SentenceTransformer("all-MiniLM-L6-v2")

        query_vector = model.encode(query)
        results = Product.objects.annotate(
            distance=CosineDistance("embedding", query_vector)
        ).order_by("distance")[:25]
        serializer = self.product_serializer(results, many=True)
        return Response(serializer.data)


class completion(APIView, LimitOffsetPagination):
    product_serializer = ProductSerializer

    def get(self, request, query):
        results = Product.objects.filter(name__icontains=query)[:5].values("name")
        return Response({"message": results})


# class change_embedding(APIView):
#     product_serializer = ProductSerializer

#     def get(self, request, format=None):
#         json_file = r"D:\AA\e-commerce\e_commerce\catalog\fixtures\product_details.json"
#         try:
#             # Load existing JSON data
#             with open(json_file, "r") as f:
#                 data = json.load(f)
#         except FileNotFoundError:
#             return Response({"error": "JSON file not found."}, status=404)
#         except json.decoder.JSONDecodeError:
#             return Response({"error": "Invalid JSON format in the file."}, status=400)

#         # Update JSON data with embeddings from the model
#         for json_product in data:
#             json_product['fields']['product'] = str(int(json_product['fields']['product']) + 155)

#         # Write updated JSON data back to the file
#         with open(json_file, "w") as f:
#             json.dump(data, f, indent=2)  # Add indentation for readability
#             f.write('\n')

#         return Response({"message": " updated successfully."})


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
