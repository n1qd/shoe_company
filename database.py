import pymysql
import pymysql.cursors


class Database:
    """Слой доступа к данным магазина обуви (pymysql, БД shoes_company)."""

    def __init__(self):
        self._cfg = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'password',
            'database': 'shoes_company',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor,
        }

    def _conn(self):
        return pymysql.connect(**self._cfg)

    def _fetch_all(self, sql, params=None):
        con = self._conn()
        try:
            with con.cursor() as cur:
                cur.execute(sql, params or ())
                return cur.fetchall()
        finally:
            con.close()

    def _fetch_one(self, sql, params=None):
        con = self._conn()
        try:
            with con.cursor() as cur:
                cur.execute(sql, params or ())
                return cur.fetchone()
        finally:
            con.close()

    def _execute(self, sql, params=None):
        con = self._conn()
        try:
            with con.cursor() as cur:
                cur.execute(sql, params or ())
                con.commit()
                return cur.lastrowid
        finally:
            con.close()

    # ── Авторизация ───────────────────────────────────────────

    def authenticate(self, email, password):
        return self._fetch_one(
            "SELECT u.user_id, u.full_name, u.email, r.role_name "
            "FROM users u "
            "JOIN roles r ON u.role_id = r.role_id "
            "WHERE u.email = %s AND u.password = %s",
            (email, password),
        )

    # ── Справочники ───────────────────────────────────────────

    def get_categories(self):
        return self._fetch_all(
            "SELECT category_id, category_name "
            "FROM productcategories ORDER BY category_name"
        )

    def get_manufacturers(self):
        return self._fetch_all(
            "SELECT manufacturer_id, manufacturer_name "
            "FROM manufacturers ORDER BY manufacturer_name"
        )

    def get_suppliers(self):
        return self._fetch_all(
            "SELECT supplier_id, supplier_name "
            "FROM suppliers ORDER BY supplier_name"
        )

    def get_pickup_points(self):
        return self._fetch_all(
            "SELECT point_id, address "
            "FROM pickuppoints ORDER BY address"
        )

    def get_clients(self):
        return self._fetch_all(
            "SELECT user_id, full_name FROM users ORDER BY full_name"
        )

    def get_product_articles(self):
        return self._fetch_all(
            "SELECT article_number FROM products "
            "ORDER BY article_number"
        )

    # ── Товары ────────────────────────────────────────────────

    def get_products(self, supplier_id=None, search=None,
                     sort_stock=None):
        """
        supplier_id  — фильтр по поставщику (None = все)
        search       — поиск по ВСЕМ текстовым полям одновременно
        sort_stock   — 'asc' | 'desc' | None (сортировка по кол-ву)
        """
        sql = (
            "SELECT p.product_id, p.article_number, p.product_name, "
            "       pc.category_name, p.description, "
            "       m.manufacturer_name, s.supplier_name, "
            "       p.price, p.unit_of_measure, "
            "       p.stock_quantity, p.current_discount, p.photo_filename "
            "FROM products p "
            "LEFT JOIN productcategories pc ON p.category_id = pc.category_id "
            "LEFT JOIN manufacturers m "
            "  ON p.manufacturer_id = m.manufacturer_id "
            "LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id"
        )
        where, params = [], []
        if supplier_id:
            where.append("p.supplier_id = %s")
            params.append(supplier_id)
        if search:
            where.append(
                "(p.product_name LIKE %s OR p.article_number LIKE %s "
                "OR p.description LIKE %s OR m.manufacturer_name LIKE %s "
                "OR s.supplier_name LIKE %s OR pc.category_name LIKE %s)"
            )
            t = f"%{search}%"
            params.extend([t, t, t, t, t, t])
        if where:
            sql += " WHERE " + " AND ".join(where)
        if sort_stock == 'asc':
            sql += " ORDER BY p.stock_quantity ASC"
        elif sort_stock == 'desc':
            sql += " ORDER BY p.stock_quantity DESC"
        else:
            sql += " ORDER BY p.product_id"
        return self._fetch_all(sql, params)

    def get_product_by_id(self, product_id):
        return self._fetch_one(
            "SELECT * FROM products WHERE product_id = %s",
            (product_id,),
        )

    def add_product(self, d):
        return self._execute(
            "INSERT INTO products "
            "(article_number, product_name, unit_of_measure, price, "
            " supplier_id, manufacturer_id, category_id, "
            " current_discount, stock_quantity, description, photo_filename) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (d['article_number'], d['product_name'], d['unit_of_measure'],
             d['price'], d['supplier_id'], d['manufacturer_id'],
             d['category_id'], d['current_discount'], d['stock_quantity'],
             d['description'], d['photo_filename']),
        )

    def update_product(self, product_id, d):
        self._execute(
            "UPDATE products SET "
            "  article_number=%s, product_name=%s, unit_of_measure=%s, "
            "  price=%s, supplier_id=%s, manufacturer_id=%s, category_id=%s, "
            "  current_discount=%s, stock_quantity=%s, description=%s, "
            "  photo_filename=%s "
            "WHERE product_id = %s",
            (d['article_number'], d['product_name'], d['unit_of_measure'],
             d['price'], d['supplier_id'], d['manufacturer_id'],
             d['category_id'], d['current_discount'], d['stock_quantity'],
             d['description'], d['photo_filename'], product_id),
        )

    def can_delete_product(self, product_id):
        """False, если товар фигурирует хотя бы в одном заказе."""
        row = self._fetch_one(
            "SELECT COUNT(*) AS cnt FROM orderitems "
            "WHERE product_id = %s",
            (product_id,),
        )
        return row['cnt'] == 0 if row else True

    def delete_product(self, product_id):
        self._execute(
            "DELETE FROM products WHERE product_id = %s", (product_id,)
        )

    # ── Заказы ────────────────────────────────────────────────

    def get_orders(self):
        return self._fetch_all(
            "SELECT o.order_id, o.pickup_code, o.status, "
            "       pp.address AS pickup_address, "
            "       o.order_date, o.delivery_date "
            "FROM orders o "
            "LEFT JOIN pickuppoints pp "
            "  ON o.pickup_point_id = pp.point_id "
            "ORDER BY o.order_id DESC"
        )

    def get_order_by_id(self, order_id):
        return self._fetch_one(
            "SELECT * FROM orders WHERE order_id = %s", (order_id,)
        )

    def add_order(self, d):
        return self._execute(
            "INSERT INTO orders "
            "(order_date, delivery_date, pickup_point_id, "
            " client_id, pickup_code, status) "
            "VALUES (%s,%s,%s,%s,%s,%s)",
            (d['order_date'], d['delivery_date'], d['pickup_point_id'],
             d['client_id'], d['pickup_code'], d['status']),
        )

    def update_order(self, order_id, d):
        self._execute(
            "UPDATE orders SET "
            "  pickup_code=%s, status=%s, pickup_point_id=%s, "
            "  order_date=%s, delivery_date=%s, client_id=%s "
            "WHERE order_id = %s",
            (d['pickup_code'], d['status'], d['pickup_point_id'],
             d['order_date'], d['delivery_date'], d['client_id'],
             order_id),
        )

    def delete_order(self, order_id):
        self._execute(
            "DELETE FROM orders WHERE order_id = %s", (order_id,)
        )
