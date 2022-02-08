from tinysqlbuilder.builder import QueryBuilder
from tinysqlbuilder.sql import union, union_all


def test_union():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.where("price > 10")
    query1 = builder.build()

    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.where("price < 20")
    query2 = builder.build()

    query = union(query1, query2)
    assert (
        query
        == "SELECT name, price FROM items WHERE price > 10 UNION SELECT name, price FROM items WHERE price < 20"
    )


def test_union_all():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.where("price > 10")
    query1 = builder.build()

    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.where("price < 20")
    query2 = builder.build()

    query = union_all(query1, query2)
    assert (
        query
        == "SELECT name, price FROM items WHERE price > 10 UNION ALL SELECT name, price FROM items WHERE price < 20"
    )
