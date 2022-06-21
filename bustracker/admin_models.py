# type: ignore

from sqladmin import ModelAdmin

from .models import Route, Type


class TypeAdmin(ModelAdmin, model=Type):
    pass


class RouteAdmin(ModelAdmin, model=Route):
    column_list = [Route.id, Route.type_name, Route.number]
