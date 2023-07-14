# Put into a Python file in your project.
# Activate your virtual environment.
# Run with python file_name.py.
from sqlalchemy import create_engine, Column, ForeignKey, Table, Integer, String
from sqlalchemy.orm import relationship, sessionmaker, declarative_base, joinedload

Base = declarative_base()

pony_handlers = Table(
    "pony_handlers",
    Base.metadata,
    Column("pony_id", ForeignKey("ponies.id"), primary_key=True),
    Column("handler_id", ForeignKey("handlers.id"), primary_key=True))


class Owner(Base):
    __tablename__ = 'owners'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))

    ponies = relationship("Pony", back_populates="owner",
                          cascade="all, delete-orphan")


class Pony(Base):
    __tablename__ = "ponies"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    birth_year = Column(Integer)
    breed = Column(String(255))
    owner_id = Column(Integer, ForeignKey("owners.id"))

    owner = relationship("Owner", back_populates="ponies")
    handlers = relationship("Handler",
                            secondary=pony_handlers,
                            back_populates="ponies")


class Handler(Base):
    __tablename__ = "handlers"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    employee_id = Column(String(12))

    ponies = relationship("Pony",
                          secondary=pony_handlers,
                          back_populates="handlers")


db_url = "postgresql://sqlalchemy_test:password@localhost/sqlalchemy_test"
engine = create_engine(db_url)

SessionFactory = sessionmaker(bind=engine)

session = SessionFactory()

# Article code here.

# # Adding Data
# you = Owner(first_name="your first name",
#             last_name="your last name",
#             email="your email")

# your_pony = Pony(name="your pony's name",
#                  birth_year=2020,
#                  breed="whatever you want",
#                  owner=you)

# print(you.id)         # > None
# print(your_pony.id)   # > None

# # The Session object has already been created and
# # bound to the engine.
# session.add(you)      # Connects you and your_pony objects
# session.commit()      # Saves data to the database

# print(you.id)         # > 4 (or whatever the new id is)
# print(your_pony.id)   # > 4 (or whatever the new id is)

# # Updating Data
# print(your_pony.birth_year)    # > 2020

# your_pony.birth_year = 2019
# print(your_pony.birth_year)    # > 2019

# session.commit()

# print(your_pony.birth_year)    # > 2019

# # Deleting Data
# session.delete(you)
# session.commit()

# # Using Rollback
# your_pony.name = "Mr. Fancy Pants"
# your_pony.birth_year = 1896
# print(your_pony.name)          # > Mr. Fancy Pants
# print(your_pony.birth_year)    # > 1896

# session.rollback()
# print(your_pony.name)          # > your pony's original name
# print(your_pony.birth_year)    # > 2019

# # Basic Query
# pony_query=session.query(Pony)
# # print(pony_query)
# # Query Primary Key
# pony_id_4_query = session.query(Pony).get(4)
# # Query Certain Attributes
# owner_query = session.query(Owner.first_name, Owner.last_name)
# # print(owner_query)
# # Ordering
# owner_query = session.query(Owner.first_name, Owner.last_name).order_by(Owner.last_name)
# # print(owner_query)
# # Filtering
# pony_query = session.query(Pony).filter(Pony.name.like("%u%"))
# pony_query = session.query(Pony).filter(Pony.name.ilike("%u%"))
# pony_query = session.query(Pony).filter(Pony.name.ilike("%u%")).filter(Pony.birth_year < 2015)
# # print(pony_query)

# # Using Queries (all,first,one,one_or_none)
# pony_query=session.query(Pony)
# ponies = pony_query.all()
# for pony in ponies:
#     print(pony.name)

# hirzai_owners = session.query(Owner) \
#                        .join(Pony)  \
#                        .filter(Pony.breed == "Hirzai")
# for owner in hirzai_owners:
#     print(owner.first_name, owner.last_name)

# # Lazy Loading (N+1)
# for owner in session.query(Owner):
#     print(owner.first_name, owner.last_name)
#     for pony in owner.ponies:
#         print("\t", pony.name)

# Eager Loading
owners_and_ponies = session.query(Owner).options(joinedload(Owner.ponies))
for owner in owners_and_ponies:
    print(owner.first_name, owner.last_name)
    for pony in owner.ponies:
        print("\t", pony.name)
hirzai_owners_and_ponies = session.query(Owner) \
                                  .join(Pony)  \
                                  .filter(Pony.breed == "Hirzai") \
                                  .options(joinedload(Owner.ponies))
for owner in hirzai_owners_and_ponies:
    print(owner.first_name, owner.last_name)
    for pony in owner.ponies:
        print("\t", pony.name)

session.close()
engine.dispose()
print('done')