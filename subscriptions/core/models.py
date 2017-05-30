import os
import pandas as pd
from datetime import datetime
from django.db import models
from subscriptions.core.validators import validate_file

SHIRT_SIZES = (
    ('BL', 'Baby Look'),
    ('P', 'P'),
    ('M', 'M'),
    ('G', 'G'),
    ('GG', 'GG'),
    ('2', 'Infantil 2'),
    ('4', 'Infantil 4'),
    ('6', 'Infantil 6'),
    ('8', 'Infantil 8'),
    ('10', 'Infantil 10'),
    ('12', 'Infantil 12'),
    ('14', 'Infantil 14'),
)

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
    modality = models.CharField('modalidade', max_length=25)
    shirt_size = models.CharField('tamanho da camiseta',
                                  max_length=20, choices=SHIRT_SIZES)
    import_t = models.ForeignKey('Import',
                                 on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Subscription, self).save(*args, **kwargs)


class Import(models.Model):
    origin=models.CharField('origem',max_length=100)
    file = models.FileField(validators=[validate_file])

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super(Import, self).save(*args, **kwargs)
        self._import()

    def _import(self):
        csv = pd.DataFrame.from_csv(self.file.name, sep=';')
        self._create_subscriptions(csv)

    def _file_column(self, subscription_name):
        column_filter = self._columns.filter(
            subscription_name__exact=subscription_name
        )
        return column_filter[0].file_name

    def _file_columns(self):
        columns = self._columns.exclude(subscription_name__exact='ignore')\
                               .values_list('subscription_name', flat=True)
        return { column:self._file_column(column) for column in columns }

    def _create_subscriptions(self, csv):
        self._columns = Column.objects.filter(file_name__in=set(csv.columns))
        records = csv.to_dict('records')
        file_columns = self._file_columns()
        model_instances = [self._new_subscription(record, file_columns)
                           for record in records]

        Subscription.objects.bulk_create(model_instances)

    def _new_subscription(self, record, file_columns):
        shirt_size = ShirtSize.objects.get(
            file_shirt_size__exact=record[file_columns['shirt_size']]
        )
        params = {column:record[file_columns[column]] for column in file_columns}
        if params['date_of_birth']:
            params['date_of_birth'] = datetime.strptime(
                params['date_of_birth'],'%d/%m/%Y'
            ).date()
        params['import_t'] = self

        return Subscription(**params)


class Column(models.Model):
    COLUMNS = (
        ('name', 'name'),
        ('email', 'email'),
        ('name_for_bib_number', 'name_for_bib_number'),
        ('gender', 'gender'),
        ('date_of_birth', 'date_of_birth'),
        ('city', 'city'),
        ('team', 'team'),
        ('shirt_size', 'shirt_size'),
        ('modality', 'modality'),
        ('ignore', 'ignore')
    )

    subscription_name = models.CharField('coluna', max_length=20, choices=COLUMNS)
    file_name = models.CharField(max_length=100, primary_key=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Column, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.file_name)

class ShirtSize(models.Model):
    shirt_size = models.CharField('camiseta', max_length=10, choices=SHIRT_SIZES)
    file_shirt_size = models.CharField(max_length=100, primary_key=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(ShirtSize, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.shirt_size)

    def __eq__(self, other):
        return other == self.shirt_size
