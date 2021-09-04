from werkzeug.datastructures import auth_property
from market import db,login_manager
from market import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id=db.Column(db.Integer(),primary_key=True) #necessary for all db tables
    username=db.Column(db.String(length=30), nullable=False, unique=True)
    email_address=db.Column(db.String(length=50),nullable=False,unique=True)
    password_hash=db.Column(db.String(length=60),nullable=False)
    budget=db.Column(db.Integer(),nullable=False,default=200000)
    items=db.relationship('Item',backref='owned_user', lazy=True)
    #db.relationship is used to convey a relationship between two models. 
    #backref='owned_user' is a back reference to that user model
    #lazy=True is used so that SQlAlchemy grabs all the objects of an Item in one shot. It is important to mention that.

    @property
    def pretty_budget(self):
        if len(str(self.budget))>=4:
            return f'₹{str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        else:
            return f'₹{self.budget}'

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self,plain_text_password):
        self.password_hash=bcrypt.generate_password_hash(plain_text_password).decode('utf-8')


    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)
        
    def can_purchase(self,item_obj):
        return self.budget >= item_obj.price
        
    def can_sell(self,item_obj):
        return item_obj in self.items


class Item(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(length=30),nullable=False,unique=True)
    price=db.Column(db.Integer(),nullable=False)
    barcode=db.Column(db.String(length=12),nullable=False,unique=True)
    description=db.Column(db.String(length=1024),nullable=False,unique=True)
    owner=db.Column(db.Integer(),db.ForeignKey('user.id'))
    #foreignkey is used to get a relationship with the primary_key of the other model


    def __repr__(self):
        return f'Item {self.name}'

    def assign_ownership(self,user):
        self.owner=user.id
        user.budget-=self.price
        db.session.commit()

    def sell(self,user):
        self.owner=None
        user.budget+=self.price
        db.session.commit()