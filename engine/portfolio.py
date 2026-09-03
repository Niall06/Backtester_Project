#Position sizing and risk tracking
from abc import ABC, abstractmethod
from engine.event import OrderEvent

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

    def update_timeindex(self, event):
        #This method updates the to the current timestamp and adjusts the portfolio accordingly
        total_stock_holdings = 0.0
        for s in self.symbol_list:
            self.current_holdings[s] = self.current_positions[s]*self.bars.get_latest_bar(s)[1]['Close']
            total_stock_holdings += self.current_holdings[s]
        date_time = self.bars.get_latest_bar(self.symbol_list[0])[0]
        self.current_holdings['datetime'] = date_time
        self.current_positions['datetime'] = date_time
        self.current_holdings['total'] = total_stock_holdings + self.current_holdings['cash']
        self.all_holdings.append(self.current_holdings.copy())
        self.all_positions.append(self.current_positions.copy())
        # Must do both so that the positions and holdings are synchronised

    def update_fill(self, event):

        s = event.symbol
        if event.direction == 'BUY':
            self.current_positions[s] += event.quantity
            self.current_holdings['cash'] -= event.fill_cost
        elif event.direction == 'SELL':
            self.current_positions[s] -= event.quantity
            self.current_holdings['cash'] += event.fill_cost
        self.current_holdings['cash'] -= event.commission
        self.current_holdings['commission'] += event.commission

    def update_signal(self,event):
        # 1. Initialize order ticket blueprint
        Order = OrderEvent(event.symbol, 'MKT', 0 ,None)
        
        # 2. Check signal intent
        if event.signal_type == 'LONG':
            Order.direction = 'BUY'
            Order.quantity = 100

        elif event.signal_type == 'SHORT':
            Order.direction= 'SELL'
            Order.quantity = 100

        elif event.signal_type == 'EXIT':
            Order.quantity = abs(self.current_positions[event.symbol])

            if self.current_positions[event.symbol] > 0:
                Order.direction = 'SELL'
            elif self.current_positions[event.symbol] < 0:
                Order.direction = 'BUY'
            elif self.current_positions[event.symbol] == 0:
                Order.direction = None
                Order.quantity = 0
        # 3. Guard clause: only push valid orders
        if Order.direction and Order.quantity > 0:
            self.events.put(Order)

            
            



