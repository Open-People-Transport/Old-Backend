# type: ignore

from sqladmin import ModelAdmin

from bustracker.database.models import Node, Route, Stop, Type


class TypeAdmin(ModelAdmin, model=Type):
    pass


class RouteAdmin(ModelAdmin, model=Route):
    column_list = [Route.id, Route.type_name, Route.number]


class NodeAdmin(ModelAdmin, model=Node):
    column_list = [Node.id, Node.name]


class StopAdmin(ModelAdmin, model=Stop):
    column_list = [Stop.id, Stop.node_id, Stop.location]
