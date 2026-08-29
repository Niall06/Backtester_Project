# Data handler classes.
from abc import ABC, abstractmethod
import numpy as np 
import pandas as pd
import os
from engine.event import MarketEvent
class DataHandler(ABC):
    """
    DataHandler is an abstract base class providing an interface for
    all subsequent (inherited) data handlers (both live and historic).
    """

    @abstractmethod
    def get_latest_bar(self, symbol: str):
        """
        Returns the last bar updated for a given symbol.
        """
        pass

    @abstractmethod
    def get_latest_bars(self, symbol: str, N: int = 1):
        """
        Returns the last N bars updated for a given symbol.
        """
        pass

    @abstractmethod
    def update_bars(self):
        """
        Pushes the latest bar to the latest_symbol_data structure
        for all symbols in the symbol list and places a MarketEvent
        on the queue.
        """
        pass

class HistoricCSVDataHandler(DataHandler):
    ''' Historic CSV Data Handler 
    '''

    def __init__(self, events, csv_dir, symbol_list,):
        """
        Initialises the historic data handler by requesting
        the location of the CSV files and a list of symbols.

        It will be assumed that all files are of the form
        'symbol.csv', where symbol is a string in the list.

        Parameters:
        events - The Event Queue.
        csv_dir - Absolute directory path to the CSV files.
        symbol_list - A list of symbol strings.
        """
        self.events = events
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list
        self.continue_backtest = True

        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.symbol_data_iter = {}

        for s in self.symbol_list:
            self.symbol_data[s] = pd.read_csv(
                os.path.join(self.csv_dir, f"{s}.csv"),
                    index_col = 0,
                    parse_dates = True)
            self.symbol_data_iter[s] = self.symbol_data[s].itterows()
            self.latest_symbol_data[s] = []

    def update_bars(self):
        for s in self.symbol_list:
            try:
                bar = next(self.symbol_data_iter[s])
            except StopIteration:
                self.continue_backtest = False
                return
            else: 
                if bar is not None:
                    self.latest_symbol_data[s].append(bar)
            
            self.events.put(MarketEvent())

    def get_latest_bar(self, symbol=str):
        try:
            return self.latest_symbol_data[symbol][-1]
        except KeyError:
            print(f"Symbol {symbol} is not available in the historical data set.")
            return None

    def get_latest_bars(self, symbol, N: int = 1):
        try:
            return self.latest_symbol_data[symbol][-N:]
        except KeyError:
                print(f"Symbol {symbol} is not available in the historical data set.")
                return None

        




