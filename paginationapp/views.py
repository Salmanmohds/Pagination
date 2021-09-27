from rest_framework import filters
from django_filters import rest_framework as filters
from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework import pagination
import math
from .models import Contact
from .serializers import ContactSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from django.db.models import Q
from datetime import datetime, timedelta
#Custom pagination starting

class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })

# TODO:-
class ContactView(APIView):
    pagination_class = CustomPagination
    PAGE_SIZE = 6
    def get(self, request):
        p = int(request.GET.get('page', 1))
        contacts = Contact.objects.all()
        # offer_start_date = datetime.today()
        # offer_end_date = offer_start_date + timedelta(days=6)
        # data = Contact.objects.filter(created_at__range=[offer_start_date, offer_end_date])
        paginator = Paginator(contacts, self.PAGE_SIZE)  # Show 25 contacts per page
        page = paginator.get_page(p)
        serializer = ContactSerializer([i for i in page.object_list], many=True)
        print((serializer))
        nextpage = page.next_page_number() if page.has_next() else None
        prevpage = page.previous_page_number() if page.has_previous() else None
        pages = {
            "current_page": p,
            "next": nextpage,
            "previous": prevpage,
            "per_page": self.PAGE_SIZE,
            "last_page": math.ceil(paginator.count / self.PAGE_SIZE),
            "total_pages": paginator.num_pages,
            "total_records": paginator.count
        }

        return Response({
            "pagination": pages,
            "results": serializer.data
        }, status=status.HTTP_200_OK)