# Event base class and subclasses. 
from abc import ABC, abstractmethod

class Event(ABC):
    '''Provides an interface for all inherited eventss.
    These events will be pushed to the 'First in First out' Event Queue.'''

    @property 
    # @property decorator allows us to define a method that can be accessed like an attribute. This is useful for defining read-only attributes or computed properties.
    @abstractmethod
    def type(self):
        ''' Returns the specific event type. 
        '''
        pass

#LEARNING

#By inheriting from ABC, python is told that this class is a 'template' 
#This means that you dont accidentally instantiate an empty event object. 

#The 'abstractmethod' decorator is used to define methods that must be implemented by any subclass

class MarketEvent(Event):
    '''The event type that singals a change in the market data.'''
    def __init__(self):
        self._type = 'MARKET'
    
    @property 
    def type(self): 
        '''Fufills ABC requirement. 
        '''
        return self._type

#This class indicantes that the market data has changed and the strategy should be run


# The following classes indicate a decision from the system - hence they inlcude data. 

class SignalEvent(Event):
    '''The event type that signals a trading signal.'''
    def __init__(self, symbol: str, datetime: str, signal_type: str): 
        self._type = 'SIGNAL'
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type
    


    @property 
    def type(self): 
        '''Fufills ABC requirement. 
        '''
        return self._type

class OrderEvent(Event):
    '''This handles the event of sending an order to the execution system.'''
    def __init__(self, symbol:str, order_type:str, quantity:int, direction:str):
        '''
        Parameters: 
        symbol: the ticker symbol, 'KO' for example
        order_type: 'MKT' or 'LMT' for market or limit orders
        quantity: the quantity of shares to be bought or sold
        direction: 'BUY' or 'SELL' for long or short'''

        self._type = 'ORDER'
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction

    @property 
    def type(self):
        '''Fufills ABC requirement. 
        '''
        return self._type
    

class FillEvent(Event):
    '''This handles the even of sending an order to the ExecutionHandler
    '''
    def __init__(self, timeindex:str, symbol:str, exchange:str, quantity:int, direction:str, fill_cost:float, commission:float=None):
        '''
        Parameters
        timeindex - The bar-resolution timestamp when the order was filled
        symbol - ticker symbol
        quantity - number of shares filled
        direction- Buying or selling
        fill_cost - the actual price of the trasnaction
        commission - transaction fee'''

        self._type = 'FILL'
        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost
        self.commission = commission if commission is not None else self.calculate_commission()
    @property

    def type(self):
        '''Fufills ABC requirement. 
        '''
        return self._type

    def calculate_commission(self):
        '''Default transaction fee'''

        return 1.00 + 0.01 * self.quantity

    



        