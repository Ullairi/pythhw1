from sqlalchemy import create_engine, Column, String, Integer, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

#Creating connection to sqlite database in memory
engine = create_engine('sqlite:///:memory:', echo=True)

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