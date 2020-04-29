from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_200_OK,  HTTP_400_BAD_REQUEST)
from rest_framework.permissions import AllowAny

from django.core.cache import cache
import json
from django.core.paginator import EmptyPage, Paginator
from search_queries.utils import set_cache, get_cache, custom_paginator, date_to_seconds
# Create your views here.



class QuestionFilter(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        try:
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
            client_page_pagination = request.data.get('client_page_pagination', None)
            

            if pagesize == "":
                pagesize = 1

            if page == "":
                page = 1
            if fromdate:
                fromdate = date_to_seconds(fromdate)
            if todate:
                todate = date_to_seconds(todate)
            if _min:
                _min = date_to_seconds(_min)
            if _max:
                _max = date_to_seconds(_max)

            query = '?page=%s&pagesize=%s&order=%s&min=%s&max=%s&sort=%s&fromdate=%s&todate=%s&tagged=%s&site=stackoverflow'%(page,pagesize,order,_min,_max,sort,fromdate,todate,tagged)
            cache_query = '?client_page_pagination=%s&page=%s&pagesize=%s&order=%s&min=%s&max=%s&sort=%s&fromdate=%s&todate=%s&tagged=%s&site=stackoverflow'%(client_page_pagination,page,pagesize,order,_min,_max,sort,fromdate,todate,tagged)
            
            print("query", query)
            if cache_query in cache:
                final_result = get_cache(cache_query)
                return Response(final_result, status=HTTP_200_OK)
            else:
                resp = requests.get('https://api.stackexchange.com/2.2/questions%s'%(query))
                print("main guy", json.loads(resp.text))
                if json.loads(resp.text)['items']:
                    myqueryset = json.loads(resp.text)['items']
                    # Pagination
                    final_result = custom_paginator(myqueryset, pagesize,client_page_pagination )
                    # Cache QUESTION 
                    set_cache(cache_query, final_result) 
                    return Response(final_result, status=HTTP_200_OK)
                else:
                    payload = {
                        "results": "Results not found"
                    }
                    return Response(payload)

        except:
            payload = {
                "results": "Sorry TeamWave Tester! Something bad went on during query"
            }
            return Response(payload)

    
