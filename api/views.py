from django.shortcuts import render

from api.models import Task
from django.contrib.auth.models import User
from rest_framework import viewsets
from .Serializers import * 
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count
from rest_framework import status
from django.db import transaction
import csv


class TaskViewSet(viewsets.ViewSet):

    def list(self, request):
        val = request.GET
        filter_camp = request.GET['field'] if request.GET['order'] == 'desc' else '-'+request.GET['field']
        queryset = Task.objects.filter(status = True , title__icontains = request.GET['title']).order_by(filter_camp)
        serializers = TaskSerializer(queryset, many=True)
        return Response(serializers.data)

    #save file csv in database
    #/task/arquivo/
    @action(methods=["POST"] , detail=False)
    def arquivo(self, request):
        try:
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(decoded_file)

            for row in csv_reader:
                item = Task(
                    hostname = row['ASSET - HOSTNAME'],
                    ip_address = row['ASSET - IP_ADDRESS'],
                    title= row['VULNERABILITY - TITLE'],
                    severity = row['VULNERABILITY - SEVERITY'],
                    cvss = row['VULNERABILITY - CVSS'],
                    publication_date = row['VULNERABILITY - PUBLICATION_DATE'],
                )
                item.save()

            return Response({
                'message': 'Arquivo salvo com sucesso',
                'success': True
            }, status=status.HTTP_200_OK)

        except:
            return Response({
                'message': 'Arquivo fora do Padrão',
                'success': True
            }, status=status.HTTP_200_OK)

    #finish Item
    #/task/finish/
    @action(methods=["POST"] , detail=False)
    def finish(self, request ):
        value = request.data['identifier']
        item = Task.objects.filter(pk = value).get()
        item.status = False
        item.save()

        return Response({
            'message': request.POST,
            'success': True
        }, status=status.HTTP_200_OK)
