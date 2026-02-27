import sys
import os
import uuid

from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QDialog,
    QTableWidgetItem, QFileDialog, QMessageBox,
    QListWidgetItem, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QFrame,
)
from PyQt6.QtCore import Qt, QDate, QSize
from PyQt6.QtGui import QPixmap, QPainter, QFont, QColor, QIcon

from database import Database

STYLE = """
* {
    font-family: "Times New Roman";
    font-size: 13px;
}
QMainWindow, QDialog {
    background-color: #FFFFFF;
}
QPushButton {
    padding: 8px 16px;
    border-radius: 4px;
    border: 1px solid #bbb;
    background-color: #F0F0F0;
}
QPushButton:hover {
    background-color: #E0E0E0;
}
QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QTextEdit {
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 3px;
    background: white;
}
#filter_widget {
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 4px;
    background: #fafafa;
}
#header_widget {
    border-bottom: 1px solid #ddd;
}
QListWidget {
    background-color: #FFFFFF;
    border: 1px solid #ccc;
}
QListWidget::item {
    background: transparent;
    border: none;
    padding: 0px;
}
QTableWidget {
    background-color: white;
    alternate-background-color: #f5f5f5;
    gridline-color: #ddd;
    border: 1px solid #ccc;
}
QHeaderView::section {
    background-color: #F0F0F0;
    color: black;
    padding: 6px;
    border: 1px solid #ddd;
}
"""


# ── Утилиты ───────────────────────────────────────────────────

def _path(*parts):
    """Абсолютный путь относительно каталога скрипта."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), *parts)


def _photo(filename):
    """Путь к фото товара; заглушка если файл не найден."""
    if filename and os.path.exists(_path('images', filename)):
        return _path('images', filename)
    return _path('picture.png')


def _set_combo(cb, val):
    """Выставляет элемент QComboBox по data-значению."""
    for i in range(cb.count()):
        if cb.itemData(i) == val:
            cb.setCurrentIndex(i)
            return


# ── Карточка товара ────────────────────────────────────────────

class ProductCard(QFrame):
    """Виджет-карточка для отображения товара в QListWidget."""

    def __init__(self, product, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setMinimumHeight(140)

        discount = int(product.get('current_discount') or 0)
        stock = int(product.get('stock_quantity') or 0)
        price = float(product.get('price') or 0)

        # Фон: скидка > 15% → зелёный; нет на складе → голубой
        if discount > 15:
            bg, fg = '#2E8B57', 'white'
        elif stock == 0:
            bg, fg = '#ADD8E6', 'black'
        else:
            bg, fg = '#FFFFFF', 'black'

        self.setObjectName('pcard')
        self.setStyleSheet(
            f'#pcard {{ background-color: {bg}; '
            f'border: 1px solid #bbb; border-radius: 4px; }}')

        main_lay = QHBoxLayout(self)
        main_lay.setContentsMargins(8, 8, 8, 8)

        # ─ Фото (слева) ─
        photo = QLabel()
        photo.setFixedSize(100, 100)
        photo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        photo.setStyleSheet('border:1px solid #999; background:#f0f0f0;')
        pm = QPixmap(_photo(product.get('photo_filename')))
        if not pm.isNull():
            photo.setPixmap(pm.scaled(
                100, 100,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation))
        main_lay.addWidget(photo)

        # ─ Информация (центр) ─
        info = QVBoxLayout()
        info.setSpacing(2)

        def lbl(text, bold=False):
            w = QLabel(text)
            s = f'color:{fg};'
            if bold:
                s += 'font-weight:bold;font-size:14px;'
            w.setStyleSheet(s)
            w.setWordWrap(True)
            return w

        cat = product.get('category_name') or ''
        name = product.get('product_name') or ''
        info.addWidget(lbl(f'{cat} | {name}', bold=True))

        desc = product.get('description') or ''
        if len(desc) > 120:
            desc = desc[:120] + '…'
        info.addWidget(lbl(f'Описание: {desc}'))
        info.addWidget(
            lbl(f'Производитель: '
                f'{product.get("manufacturer_name", "")}'))
        info.addWidget(
            lbl(f'Поставщик: '
                f'{product.get("supplier_name", "")}'))

        # Цена: при скидке основная зачёркнута красным
        if discount > 0:
            final = price * (1 - discount / 100)
            price_w = QLabel(
                f'Цена: '
                f'<span style="text-decoration:line-through;color:red;">'
                f'{price:.2f} ₽</span> '
                f'<span style="color:{fg};font-weight:bold;">'
                f'{final:.2f} ₽</span>')
        else:
            price_w = QLabel(f'Цена: {price:.2f} ₽')
        price_w.setStyleSheet(f'color:{fg};')
        info.addWidget(price_w)

        info.addWidget(lbl(
            f'Ед. измерения: '
            f'{product.get("unit_of_measure", "шт.")}'))
        info.addWidget(lbl(f'Количество на складе: {stock}'))

        main_lay.addLayout(info, 1)

        # ─ Блок скидки (справа) ─
        disc_frame = QFrame()
        disc_frame.setFixedWidth(100)
        disc_frame.setStyleSheet(
            'border:1px solid #999;border-radius:4px;'
            'background:rgba(255,255,255,0.15);')
        disc_lay = QVBoxLayout(disc_frame)
        disc_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)

        dl = QLabel('Действующая\nскидка')
        dl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dl.setStyleSheet(f'color:{fg};font-size:10px;border:none;')
        disc_lay.addWidget(dl)

        dv = QLabel(f'{discount}%')
        dv.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dv.setStyleSheet(
            f'color:{fg};font-size:18px;font-weight:bold;border:none;')
        disc_lay.addWidget(dv)

        main_lay.addWidget(disc_frame)


# ── Авторизация ───────────────────────────────────────────────

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(_path('login.ui'), self)
        self.db = Database()
        self.user_data = None

        logo = _path('logo.png')
        if os.path.exists(logo):
            pm = QPixmap(logo)
            self.logo_label.setPixmap(pm.scaled(
                200, 60,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation))
        else:
            self.logo_label.hide()

        self.login_btn.clicked.connect(self._login)
        self.guest_btn.clicked.connect(self._guest)
        self.password_input.returnPressed.connect(self._login)
        self.email_input.returnPressed.connect(
            lambda: self.password_input.setFocus())

    def _login(self):
        email = self.email_input.text().strip()
        pw = self.password_input.text().strip()
        if not email or not pw:
            QMessageBox.warning(
                self, 'Предупреждение',
                'Заполните оба поля для входа.')
            return
        try:
            user = self.db.authenticate(email, pw)
            if user:
                self.user_data = user
                self.accept()
            else:
                QMessageBox.critical(
                    self, 'Ошибка авторизации',
                    'Неверный email или пароль.\n'
                    'Проверьте правильность ввода.')
        except Exception as e:
            QMessageBox.critical(
                self, 'Ошибка подключения',
                f'Нет подключения к базе данных:\n{e}')

    def _guest(self):
        self.user_data = {
            'user_id': 0,
            'full_name': 'Гость',
            'email': '',
            'role_name': 'Гость',
        }
        self.accept()


# ── Редактирование товара ─────────────────────────────────────

class ProductEditDialog(QDialog):
    def __init__(self, db, product=None, parent=None):
        super().__init__(parent)
        uic.loadUi(_path('product_edit.ui'), self)
        self.db = db
        self.product = product
        self.orig_photo = product['photo_filename'] if product else None
        self.cur_photo = self.orig_photo

        if product:
            self.setWindowTitle(
                f'Редактирование товара #{product["product_id"]}')
            self.id_value.setText(str(product['product_id']))
        else:
            self.setWindowTitle('Добавление нового товара')
            self.id_text_label.hide()
            self.id_value.hide()

        for c in self.db.get_categories():
            self.category_cb.addItem(c['category_name'], c['category_id'])
        for m in self.db.get_manufacturers():
            self.manufacturer_cb.addItem(
                m['manufacturer_name'], m['manufacturer_id'])
        for s in self.db.get_suppliers():
            self.supplier_cb.addItem(s['supplier_name'], s['supplier_id'])

        self._show_photo(self.cur_photo)
        if product:
            self._load()

        self.upload_btn.clicked.connect(self._upload)
        self.save_btn.clicked.connect(self._save)
        self.cancel_btn.clicked.connect(self.reject)

    def _show_photo(self, filename):
        pm = QPixmap(_photo(filename))
        self.photo_label.setPixmap(pm.scaled(
            300, 200,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation))

    def _upload(self):
        path, _ = QFileDialog.getOpenFileName(
            self, 'Выберите изображение', '',
            'Изображения (*.png *.jpg *.jpeg *.bmp *.gif)')
        if not path:
            return
        pm = QPixmap(path)
        if pm.isNull():
            QMessageBox.critical(
                self, 'Ошибка',
                'Выбранный файл не является изображением.')
            return
        ext = os.path.splitext(path)[1].lower()
        fname = f'product_{uuid.uuid4().hex[:10]}{ext}'
        scaled = pm.scaled(
            300, 200,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation)
        if not scaled.save(_path('images', fname)):
            QMessageBox.critical(
                self, 'Ошибка', 'Не удалось сохранить изображение.')
            return
        self.cur_photo = fname
        self.photo_label.setPixmap(scaled)

    def _load(self):
        p = self.product
        self.article_input.setText(p.get('article_number') or '')
        self.name_input.setText(p.get('product_name') or '')
        _set_combo(self.category_cb, p.get('category_id'))
        self.description_input.setPlainText(p.get('description') or '')
        _set_combo(self.manufacturer_cb, p.get('manufacturer_id'))
        _set_combo(self.supplier_cb, p.get('supplier_id'))
        self.price_input.setValue(
            float(p['price']) if p.get('price') is not None else 1)
        self.unit_input.setText(p.get('unit_of_measure') or 'шт.')
        self.stock_input.setValue(int(p['stock_quantity'] or 0))
        self.discount_input.setValue(int(p['current_discount'] or 0))

    def _save(self):
        art = self.article_input.text().strip()
        name = self.name_input.text().strip()
        if not art:
            QMessageBox.warning(
                self, 'Ошибка ввода',
                'Поле «Артикул» обязательно для заполнения.')
            self.article_input.setFocus()
            return
        if not name:
            QMessageBox.warning(
                self, 'Ошибка ввода',
                'Поле «Наименование» обязательно для заполнения.')
            self.name_input.setFocus()
            return
        data = {
            'article_number': art,
            'product_name': name,
            'category_id': self.category_cb.currentData(),
            'description': self.description_input.toPlainText().strip(),
            'manufacturer_id': self.manufacturer_cb.currentData(),
            'supplier_id': self.supplier_cb.currentData(),
            'price': self.price_input.value(),
            'unit_of_measure': self.unit_input.text().strip() or 'шт.',
            'stock_quantity': self.stock_input.value(),
            'current_discount': self.discount_input.value(),
            'photo_filename': self.cur_photo,
        }
        try:
            if self.product:
                self.db.update_product(
                    self.product['product_id'], data)
                if (self.orig_photo
                        and self.orig_photo != self.cur_photo):
                    old = _path('images', self.orig_photo)
                    if os.path.exists(old):
                        try:
                            os.remove(old)
                        except OSError:
                            pass
                QMessageBox.information(
                    self, 'Успех', 'Товар успешно обновлён.')
            else:
                self.db.add_product(data)
                QMessageBox.information(
                    self, 'Успех', 'Товар успешно добавлен.')
            self.accept()
        except Exception as e:
            QMessageBox.critical(
                self, 'Ошибка БД',
                f'Не удалось сохранить товар:\n{e}')


# ── Редактирование заказа ─────────────────────────────────────

class OrderEditDialog(QDialog):
    def __init__(self, db, order=None, parent=None):
        super().__init__(parent)
        uic.loadUi(_path('order_edit.ui'), self)
        self.db = db
        self.order = order

        if order:
            self.setWindowTitle(
                f'Редактирование заказа #{order["order_id"]}')
        else:
            self.setWindowTitle('Добавление нового заказа')

        for art in self.db.get_product_articles():
            self.code_cb.addItem(art['article_number'])
        for pp in self.db.get_pickup_points():
            self.point_cb.addItem(pp['address'], pp['point_id'])
        for cl in self.db.get_clients():
            self.client_cb.addItem(cl['full_name'], cl['user_id'])

        self.order_date.setDate(QDate.currentDate())
        self.delivery_date.setDate(QDate.currentDate().addDays(14))

        if order:
            self._load()

        self.save_btn.clicked.connect(self._save)
        self.cancel_btn.clicked.connect(self.reject)

    def _load(self):
        o = self.order
        idx = self.code_cb.findText(o.get('pickup_code', ''))
        if idx >= 0:
            self.code_cb.setCurrentIndex(idx)
        idx = self.status_cb.findText(o.get('status', ''))
        if idx >= 0:
            self.status_cb.setCurrentIndex(idx)
        _set_combo(self.point_cb, o.get('pickup_point_id'))
        _set_combo(self.client_cb, o.get('client_id'))
        if o.get('order_date'):
            d = o['order_date']
            self.order_date.setDate(QDate(d.year, d.month, d.day))
        if o.get('delivery_date'):
            d = o['delivery_date']
            self.delivery_date.setDate(QDate(d.year, d.month, d.day))

    def _save(self):
        code = self.code_cb.currentText().strip()
        if not code:
            QMessageBox.warning(
                self, 'Ошибка ввода',
                'Выберите артикул товара из списка.')
            self.code_cb.setFocus()
            return
        od = self.order_date.date()
        dd = self.delivery_date.date()
        data = {
            'pickup_code': code,
            'status': self.status_cb.currentText(),
            'pickup_point_id': self.point_cb.currentData(),
            'client_id': self.client_cb.currentData(),
            'order_date':
                f'{od.year()}-{od.month():02d}-{od.day():02d} 00:00:00',
            'delivery_date':
                f'{dd.year()}-{dd.month():02d}-{dd.day():02d} 00:00:00',
        }
        try:
            if self.order:
                self.db.update_order(self.order['order_id'], data)
                QMessageBox.information(
                    self, 'Успех', 'Заказ успешно обновлён.')
            else:
                self.db.add_order(data)
                QMessageBox.information(
                    self, 'Успех', 'Заказ успешно добавлен.')
            self.accept()
        except Exception as e:
            QMessageBox.critical(
                self, 'Ошибка БД',
                f'Не удалось сохранить заказ:\n{e}')


# ── Главное окно ──────────────────────────────────────────────

class MainWindow(QMainWindow):
    _O_H = ['ID', 'Артикул', 'Статус', 'Адрес выдачи',
            'Дата заказа', 'Дата выдачи']
    _O_K = ['order_id', 'pickup_code', 'status', 'pickup_address',
            'order_date', 'delivery_date']

    def __init__(self, user):
        super().__init__()
        uic.loadUi(_path('main.ui'), self)
        self.db = Database()
        self.user = user
        self.edit_open = False
        self.restart = False

        role = user['role_name']
        self.is_admin = role == 'Администратор'
        self.is_manager = role == 'Менеджер'
        self.can_search = self.is_admin or self.is_manager
        self.can_crud = self.is_admin
        self.can_orders = self.is_admin or self.is_manager

        self.setWindowTitle(f'Магазин обуви — {role}')
        self.fio_label.setText(user['full_name'])
        self.page_title.setText('Список товаров')

        # Логотип
        logo = _path('logo.png')
        if os.path.exists(logo):
            pm = QPixmap(logo)
            self.logo_label.setPixmap(pm.scaled(
                50, 50,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation))
        else:
            self.logo_label.hide()

        # Видимость элементов по ролям
        self.filter_widget.setVisible(self.can_search)
        self.add_product_btn.setVisible(self.can_crud)
        self.delete_product_btn.setVisible(self.can_crud)
        self.orders_btn.setVisible(self.can_orders)
        self.add_order_btn.setVisible(self.can_crud)
        self.delete_order_btn.setVisible(self.can_crud)

        # Фильтр по поставщику
        if self.can_search:
            self.supplier_filter.blockSignals(True)
            self.supplier_filter.addItem('Все поставщики', None)
            for s in self.db.get_suppliers():
                self.supplier_filter.addItem(
                    s['supplier_name'], s['supplier_id'])
            self.supplier_filter.blockSignals(False)

            self.supplier_filter.currentIndexChanged.connect(
                self.load_products)
            self.sort_combo.currentIndexChanged.connect(
                self.load_products)
            self.search_input.textChanged.connect(
                self.load_products)

        self.products_list.setSpacing(4)

        # Навигация
        self.orders_btn.clicked.connect(self._show_orders)
        self.back_btn.clicked.connect(self._show_products)
        self.logout_btn.clicked.connect(self._logout)

        if self.can_crud:
            self.add_product_btn.clicked.connect(self._add_product)
            self.delete_product_btn.clicked.connect(self._del_product)
            self.add_order_btn.clicked.connect(self._add_order)
            self.delete_order_btn.clicked.connect(self._del_order)

        # Двойной клик → редактирование (только админ)
        if self.is_admin:
            self.products_list.itemDoubleClicked.connect(
                self._edit_product)
            self.orders_table.cellDoubleClicked.connect(
                self._edit_order)

        self.load_products()

    # ── навигация ──

    def _show_orders(self):
        self.page_title.setText('Список заказов')
        self.load_orders()
        self.stacked_widget.setCurrentIndex(1)

    def _show_products(self):
        self.page_title.setText('Список товаров')
        self.load_products()
        self.stacked_widget.setCurrentIndex(0)

    def _logout(self):
        self.restart = True
        self.close()

    # ── загрузка товаров (карточки) ──

    def load_products(self):
        try:
            supplier = (self.supplier_filter.currentData()
                        if self.can_search else None)
            search = (self.search_input.text().strip()
                      if self.can_search else None)
            sort_idx = (self.sort_combo.currentIndex()
                        if self.can_search else 0)
            sort_stock = {0: None, 1: 'asc', 2: 'desc'}.get(sort_idx)

            rows = self.db.get_products(
                supplier, search or None, sort_stock)

            self.products_list.clear()
            for row in rows:
                card = ProductCard(row)
                item = QListWidgetItem(self.products_list)
                h = max(card.sizeHint().height(), 160)
                item.setSizeHint(QSize(
                    self.products_list.viewport().width(), h))
                item.setData(
                    Qt.ItemDataRole.UserRole, row['product_id'])
                self.products_list.setItemWidget(item, card)
            self.products_list.viewport().update()

            self.products_count.setText(
                f'Найдено товаров: {len(rows)}')
        except Exception as e:
            QMessageBox.critical(
                self, 'Ошибка', f'Загрузка товаров:\n{e}')

    # ── загрузка заказов (таблица) ──

    def load_orders(self):
        try:
            rows = self.db.get_orders()
            t = self.orders_table
            t.setRowCount(len(rows))
            t.setColumnCount(len(self._O_H))
            t.setHorizontalHeaderLabels(self._O_H)
            for r, row in enumerate(rows):
                for c, k in enumerate(self._O_K):
                    v = row.get(k)
                    if v is not None and hasattr(v, 'strftime'):
                        s = v.strftime('%d.%m.%Y')
                    else:
                        s = str(v) if v is not None else ''
                    t.setItem(r, c, QTableWidgetItem(s))
            t.resizeColumnsToContents()
            t.setColumnWidth(0, 50)
            self.orders_count.setText(f'Всего заказов: {len(rows)}')
        except Exception as e:
            QMessageBox.critical(
                self, 'Ошибка', f'Загрузка заказов:\n{e}')

    # ── CRUD товаров ──

    def _add_product(self):
        if self.edit_open:
            QMessageBox.warning(
                self, 'Внимание',
                'Сначала закройте открытое окно редактирования.')
            return
        self.edit_open = True
        try:
            dlg = ProductEditDialog(self.db, parent=self)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                self.load_products()
        finally:
            self.edit_open = False

    def _edit_product(self, item):
        if self.edit_open:
            return
        pid = item.data(Qt.ItemDataRole.UserRole)
        prod = self.db.get_product_by_id(pid)
        if not prod:
            return
        self.edit_open = True
        try:
            dlg = ProductEditDialog(self.db, prod, self)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                self.load_products()
        finally:
            self.edit_open = False

    def _del_product(self):
        item = self.products_list.currentItem()
        if not item:
            QMessageBox.warning(
                self, 'Внимание',
                'Выберите товар из списка для удаления.')
            return
        pid = item.data(Qt.ItemDataRole.UserRole)
        prod = self.db.get_product_by_id(pid)
        if not prod:
            return
        name = prod.get('product_name', '')
        if QMessageBox.question(
            self, 'Подтверждение удаления',
            f'Удалить товар «{name}»?\n'
            f'Это действие необратимо.',
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        ) != QMessageBox.StandardButton.Yes:
            return
        try:
            if not self.db.can_delete_product(pid):
                QMessageBox.critical(
                    self, 'Удаление невозможно',
                    f'Товар «{name}» нельзя удалить,\n'
                    f'так как он присутствует в заказах.')
                return
            self.db.delete_product(pid)
            if prod.get('photo_filename'):
                p = _path('images', prod['photo_filename'])
                if os.path.exists(p):
                    try:
                        os.remove(p)
                    except OSError:
                        pass
            self.load_products()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))

    # ── CRUD заказов ──

    def _add_order(self):
        if self.edit_open:
            QMessageBox.warning(
                self, 'Внимание',
                'Сначала закройте открытое окно редактирования.')
            return
        self.edit_open = True
        try:
            dlg = OrderEditDialog(self.db, parent=self)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                self.load_orders()
        finally:
            self.edit_open = False

    def _edit_order(self, row, _col=0):
        if self.edit_open:
            return
        oid = int(self.orders_table.item(row, 0).text())
        order = self.db.get_order_by_id(oid)
        if not order:
            return
        self.edit_open = True
        try:
            dlg = OrderEditDialog(self.db, order, self)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                self.load_orders()
        finally:
            self.edit_open = False

    def _del_order(self):
        row = self.orders_table.currentRow()
        if row < 0:
            QMessageBox.warning(
                self, 'Внимание',
                'Выберите заказ из таблицы для удаления.')
            return
        oid = int(self.orders_table.item(row, 0).text())
        code = self.orders_table.item(row, 1).text()
        if QMessageBox.question(
            self, 'Подтверждение удаления',
            f'Удалить заказ «{code}»?\n'
            f'Позиции заказа тоже будут удалены.',
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        ) != QMessageBox.StandardButton.Yes:
            return
        try:
            self.db.delete_order(oid)
            self.load_orders()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))


# ── Запуск ────────────────────────────────────────────────────

def _ensure_setup():
    """Создаёт папку images и заглушку picture.png при необходимости."""
    os.makedirs(_path('images'), exist_ok=True)
    if not os.path.exists(_path('picture.png')):
        pm = QPixmap(300, 200)
        pm.fill(QColor('#E0E0E0'))
        p = QPainter(pm)
        p.setPen(QColor('#999'))
        p.setFont(QFont('Times New Roman', 14))
        p.drawText(pm.rect(), Qt.AlignmentFlag.AlignCenter,
                   'Нет изображения')
        p.end()
        pm.save(_path('picture.png'))


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)

    _ensure_setup()

    # Иконка приложения
    for ico in ('icon.ico', 'icon.png'):
        p = _path(ico)
        if os.path.exists(p):
            app.setWindowIcon(QIcon(p))
            break

    # Цикл авторизации: при логауте пользователь возвращается сюда
    while True:
        login = LoginDialog()
        if login.exec() != QDialog.DialogCode.Accepted:
            break
        win = MainWindow(login.user_data)
        win.show()
        app.exec()
        do_restart = win.restart
        del win
        if not do_restart:
            break


if __name__ == '__main__':
    main()
