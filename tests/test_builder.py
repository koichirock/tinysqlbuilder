from tinysqlbuilder.builder import QueryBuilder
from tinysqlbuilder.sql import and_, between, eq, ge, gt, in_, le, like, lt, not_, not_eq, or_


def test_select():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    query = builder.build()

    assert query.to_sql() == "SELECT name, price FROM items"


def test_where():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.where("price > 10")
    query = builder.build()

    assert query.to_sql() == "SELECT name, price FROM items WHERE price > 10"


def test_where_and():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.where(and_("price > 10", "price < 20"))
    query = builder.build()

    assert query.to_sql() == "SELECT name, price FROM items WHERE price > 10 AND price < 20"


def test_where_or():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.where(or_("price > 10", "price < 20"))
    query = builder.build()

    assert query.to_sql() == "SELECT name, price FROM items WHERE price > 10 OR price < 20"


def test_where_not():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.where(not_("price > 10"))
    query = builder.build()

    assert query.to_sql() == "SELECT name, price FROM items WHERE NOT price > 10"


def test_where_or_and_and():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.where(
        or_(
            and_("price > 10", "price < 20"),
            and_("price > 30", "price < 40"),
        )
    )
    query = builder.build()

    assert (
        query.to_sql()
        == "SELECT name, price FROM items WHERE (price > 10 AND price < 20) OR (price > 30 AND price < 40)"
    )


def test_where_or_and_and_not():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.where(
        or_(
            and_("price > 10", "price < 20"),
            and_("price > 30", "price < 40"),
            not_("price > 50"),
        )
    )
    query = builder.build()

    assert (
        query.to_sql()
        == "SELECT name, price FROM items WHERE (price > 10 AND price < 20) OR (price > 30 AND price < 40) OR (NOT price > 50)"
    )


def test_where_or_and_or():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.where(
        or_(
            and_("price > 10", "price < 20"),
            or_("price > 30", "price < 40"),
        )
    )
    query = builder.build()

    assert (
        query.to_sql()
        == "SELECT name, price FROM items WHERE (price > 10 AND price < 20) OR (price > 30 OR price < 40)"
    )


def test_join():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.join("categories", "items.catetory_id = categories.id")
    query = builder.build()

    assert (
        query.to_sql()
        == "SELECT name, price FROM items JOIN categories ON items.catetory_id = categories.id"
    )


def test_join_join():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.join("categories", "items.catetory_id = categories.id")
    builder.join("orders", "items.id = orders.item_id")
    query = builder.build()

    assert (
        query.to_sql()
        == "SELECT name, price FROM items JOIN categories ON items.catetory_id = categories.id JOIN orders ON items.id = orders.item_id"
    )


def test_join_subquery():
    subquery_builder = QueryBuilder("categories")
    subquery_builder.select("id")
    subquery_builder.where("name = 'foo'")
    subquery_builder.subquery("ctg")
    subquery = subquery_builder.build()

    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.join(subquery, "items.catetory_id = ctg.id")
    query = builder.build()

    assert (
        query.to_sql()
        == "SELECT name, price FROM items JOIN (SELECT id FROM categories WHERE name = 'foo') AS ctg ON items.catetory_id = ctg.id"
    )


def test_equal():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.where(eq("price", 10))
    query = builder.build()

    assert query.to_sql() == "SELECT name, price FROM items WHERE price = 10"


def test_not_equal():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.where(not_eq("price", 10))
    query = builder.build()

    assert query.to_sql() == "SELECT name, price FROM items WHERE price != 10"


def test_gt():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.where(gt("price", 10))
    query = builder.build()

    assert query.to_sql() == "SELECT name, price FROM items WHERE price > 10"


def test_lt():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.where(lt("price", 10))
    query = builder.build()

    assert query.to_sql() == "SELECT name, price FROM items WHERE price < 10"


def test_ge():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.where(ge("price", 10))
    query = builder.build()

    assert query.to_sql() == "SELECT name, price FROM items WHERE price >= 10"


def test_le():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.where(le("price", 10))
    query = builder.build()

    assert query.to_sql() == "SELECT name, price FROM items WHERE price <= 10"


def test_between():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.where(between("price", 10, 20))
    query = builder.build()

    assert query.to_sql() == "SELECT name, price FROM items WHERE price BETWEEN 10 AND 20"


def test_like():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.where(like("name", "foo"))
    query = builder.build()

    assert query.to_sql() == "SELECT name, price FROM items WHERE name LIKE 'foo'"


def test_in_():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.where(in_("price", [10, 20]))
    query = builder.build()

    assert query.to_sql() == "SELECT name, price FROM items WHERE price IN (10, 20)"


def test_left_outer_join():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.left_outer_join("categories", "items.catetory_id = categories.id")
    query = builder.build()

    assert (
        query.to_sql()
        == "SELECT name, price FROM items LEFT OUTER JOIN categories ON items.catetory_id = categories.id"
    )


def test_right_outer_join():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.right_outer_join("categories", "items.catetory_id = categories.id")
    query = builder.build()

    assert (
        query.to_sql()
        == "SELECT name, price FROM items RIGHT OUTER JOIN categories ON items.catetory_id = categories.id"
    )


def test_full_outer_join():
    builder = QueryBuilder("items")
    builder.select("name", "price")
    builder.full_outer_join("categories", "items.catetory_id = categories.id")
    query = builder.build()

    assert (
        query.to_sql()
        == "SELECT name, price FROM items FULL OUTER JOIN categories ON items.catetory_id = categories.id"
    )
