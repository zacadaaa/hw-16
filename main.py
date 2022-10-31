import row_data
import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
app.config["SQLAlCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    age = db.Column(db.Integer)
    email = db.Column(db.String(255))
    role = db.Column(db.String(255))
    phone = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    start_date = db.Column(db.String(255))
    end_date = db.Column(db.String(255))
    address = db.Column(db.String(255))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }


def init_database():
    app.app_context().push()
    db.drop_all()
    db.create_all()

    for user_data in row_data.users:
        db.session.add(User(
            id=user_data.get('id'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            age=user_data.get('age'),
            email=user_data.get('email'),
            role=user_data.get('role'),
            phone=user_data.get('phone')
        ))
        db.session.commit()

    for order_data in row_data.orders:
        db.session.add(Order(
            id=order_data.get('id'),
            name=order_data.get('name'),
            description=order_data.get('description'),
            start_date=order_data.get('start_date'),
            end_date=order_data.get('end_date'),
            address=order_data.get('address'),
            price=order_data.get('price'),
            customer_id=order_data.get('customer_id'),
            executor_id=order_data.get('executor_id')
        ))
        db.session.commit()

        for offer_data in row_data.offers:
            db.session.add(Offer(
                id=offer_data.get('id'),
                order_id=offer_data.get('order_id'),
                executor_id=offer_data.get('executor_id')
            ))

        db.session.commit()


@app.route('/users')
def get_users():
    result = []
    for user in User.query.all():
        result.append(user.to_dict())
    return json.dumps(result), 200, {'Content-Type': 'application/json; charset: utf-8'}

if __name__ == '__main__':
    init_database()
    app.run(debug=True)
