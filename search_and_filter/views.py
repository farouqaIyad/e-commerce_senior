from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from catalog.serializers import ProductSerializer
from .documents import ProductDocument
from django.http import HttpResponse
from elasticsearch_dsl import Q
from django.http import JsonResponse


class SearchProduct(APIView, LimitOffsetPagination):
    product_serializer = ProductSerializer
    search_document = ProductDocument

    def get(self, request, query):
        try:
            q = Q(
                "multi_match",
                query=query,
                fields=[
                    "name",
                ],
                fuzziness="auto",
            )
            search = self.search_document.search().query(q)
            response = search.execute()
            results = self.paginate_queryset(response, request, view=self)
            serializer = self.product_serializer(results, many=True)
            return self.get_paginated_response(serializer.data)

        except Exception as e:
            return HttpResponse(e, status=500)
