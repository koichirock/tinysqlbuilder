from tinysqlbuilder.builder import QueryBuilder
from tinysqlbuilder.ddl import create_or_replace_table_from_query, create_table_from_query


def test_create_or_replace_table_from_query():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.where("price > 10")
    query = builder.build()

    assert (
        create_or_replace_table_from_query("new_items", query)
        == "CREATE OR REPLACE TABLE new_items AS (SELECT name, price FROM items WHERE price > 10)"
    )


def test_create_table_from_query():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.where("price > 10")
    query = builder.build()

    assert (
        create_table_from_query("new_items", query)
        == "CREATE TABLE new_items AS (SELECT name, price FROM items WHERE price > 10)"
    )
