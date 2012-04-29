#!/usr/bin/python

import ConfigParser
import string
from random import choice


from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'
    
    id_customer = Column(BigInteger, Sequence('pk_seq'), primary_key=True)
    firstname = Column(Text, nullable=False)
    lastname = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    password = Column(Text(), nullable=False)
    
    address = relationship("Address")
    orders = relationship("Orders")
        
    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password                            
        
    def __repr__(self):
        return "<Customer('%s','%s','%s','%s')>" % ( self.firstname, 
                                                     self.lastname,
                                                     self.email,
                                                     self.password )

class Address(Base):
    __tablename__ = 'address'
    
    id_address = Column(BigInteger, Sequence('pk_seq'), primary_key=True)
    key_customer = Column(BigInteger, ForeignKey('customer.id_customer'), nullable=False)
    address_line1 = Column(Text, nullable=False)
    address_line2 = Column(Text)
    postcode = Column(Text, nullable=False)
    country = Column(Text, nullable=False)
    region = Column(Text)
    city = Column(Text)
    
    customer = relationship("Customer")
    orders = relationship("Orders")


class Orders(Base):
    __tablename__ = 'orders'
    
    id_order = Column(BigInteger, Constraint('orders_pkey'), 
                      Sequence('pk_seq'), primary_key=True)
    key_customer = Column(BigInteger, ForeignKey('customer.id_customer'), 
                          Constraint('orders_key_customer_fkey'), nullable=False)
    key_status = Column(Integer, nullable=False)
    key_address = Column(BigInteger, ForeignKey('address.id_address'),
                         Constraint('orders_key_customer_fkey2'), nullable=False)
    delivered = Column(Boolean) # server_default='false'

    ForeignKeyConstraint(['key_customer', 'key_address'], ['customer.id_customer', 'address.id_address'])
    
    customer = relationship("Customer")
    address = relationship("Address")


class Actions(object):
    
    def __init__(self, echo=False):
        '''
        Initialize actions
        
        :Args:
            echo - boolean, if True, then turn on sqlalchemy loggin 
                    into console
                (default: False).
        '''            
        try:
            cfg = ConfigParser.SafeConfigParser()
            cfg.read('config')
            self._engine = create_engine('postgresql+psycopg2://%s:%s@%s/%s' % 
                                          ( cfg.get('connection', 'username'),
                                            cfg.get('connection', 'password'),
                                            cfg.get('connection', 'host'),
                                            cfg.get('connection', 'dbname')),
                                          echo=echo)
            self._engine.connect()                            
        except Exception, msg:
            raise Exception("Unable to connect to DB:\n\t%s" % msg.message)            
    
    def __get_random_string(self, length=10):
        ''' 
        Generate random string (letters(upper,lower case) with digits)
        with specified length (default = 10).
        '''   
        return ''.join(choice(string.letters + string.digits) for i in xrange(length))
    
    def __get_random_int(self, length=5):
        '''
        Generate random int with specified number of digits (default = 5).
        '''
        return ''.join(choice(string.digits) for i in xrange(length))
        
    def add_random_customer(self):
        '''
        Add record to the customer table with randomly generated values
        ''' 
        
        def do_sql_script(conn, fname, lname, email, pwd):
            script = text("""SELECT create_customer(:fname,:lname,:email,:pwd);""")
            conn.execute(script, {'fname':fname, 'lname':lname, 
                                  'email':email, 'pwd':pwd} )            
        
        firstname = self.__get_random_string(10)
        lastname = self.__get_random_string(15)
        email = "%s.%s@company.com" % (firstname, lastname)
        password = self.__get_random_string(8)
        
                    
        self._engine.transaction(do_sql_script, firstname, lastname, 
                               email, password)
        
    def get_last_customer_id(self):
        '''
        Return id_customer of the last added record in 'customer' table.
        '''
        
        session = sessionmaker(bind=self._engine)()
        inst = session.query(Customer).order_by(Customer.id_customer.desc()).first()
        i = 0
        if inst != None:
            i = inst.id_customer
        
        return i
    
    def get_last_address_id(self, cust_id=0):
        '''
        Return last added address (record) for the specified customer, 
        
        :Args:
            cust_id - int, id_customer. If value not specified or 0,
            then returned address for the last customer.
        '''
        
        if (cust_id==0):
            cust_id = self.get_last_customer_id(
                                                )
        session = sessionmaker(bind=self._engine)()
        inst = session.query(Address).filter(Address.key_customer == cust_id).\
                order_by(Address.id_address.desc()).first()
        i = 0
        if inst != None:
            i = inst.id_address
        
        return i
        
    def add_random_address(self, cust_id=0):
        '''
        Add record to the address table for the specified customer
        
        :Args:
            cust_id - int, customer id. If value not specified or 0,
                then last customer used.
        '''
        def do_sql_script(conn, cust_id, line1, line2, pcode, cntry, rgn, cty):
            script = text("""SELECT save_address(:cust_id,:line1,
                                                 :line2,:pcode,                                                                                                  
                                                 :country,:region,
                                                 :city);""")
            conn.execute(script, {'cust_id':cust_id, 'line1':line1, 
                                  'line2':line2, 'pcode':pcode,
                                  'country':cntry, 'region':rgn, 'city':cty} )            
        
        line1 = self.__get_random_string(20)
        line2 = self.__get_random_string(20)
        if (cust_id == 0):
            cust_id = self.get_last_customer_id()
        pcode = self.__get_random_int(5)
        cntry = self.__get_random_string(8)
        rgn = self.__get_random_string(5)
        cty = self.__get_random_string(6)        
                    
        self._engine.transaction(do_sql_script, cust_id, line1, 
                                 line2, pcode, cntry, rgn, cty)
    
    def add_random_order(self, cust_id=0, addr_id=0):
        '''
        Add random order for the specified customer and  address
        
        :Args:
            cust_id = int, customer id
                (if not set or 0, then last customer used).
            addr_id = int, address id
                (if not set or 0, then last address for customer used).
        '''
        
        def do_sql_script(conn, cid, aid):
            script = text("""SELECT create_order(:cust_id,:addr_id);""")
            conn.execute(script, {'cust_id':cid, 'addr_id':aid} )       
        
        if (cust_id == 0):
            cust_id = self.get_last_customer_id()
        if (addr_id == 0):
            addr_id = self.get_last_address_id(cust_id)
        
        self._engine.transaction(do_sql_script, cust_id, addr_id)
    
    def get_last_order_id(self, cust_id=0, addr_id=0):
        '''
        Get last added Order id for specified customer and address
        
        :Args:
            cust_id = int, customer id
                (if not set or 0, then last customer used).
            addr_id = int, address id
                (if not set or 0, then last address for customer used).
        '''
        if (cust_id == 0):
            cust_id = self.get_last_customer_id()
        if (addr_id == 0):
            addr_id = self.get_last_address_id(cust_id)
        
        session = sessionmaker(bind=self._engine)()
        inst = session.query(Orders).filter(Orders.key_customer == cust_id).\
                filter(Orders.key_address == addr_id).\
                order_by(Orders.id_order.desc()).first()
        i = 0
        if inst != None:
            i = inst.id_order
        
        return i
    
    def make_order_deliverd(self, order_id=0):
        '''
        Mark order as delivered.
        
        :Args:
            order_id - int, Order id
                (if not set or 0, then last oder used).
        '''
        def do_sql_script(conn, oid):
            script = text("""SELECT deliver_order(:oid,'auto');""")
            conn.execute(script, {'oid':oid} ) 
        
        if (order_id == 0):
            order_id = self.get_last_order_id()
        
        self._engine.transaction(do_sql_script, order_id)
    
    def randomly_fill_db(self, customers=1000):
        '''
        Fill DB with random values.
        
        :Args:
            customers - int, number of customers
                (default value 1000).
        '''
        for i in xrange(customers):
            self.add_random_customer()
            
            self.add_random_address()
            if ((i % 2) != 0): self.add_random_address()
            
            for j in xrange(i / 2):
                self.add_random_order()
                if ((j % 2) == 0):
                    self.make_order_deliverd()
                 

if __name__ == '__main__':
    act = Actions(True)
    act.randomly_fill_db(10)