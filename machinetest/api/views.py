from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

# Create your views here.


class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ClientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            client = Client.objects.get(id=self.kwargs['client_id'])
            serializer.save(client=client, created_by=self.request.user)
        except Client.DoesNotExist:
            raise NotFound(detail="Client not found")


class UserProjectsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        projects = request.user.projects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)