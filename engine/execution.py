# Brokerage simulation and order execution.
from abc import ABC, abstractmethod
from engine.event import FillEvent
class ExecutionHandler(ABC):
    '''Simulates a live broker exchanges. '''
    @abstractmethod
    def execute_order(self, event):
        '''
        Takes and order event and executes it, producing a FillEvent that gest placed onto the events queue
        '''
        pass

class SimulatedExecutionHandler(ExecutionHandler):

    def __init__(self, events,  bars):
        self.events = events
        self.bars = bars

    def execute_order(self, event):
        if event.type == 'ORDER':
            date_time = self.bars.get_latest_bar(event.symbol)[0]
            fill_cost = self.bars.get_latest_bar(event.symbol)[1]['Close'] * event.quantity
            fill = FillEvent(date_time, event.symbol, 'NYSE', event.quantity, event.direction, fill_cost, None)

            self.events.put(fill)

