from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TinyUserSerializers

class My(APIView):  

    def get(self, request):
        user = request.user
        serializer = TinyUserSerializers(user)
        return Response(serializer.data)
    
    
class getIP(APIView):#위도 경도로 부터 현재 접속 IP로부터 ㅓ동네 검색
    pass

class getQuery(APIView):#검색어 입력 기반 동네 검색
    pass
