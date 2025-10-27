from sqlalchemy import create_engine, Column, String, Integer, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import func

#Creating connection to sqlite database in memory
engine = create_engine('sqlite:///:memory:', echo=False)

#Creating session
Session = sessionmaker(bind=engine)
session = Session()

#Creating base class for declarative models
Base = declarative_base()

#Defining Category model
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)

    products = relationship("Product", back_populates="category")

#Defining Product model
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    in_stock = Column(Boolean, default=True)

#  Linking Foreign key to Category
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="products")


# Creating all tables in database
Base.metadata.create_all(engine)

# Add categories
electronics = Category(name='Электроника', description='Гаджеты и устройства.')
books =  Category(name='Книги',description='Печатные книги и электронные книги')
cloth = Category(name='Одежда', description='Одежда для мужчин и женщин')

session.add_all([electronics, books, cloth])
session.commit()

products = [
    Product(name='Смартфон', price=299.99, in_stock=True, category=electronics),
    Product(name='Ноутбук', price=499.99, in_stock=True, category=electronics),
    Product(name='Научно-фантастический роман', price=15.99, in_stock=True, category=books),
    Product(name='Джинсы', price=40.50, in_stock=True, category=cloth),
    Product(name='Футболка', price=20.00, in_stock=True, category=cloth)
]

session.add_all(products)
session.commit()

#2 categories and products display
categories = session.query(Category).all()
for ctg in categories:
    print(f"Категория: {ctg.name}")
    for prt in ctg.products:
        print(f" Продукт: {prt.name}, Цена: {prt.price}")


#3 Update product price
smartphone = session.query(Product).filter_by(name='Смартфон').first()
if smartphone:
    smartphone.price = 349.99
    session.commit()
    smartphone_newprice = session.query(Product).filter_by(name='Смартфон').first()
    print(f"Новая цена смартфона: {smartphone_newprice.price}")

#4 Product count per category
counts = session.query(Category.name, func.count(Product.id))\
          .join(Product).group_by(Category.id).all()

for name, count in counts:
    print(f"Категория: {name}; Количество продуктов: {count}")


#5 Filter categories with more than one product
filtr = session.query(Category.name, func.count(Product.id)).join(Product)\
         .group_by(Category.id).having(func.count(Product.id) > 1).all()

for name, count in filtr:
    print(f"Категории где больше 1 продукта: {name}; Количество продуктов: {count}")