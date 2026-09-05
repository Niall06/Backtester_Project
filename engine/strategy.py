# Statistical arbitrage strategy Logic. 

from abc import ABC, abstractmethod
from engine.event import MarketEvent
import numpy as np
class Strategy(ABC):
    '''It defines the interface for any trading strategy so the information can be sent to the central engine'''

    @abstractmethod
    def calculate_signals(self, event):
        '''When a market event happens, the engine performs the strategy
        Then generates a signal 
        '''
        pass
   


class PairsTradingStrategy(Strategy):
    '''The pairs trading society
    '''
    def __init__(self, events, bars, symbol_1, symbol_2 ,w=30, b=1.25, z_in = 2.0, z_out= 0.5  ):

        self.events = events
        self.bars = bars
        self.symbol_1 = symbol_1
        self.symbol_2 = symbol_2
        self.w = w
        self.b = b
        self.z_in = z_in
        self.z_out = z_out

        self.in_market = False

    def calculate_signals(self, event):
        if event.type == 'MARKET':
            bars_1 = self.bars.get_latest_bars(self.symbol_1, self.w)
            bars_2 = self.bars.get_latest_bars(self.symbol_2, self.w)
            if len(bars_1) >= 30 and len(bars_2) >= self.w:

                closing_prices_1 = []


            