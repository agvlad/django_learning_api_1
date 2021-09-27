from .models import Network, Router
from .serializers import NetworkReadSerializer, NetworkWriteSerializer,\
    RouterReadSerializer, RouterWriteSerializer

from django.http import Http404

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class NetworkList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        networks = Network.objects.all()
        serializer = NetworkReadSerializer(networks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NetworkWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NetworkDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_network(self, pk):
        try:
            return Network.objects.get(id=pk)
        except Network.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        network = self.get_network(pk)
        serializer = NetworkReadSerializer(network, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        network = self.get_network(pk)
        serializer = NetworkWriteSerializer(network, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        network = self.get_network(pk)
        network.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RouterList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        routers = Router.objects.all()
        serializer = RouterReadSerializer(routers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RouterWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RouterDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_router(self, pk):
        try:
            return Router.objects.get(id=pk)
        except Router.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        router = self.get_router(pk)
        serializer = RouterReadSerializer(router, many=False)
        return Response(serializer.data)

    def delete(self, request, pk):
        router = self.get_router(pk)
        router.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        router = self.get_router(pk)
        serializer = RouterWriteSerializer(router, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
