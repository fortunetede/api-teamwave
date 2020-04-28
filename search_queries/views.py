from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_200_OK,  HTTP_400_BAD_REQUEST)
from rest_framework.permissions import AllowAny
from django.core.paginator import Paginator
import json
# Create your views here.

def paginated_response(paginated_questions, page_results):
    payload = {
        "Previous": "",
        "Next":"",
        "Count": paginated_questions.count,
        "results": page_results.object_list
    }
    return payload


class QuestionFilter(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        try:
            page = request.data.get('page', None)
            pagesize = request.data.get('pagesize', None)
            fromdate = request.data.get('fromdate', None)
            todate = request.data.get('todate', None)
            order = request.data.get('order', None)
            _min = request.data.get('min', None)
            _max = request.data.get('max', None)
            sort = request.data.get('sort', None)
            tagged = request.data.get('tagged', None)

            params = '?page=%s&pagesize=%s&order=%s&min=%s&max=%s&sort=%s&fromdate=%s&todate=%s&site=stackoverflow'%(page,pagesize,order,_min,_max,sort,fromdate,todate)
            resp = requests.get('https://api.stackexchange.com/2.2/questions%s'%(params))
            myqueryset = json.loads(resp.text)['items']
        

            paginate_number = request.data.get('paginate_number', None)
            paginated_questions = Paginator(myqueryset, pagesize)
            # print("paginated_questions.previous_page_number()", paginated_questions.previous_page_number()) 
            page_results = paginated_questions.page(paginate_number)
            # print("main results", paginated_questions.count)
            final_result = paginated_response(paginated_questions, page_results)
            print("paginated result", final_result)
            return Response(final_result, status=HTTP_200_OK)
        except:
            return Response("Sorry query could not be retrived", status=HTTP_400_BAD_REQUEST)

      
