from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^vagas$', VagaList.as_view()),
    url(r'^vagas/(?P<pk>[0-9]+)$', VagaDetalhes.as_view()),
    url(r'^empresas$', EmpresaList.as_view()),
    url(r'^empresas/(?P<pk>[0-9]+)$', EmpresaDetalhes.as_view())
]