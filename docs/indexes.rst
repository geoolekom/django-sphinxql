Indexes API
===========

.. currentmodule:: sphinxql

This document explains how Django-SphinxQL maps a Django model into a Sphinx
index.

Sphinx uses a SQL query to retrieve data from a relational database to index it.
This means that Django-SphinxQL must know:

1. what you want to index (e.g. what data)
2. how you want to index it (e.g. type)

In the same spirit of Django, Django-SphinxQL defines an ORM for you to answer
those questions. For example::

    # indexes.py
    from sphinxql import fields, indexes
    from myapp import models

    class PostIndex(indexes.Index):
        text = fields.Text('text')  # Post has the model field ``text``
        date = fields.Date('added_date')
        summary = fields.Text('summary')
        # `Post` has a foreign key to a `Blog`, and blog has a name.
        blog_name = fields.Text('blog__name')

        class Meta:
            model = models.Post  # the model we are indexing

The ``fields`` and the ``Meta.model`` identify the "what"; the specific field type,
e.g. ``Text``, identifies the "how". In the following sections the complete API
is presented.

API references
--------------

Index
~~~~~

.. class:: indexes.Index

    :class:`~indexes.Index` is an ORM to Sphinx-index a Django Model. It works in
    a similar fashion to a Django model: you set up the :class:`fields
    <fields.Field>`, and it constructs a Sphinx index out of those fields.

    Formally, when an index is declared, it is registered in the
    :class:`~sphinxql.configuration.configurators.IndexConfigurator` so
    Django-SphinxQL configures it in Sphinx.

    An index is always composed by two components: a set of :class:`fields
    <fields.Field>` that you declare as class attributes and a class ``Meta``:

    .. class:: Meta

        Used to declare Django-SphinxQL related options.
        An index must always define the ``model`` of its Meta:

        .. attribute:: model

            The model of this index. E.g. ``model = blog.models.Post``.

        In case you want to index only particular instances, you can define the
        class attribute ``query``:

        .. attribute:: query

            Optional. The query Sphinx uses to index its data, e.g.
            ``query = models.Post.objects.filter(date__year__gt=2000)``. If not
            set, Django-SphinxQL uses ``.objects.all()``. This is useful if you
            want to construct indexes for specific sets of instances.

        .. _ranged-queries: http://sphinxsearch.com/docs/current.html#ranged-queries

        .. attribute:: range_step

            Optional. Defining it automatically enables ranged-queries_.
            This integer defines the number of rows per query retrieved during
            indexing. It increases the number of queries during indexing, but
            reduces the amount of data transfer on each query.

        In case you want to override Sphinx settings only to this particular
        index, you can also define the following class attributes:

        .. attribute:: source_params

            A dictionary of Sphinx options to override Sphinx settings of
            ``source`` for this particular index.

            See how to use in :ref:`override-settings`.

        .. attribute:: index_params

            A dictionary of Sphinx options to override Sphinx settings of
            ``index`` for this particular index.

            See how to use in :ref:`override-settings`.

Field
~~~~~

Django-SphinxQL uses fields to identify which attributes from a Django model
are indexed:

.. _attribute: http://sphinxsearch.com/docs/current.html#attributes
.. _search field: http://sphinxsearch.com/docs/current.html#fields

.. class:: fields.Field

    A field to be added to an :class:`~indexes.Index`. A field is always mapped
    to a Django queryset, set on its initialization::

        my_indexed_text = FieldType('text')  # Index.Meta.model contains `text =
        ...`

    You can use both Django's F expressions or lookup expressions to index
    related fields or concatenate two fields. For instance,
    `TextField('article__text')`.

    Fields are then mapped to a `search field`_ or an `attribute`_ of Sphinx:

    * search fields are indexed for text search, and thus are used for
      textual searches with :meth:`~sphinxql.query.SearchQuerySet.search`.

    * attributes are used to filter and order the search results (see
      :meth:`~sphinxql.query.SearchQuerySet.search_filter` and
      :meth:`~sphinxql.query.SearchQuerySet.search_order_by`). They cannot be
      used in textual search.

    The following fields are implemented in Django-SphinxQL:

    * ``Text``: a search field (Sphinx equivalent of no field declaration).
    * ``IndexedString``: attribute and search field (``sql_field_string``).
    * ``String``: (non-indexed) attribute for strings (``sql_attr_string``).
    * ``Date``: attribute for dates (``sql_attr_timestamp``).
    * ``DateTime``: attribute for datetimes (``sql_attr_timestamp``).
    * ``Float``: attribute for floats (``sql_attr_float``).
    * ``Bool``: attribute for booleans (``sql_attr_bool``).
    * ``Integer``: attribute for integers (``sql_attr_bigint``).

    To simply index a Django field, use ``Text``. If you need an attribute to filter
    or order your search results, use any of the attributes. Typically
    ``IndexedString`` is only needed if you want to use Sphinx without hitting
    Django's database (e.g. you redundantly store the data on Sphinx, query Sphinx
    and use the results of it.

    .. _unix timestamp: https://en.wikipedia.org/wiki/Unix_time

    Note that Sphinx ``sql_attr_timestamp`` is stored as a `unix timestamp`_,
    so Django-SphinxQL only supports dates/times since 1970.
