from sqladmin import ModelAdmin  # type: ignore

from .models import Type


class TypeAdmin(ModelAdmin, model=Type):  # type: ignore
    pass
