import os
import pandas as pd
from datetime import datetime
from django.db import models

class Subscription(models.Model):
    GENDERS = (
        ('F', 'Feminino'),
        ('M', 'Masculino'),
    )

    name = models.CharField('nome', max_length=200)
    email = models.EmailField('e-mail')
    name_for_bib_number = models.CharField('nome para número de peito',
                                           max_length=200, blank=True)
    gender = models.CharField('sexo', max_length=1, choices=GENDERS)
    date_of_birth = models.DateField('data de nascimento')
    city = models.CharField('cidade', max_length=100, blank=True)
    team = models.CharField('equipe', max_length=100, blank=True)
    shirt_size = models.CharField('tamanho da camiseta', max_length=25)
    modality = models.CharField('modalidade', max_length=25)
    import_t = models.ForeignKey('Import', on_delete=models.CASCADE, null=True)

class Import(models.Model):
    file = models.FileField()

    def save(self, *args, **kwargs):
        super(Import, self).save(*args, **kwargs)
        self._import()

    def _import(self):
        csv = pd.DataFrame.from_csv(self.file.name, sep=';')
        records = csv.to_dict('records')
        model_instances = [Subscription(
            name=record['*Nome Completo'],
            email=record['E-mail'],
            name_for_bib_number=record['Nome para Numero de Peito'],
            gender=record['*Sexo (M ou F)'],
            date_of_birth=datetime.strptime(
                record['*Data Nascimento (dd/mm/aaaa)'],
                '%d/%m/%Y').date(),
            city=record['Cidade'],
            team=record['Equipe'],
            shirt_size=record['Tamanho da Camiseta'],
            modality=record['Modalidade'],
            import_t=self,
        ) for record in records]

        Subscription.objects.bulk_create(model_instances)
