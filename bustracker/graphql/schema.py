import strawberry
from strawberry import Schema


@strawberry.type
class Query:
    pass


schema = Schema(Query)
