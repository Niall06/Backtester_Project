#Position sizing and risk tracking
from abc import ABC, abstractmethod


class Portfolio(ABC):
    '''Provides an interface for all portfolios ensuring they each contain all the required data.
    Handles the position and market data at a resolution of a bar'''
    @abstractmethod
    def update_signal(self,event):
        """
        Acts on a SignalEvent to generate new orders
        based on portfolio logic.
        """
        pass
    @abstractmethod
    def update_fill(self,event):
        '''Updates the portfolio current positions and holdings
        from a FillEvent.'''
        pass


class NaivePortfolio(Portfolio):

    def __init__(self, events, bars, start_date, initial_capital = 100000.0):

        self.events = events
        self.bars = bars
        self.start_date = start_date
        self.initial_capital = initial_capital
        self.symbol_list = self.bars.symbol_list
        self.current_positions = {}
        self.current_holdings = {}

        self.all_positions = []
        self.all_holdings = []

        self.current_holdings['cash'] = self.initial_capital
        self.current_holdings['commission'] = 0.0
        self.current_holdings['total'] = self.initial_capital
        for s in self.symbol_list:
            self.current_positions[s] = 0 
            self.current_holdings[s] = 0.0
        self.all_positions.append(self.current_positions.copy())
        self.all_holdings.append(self.current_holdings.copy())

    


