# Statistical arbitrage strategy Logic. 

from abc import ABC, abstractmethod
from engine.event import MarketEvent 
from engine.event import SignalEvent
import numpy as np
from statsmodels.tsa.stattools import adfuller
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
    def __init__(self, events, bars, symbol_1, symbol_2 ,w=30, z_in = 2.0, z_out= 0.5  ):

        self.events = events
        self.bars = bars
        self.symbol_1 = symbol_1
        self.symbol_2 = symbol_2
        self.w = w
        self.z_in = z_in
        self.z_out = z_out

        self.position = 'OUT'

    def calculate_signals(self, event):
        if event.type == 'MARKET':
            bars_1 = self.bars.get_latest_bars(self.symbol_1, self.w)
            bars_2 = self.bars.get_latest_bars(self.symbol_2, self.w)
            
            if len(bars_1) >= self.w and len(bars_2) >= self.w:
                datetime = bars_1[-1][0]
                closing_prices_1 = np.array([b[1]['Close'] for b in bars_1], dtype = np.float64)
                closing_prices_2 = np.array([b[1]['Close'] for b in bars_2], dtype = np.float64)

                beta, alpha = np.polyfit(closing_prices_2, closing_prices_1, deg = 1)
                
                #Calculate the spread
                spread = closing_prices_1 - (alpha+ beta* closing_prices_2)

                #perform adf test
                adf_result = adfuller(spread)

                if adf_result[1]< 0.05:

                #find standard deviation
                    
                    standard_deviation = np.std(spread, ddof= 1)
                    # find spread at this current time and then calculate the z-score
                    if standard_deviation == 0:
                        return

                    spread_t = spread[-1]
                    z_t = spread_t/standard_deviation

                    if self.position != 'OUT' and abs(z_t) <= self.z_out:
                        signal_1 = SignalEvent(self.symbol_1, datetime, 'EXIT')
                        signal_2 = SignalEvent(self.symbol_2, datetime, 'EXIT')
                        self.events.put(signal_1)
                        self.events.put(signal_2)
                        self.position = 'OUT'


                    elif self.position == 'OUT' and z_t < -self.z_in:
                        signal_1 = SignalEvent(self.symbol_1, datetime, 'LONG')
                        signal_2 = SignalEvent(self.symbol_2, datetime, 'SHORT')
                        self.events.put(signal_1)
                        self.events.put(signal_2)
                        self.position = 'LONG'
                    elif self.position == 'OUT' and z_t > self.z_in:
                        signal_1 = SignalEvent(self.symbol_1, datetime, 'SHORT')
                        signal_2 = SignalEvent(self.symbol_2, datetime, 'LONG')
                        self.events.put(signal_1)
                        self.events.put(signal_2)
                        self.position = 'SHORT'
                            
                else:
                    if  self.position != 'OUT':
                        signal_1 = SignalEvent(self.symbol_1, datetime, 'EXIT')
                        signal_2 = SignalEvent(self.symbol_2, datetime, 'EXIT')
                        self.position = 'OUT'

                        self.events.put(signal_1)
                        self.events.put(signal_2)


                    





            