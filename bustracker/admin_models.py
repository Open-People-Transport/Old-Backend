# type: ignore

from sqladmin import ModelAdmin

from .models import Node, Route, Type


class TypeAdmin(ModelAdmin, model=Type):
    pass


class RouteAdmin(ModelAdmin, model=Route):
    column_list = [Route.id, Route.type_name, Route.number]


class NodeAdmin(ModelAdmin, model=Node):
    column_list = [Node.id, Node.name]
