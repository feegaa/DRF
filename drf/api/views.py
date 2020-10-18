from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.views import APIView
from rest_framework import generics, mixins, status, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response 
# from rest_framework.routers import DefaultRouter

# from rest_framework.throttling import UserRateThrottle


from api.models import PostModel
from api.serializers import PostModelSerializer, PostSerializer

# Create your views here.


class PostAPIModelViewsets(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset         = PostModel.objects.all()



class PostAPIGenericViewsets(viewsets.GenericViewSet, 
                            mixins.ListModelMixin, 
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin):

    serializer_class = PostSerializer
    queryset         = PostModel.objects.all()

    # serializer_class   = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]




class PostAPIViewsets(viewsets.ViewSet):
    
    def list(self, request):
        posts = PostModel.objects.all()
        serialized = PostSerializer(posts, many=True)
        return Response(serialized.data)


    def create(self, request):
        data = JSONParser().parse(request)
        serialized = PostSerializer(data=data)

        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)

        return Response(serialized.data, status=status.HTTP_201_CREATED)


    def retrieve(self, request, id=None):
        queryset   = PostModel.objects.all()
        post       = get_object_or_404(queryset, id=id)
        serialized = PostSerializer(post)
        return Response(serialized.data)

    def update(self, request, pk=None):
        post = PostModel.objects.get(id=pk)
        data = JSONParser().parse(request)
        serialized = PostSerializer(post, data=data)

        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)



class PostGenericAPIView(generics.GenericAPIView, 
                        mixins.ListModelMixin, 
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin, 
                        mixins.UpdateModelMixin, 
                        mixins.DestroyModelMixin):

    serializer_class = PostSerializer
    queryset         = PostModel.objects.all()
    lookup_field     = 'id'
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    # authentication_classes = [TokenAuthentication]
    permission_classes     = [IsAuthenticated]

    def get(self, request, id):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # def put(self, request, id=None):
    #     return self.update(request, id)   

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class PostAPI(APIView):

    def get(self, request):
        posts = PostModel.objects.all()
        serialized = PostSerializer(posts, many=True)
        return JsonResponse(serialized.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        serialized = PostSerializer(data=data)

        if serialized.is_valid():
            serialized.save()
            return JsonResponse(serialized.data, status=status.HTTP_201_CREATED)



class PostDetailAPI(APIView):

    def get_object(self, id):
        try:
            return PostModel.objects.get(id=id)
        except ObjectDoesNotExist:
            return False

    def get(self, request, id):
        post = self.get_object(id)
        serialized = PostSerializer(post)
        return JsonResponse(serialized.data)

    def put(self, request, id):
        post = self.get_object(id)
        data = JSONParser().parse(request)
        serialized = PostSerializer(post, data=data)

        if serialized.is_valid():
            serialized.save()
            return JsonResponse(serialized.data, status=status.HTTP_202_ACCEPTED)

        return JsonResponse(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        post = self.get_object(id)
        post.delete()
        return HttpResponse(None, status=204)
        

@api_view(['GET'])
def postList(request):
    
    if request.method == "GET":
        posts = PostModel.objects.all()
        serialized = PostSerializer(posts, many=True)
        return JsonResponse(serialized.data, safe=False)

    else:
        return JsonResponse(None, status=400)

@api_view(['POST'])
@csrf_exempt
def addPost(request):
    
    if request.method == "POST":
        data = JSONParser().parse(request)
        serialized = PostSerializer(data=data)

        if serialized.is_valid():
            serialized.save()
            return JsonResponse(serialized.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['PUT', 'GET', 'DELETE'])
@csrf_exempt
def detail(request, id):
    try:
        post = PostModel.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponse(None, status=403)
    
    if request.method == "GET":
        serialized = PostSerializer(post)
        return JsonResponse(serialized.data)


    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serialized = PostSerializer(post, data=data)

        if serialized.is_valid():
            # print(serialized.data['title'])
            # post.title   = serialized.data['title']
            # post.content = serialized.data['content']
            # post.save()

            serialized.save()
            return JsonResponse(serialized.data, status=status.HTTP_202_ACCEPTED)
        return JsonResponse(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        post.delete()
        return HttpResponse(None, status=204)





# class OncePerDayUserThrottle(UserRateThrottle):
#         rate = '1/day'

# @api_view(['GET'])
# @throttle_classes([OncePerDayUserThrottle])
# def view(request):
#     return Response({"message": "Hello for today! See you tomorrow!"})






# class UpdateName(generics.UpdateAPIView):
#     queryset = ClientUser.objects.all()
#     serializer_class = ClientNameSerializer
#     permission_classes = (permissions.IsAuthenticated,)

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.name = request.data.get("name")
#         instance.save()

#         serializer = self.get_serializer(instance)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         return Response(serializer.data)