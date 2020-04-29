from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_200_OK,  HTTP_400_BAD_REQUEST)
from rest_framework.permissions import AllowAny

from django.core.cache import cache
import json
from search_queries.utils import set_cache, get_cache, custom_paginator
# Create your views here.


class QuestionFilter(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
    # try:
        print("req.data", request.data)
        page = request.data.get('page', None)
        pagesize = request.data.get('pagesize', None)
        fromdate = request.data.get('fromdate', None)
        todate = request.data.get('todate', None)
        order = request.data.get('order', None)
        _min = request.data.get('min', None)
        _max = request.data.get('max', None)
        sort = request.data.get('sort', None)
        tagged = request.data.get('tagged', None)

        query = '?page=%s&pagesize=%s&order=%s&min=%s&max=%s&sort=%s&fromdate=%s&todate=%s&site=stackoverflow'%(page,pagesize,order,_min,_max,sort,fromdate,todate)

        if query in cache:
            final_result = get_cache(query)
            return Response(final_result, status=HTTP_200_OK)
        else:
            resp = requests.get('https://api.stackexchange.com/2.2/questions%s'%(query))
            myqueryset = json.loads(resp.text)['items']
            # Pagination
            final_result = custom_paginator(myqueryset, pagesize, page)
            # Cache QUESTION 
            set_cache(query, final_result) 
            return Response(final_result, status=HTTP_200_OK)
    # except:
    #     payload = {
    #         "status": "00",
    #         "results": "Sorry TeamWave Tester! Something bad went on during query"
    #     }
    #     return Response(payload, status=HTTP_400_BAD_REQUEST)

      
