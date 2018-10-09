from django.db import connections

from sphinxql.configuration.configurators import DJANGO_TO_SPHINX_VENDOR
from sphinxql.manager import IndexManager
from sphinxql import indexes, fields

from .models import Document, CharPrimaryKeyDocument


class Manager(IndexManager):

    def get_queryset(self):
        return super(Manager, self).get_queryset().filter(number__in=[2, 4, 6])


class DocumentIndex(indexes.Index):
    summary = fields.String(model_attr='summary')
    text = fields.IndexedString(model_attr='text')

    date = fields.Date(model_attr='date')
    added_time = fields.DateTime(model_attr='added_time')

    number = fields.Integer(model_attr='number')

    other_objects = Manager()
    objects = IndexManager()

    class Meta:
        model = Document

vendor = connections['default'].vendor
if vendor == 'postgresql':
    sql_query = '''SELECT CAST(CAST(CONCAT('x', id) AS BIT(32)) AS INT) AS id, id AS uid, "text" FROM queryset_charprimarykeydocument'''
elif vendor == 'mysql':
    sql_query = '''SELECT CONV(id, 16, 10) AS id, id AS uid, `text` FROM queryset_charprimarykeydocument'''


class CharPrimaryKeyDocumentIndex(indexes.Index):
    uid = fields.String(model_attr='id')
    text = fields.Text(model_attr='text')

    class Meta:
        model = CharPrimaryKeyDocument
        source_params = {
            'sql_query': sql_query
        }

    def get_pk(self):
        return self.uid
