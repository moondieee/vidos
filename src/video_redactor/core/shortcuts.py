"""
Django get_object_or_404 and get_list_or_404 for mongoengine Documents and Querysets.
"""
from django.http import Http404
from mongoengine.base.document import BaseDocument
from mongoengine.queryset.base import BaseQuerySet


def _get_queryset(klass):
    """
    Return a QuerySet or a Manager.
    Duck typing in action: any class with a `get()` method (for
    get_object_or_404) or a `filter()` method (for get_list_or_404) might do
    the job.
    """
    # If it is a model class or anything else with ._default_manager
    if hasattr(klass, '_default_manager'):
        return klass._default_manager.all()
    # If it is mongoengine Queryset or Document
    if issubclass(klass, BaseQuerySet):
        return klass.objects.all()
    if issubclass(klass, BaseDocument):
        return klass.objects.all()

    return klass


def get_object_or_404(klass, *args, **kwargs):
    """
    Use get() to return an object, or raise a Http404 exception if the object
    does not exist.

    klass may be a Document, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
    one object is found.
    """
    queryset = _get_queryset(klass)
    if not hasattr(queryset, 'get'):
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            "First argument to get_object_or_404() must be a Document, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )

    try:
        return queryset.get(*args, **kwargs)
    except queryset._document.DoesNotExist:
        raise Http404('No %s matches the given query.' % queryset._document)


def get_list_or_404(klass, *args, **kwargs):
    """
    Use filter() to return a list of objects, or raise a Http404 exception if
    the list is empty.

    klass may be a Document, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the filter() query.
    """
    queryset = _get_queryset(klass)
    if not hasattr(queryset, 'filter'):
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            "First argument to get_list_or_404() must be a Document, Manager, or "
            "QuerySet, not '%s'." % klass__name
        )
    obj_list = list(queryset.filter(*args, **kwargs))
    if not obj_list:
        raise Http404('No %s matches the given query.' % queryset._document)
    return obj_list
