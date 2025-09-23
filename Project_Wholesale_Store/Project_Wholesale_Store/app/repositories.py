from .models import Product, db

class ProductRepository:
    def get_all(self):
        return Product.query.all()

    def get_by_id(self, product_id):
        return Product.query.get(product_id)

    def add(self, product):
        db.session.add(product)
        db.session.commit()

    def delete(self, product):
        db.session.delete(product)
        db.session.commit()

    def update(self):
        db.session.commit()