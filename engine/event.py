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