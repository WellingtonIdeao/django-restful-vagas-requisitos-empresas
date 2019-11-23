from django.db import models

# Create your models here.
TIPO_CONTRATO_CHOICES = (
    ('PJ', 'Pesssoa Jurídica'),
    ('CLT', 'Consolidação das leis do Trabalho')
)


class Empresa(models.Model):
    nome_fantasia = models.CharField(max_length=50, null=False)
    cnpj = models.CharField(max_length=20, null=False)
    email = models.EmailField(null=False)


class Vaga(models.Model):
    titulo = models.CharField(max_length=30, null=False)
    descricao = models.TextField(null=False)
    salario = models.FloatField(null=False)
    tipo_contrato = models.CharField(max_length=50,
                                     choices=TIPO_CONTRATO_CHOICES, null=False)
    status = models.BooleanField(default=1, null=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo


class Requisito(models.Model):
    descricao = models.TextField(null=False)
    vaga = models.ForeignKey(Vaga, related_name='requisitos_vaga',
                             on_delete=models.CASCADE)
