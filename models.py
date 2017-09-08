from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer,Numeric,String,Sequence,ForeignKey,Enum,BLOB,Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.schema import CheckConstraint
import enum
from sqlalchemy.orm import sessionmaker


Base=declarative_base()

#Track association between loans and reports
ReportsLoansAssociation = Table('ReportsLoansAssociation',
    Base.metadata,
    Column('loan_id',Integer(), ForeignKey('loans.id') ),
    Column('report_id',Integer(), ForeignKey('reports.id') )
    )

#Enumerate currencies
class Currency(enum.Enum):
    USD=1
    GBP=2
    JPY=3

#A helper class to convert currencies to GBP
class Conversion(Base):
    __tablename__='conversion'
    id = Column(Integer,primary_key=True)
    currency=Column( Enum(Currency),nullable=False,unique=True )
    value=Column(Numeric) #In GBP
    @staticmethod
    def convert(session,currency,amount): #Converts to GBP
        entry=session.query(Conversion).filter(Conversion.currency==currency).first()
        return amount*entry.value

class User(Base):
    __tablename__='users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column( String(255),CheckConstraint('length(name)>=1'),nullable=False )
#    def __repr__(self):
#        return "Name: %s"%(self.name)

class Loan(Base):
    __tablename__='loans'
    id = Column(Integer, primary_key=True)
    balance = Column(Numeric, CheckConstraint('balance>=0') )
    currency=Column( Enum(Currency),nullable=False )
    reports=relationship('Report', secondary=ReportsLoansAssociation,backref='Loan')
#    def __repr__(self):
#        return "%s"%(self.balance)
    
class Report(Base):
    __tablename__='reports'
    id = Column(Integer, primary_key=True)
    title = Column( String(255),CheckConstraint('length(title)>=1'),nullable=False ) 
    body = Column(BLOB,CheckConstraint('length(body)<=5*1024*1024') )
    author = Column( Integer,ForeignKey(User.id),nullable=False )
    loans = relationship('Loan',secondary=ReportsLoansAssociation,backref='Report')
#    def __repr__(self):
#        return "%s"%(self.title)
