from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from . pagination import *
from . serializers import *
from . models import Vaga

# Create your views here.


class VagaList(APIView):
    def get(self, request):
        try:
            lista_vagas = Vaga.objects.all()
            paginator = PaginacaoVagas()
            result_page = paginator.paginate_queryset(lista_vagas, request)
            serializer = VagaSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception:
            return JsonResponse({'mensagem': 'Ocorreu um erro no servidor.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = VagaSerializer(data=request.data)
            empresa_id = request.data['empresa']
            Empresa.objects.get(pk=empresa_id)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Empresa.DoesNotExist:
            return JsonResponse({'mensagem': 'A empresa a ser relacionada não existe.'},
                                status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'mensagem': 'Ocorreu um erro no servidor.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VagaDetalhes(APIView):
    def get(self, request, pk):
        try:
            if pk == '0':
                return JsonResponse({'mensagem': 'O ID deve ser maior que zero.'},
                                    status=status.HTTP_400_BAD_REQUEST)
            vaga = Vaga.objects.get(pk=pk)
            serializer = VagaSerializer(vaga)
            return Response(serializer.data)
        except Vaga.DoesNotExist:
            return JsonResponse({'mensagem': 'A vaga não existe.'},
                                status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'mensagem': 'Ocorreu um erro no servidor.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            if pk == "0":
                return JsonResponse({'mensagem': 'O ID deve ser maior que zero.'},
                                    status=status.HTTP_400_BAD_REQUEST)
            vaga = Vaga.objects.get(pk=pk)
            serializer = VagaSerializer(vaga, data=request.data)
            empresa_id = request.data['empresa']
            Empresa.objects.get(pk=empresa_id)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Vaga.DoesNotExist:
            return JsonResponse({'mensagem': 'A vaga não existe.'},
                                status=status.HTTP_404_NOT_FOUND)
        except Empresa.DoesNotExist:
            return JsonResponse({'mensagem': 'A empresa a ser relacionada não existe.'},
                                status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'mensagem': 'Ocorreu um erro no servidor.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            if pk == "0":
                return JsonResponse({'mensagem': 'O ID deve ser maior que zero.'},
                                    status=status.HTTP_400_BAD_REQUEST)
            vaga = Vaga.objects.get(pk=pk)
            vaga.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Vaga.DoesNotExist:
            return JsonResponse({'mensagem': 'A vaga não existe.'},
                                status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'mensagem': 'Ocorreu um erro no servidor.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmpresaList(APIView):
    def get(self, request):
        try:
            lista_empresas = Empresa.objects.all()
            paginator = PaginacaoEmpresas()
            result_page = paginator.paginate_queryset(lista_empresas, request)
            serializer = EmpresaSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception:
            return JsonResponse({'mensagem': 'Ocorreu um erro no servidor.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = EmpresaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return JsonResponse({'mensagem': 'Ocorreu um erro no servidor.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmpresaDetalhes(APIView):
    def get(self, request, pk):
        try:
            if pk == "0":
                return JsonResponse({'mensagem': 'O ID deve ser maior que zero.'},
                                    status=status.HTTP_400_BAD_REQUEST)
            empresa = Empresa.objects.get(pk=pk)
            serializer = EmpresaSerializer(empresa)
            return Response(serializer.data)
        except Empresa.DoesNotExist:
            return JsonResponse({'mensagem': 'A empresa não existe.'},
                                status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'mensagem': 'Ocorreu um erro no servidor.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            if pk == '0':
                return JsonResponse({'mensagem': 'O ID deve ser maior que zero.'},
                                    status=status.HTTP_400_BAD_REQUEST)
            empresa = Empresa.objects.get(pk=pk)
            serializer = EmpresaSerializer(empresa, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        except Empresa.DoesNotExist:
            return JsonResponse({'mensagem': 'A empresa não existe.'},
                                status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'mensagem': 'Ocorreu um erro no servidor.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            if pk == '0':
                return JsonResponse({'mensagem': 'O ID deve ser maior que zero.'},
                                    status=status.HTTP_400_BAD_REQUEST)
            vagas_empresas = Vaga.objects.filter(empresa_id=pk)
            if vagas_empresas:
                return JsonResponse({'mensagem': 'A empresa não pode ser excluída,'
                                                 ' pois há vagas relacionadas a ela.'},
                                    status=status.HTTP_403_FORBIDDEN)
            empresa = Empresa.objects.get(pk=pk)
            empresa.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Empresa.DoesNotExist:
            return JsonResponse({'mensagem': 'A empresa não existe.'},
                                status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'mensagem': 'Ocorreu um erro no servidor.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
