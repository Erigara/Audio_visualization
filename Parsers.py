# -*- coding: utf-8 -*-
"""
@author: Shanin Roman (Erigara)
@email: shanin1000@yandex.ru

Module to deal with values in file/stdin separated by some delimeters.
Include funclionality to create rolling windows from that values.
"""
import sys


class FileParser:
    """
    Class FileParser - parser that take file name 
    and return values splitted by separators of that file one by one.
    To start iteration call: iter(file_parser)
    Then iterable object handeled as common iterator.
    """
    def __init__(self, filename, separators = [" ",]):
        """
        filename: String
        separators: List - list of separators that separete data points.
        """
        self.filename = filename
        self.separators = separators
        self.separators.append("")
        self.separators.append("/n")
    def __iter__(self):
        """
        Use to create iterator througth data values in file.
        """
        states = {"EndOfFile": 0, "IsGoing": 1}
        def getNextValue(current_state):
            value = []
            char = file.read(1)
            while not char in self.separators:
                value.append(char)
                char = file.read(1)
            if char == '':
                current_state = states["EndOfFile"]
            result =  "".join(value)
            return result, current_state
        with open(self.filename, "r") as file:
            current_state = states["IsGoing"]
            new_value, current_state = getNextValue(current_state)
            while current_state == states["IsGoing"]:
                yield new_value
                new_value, current_state = getNextValue(current_state)
            if new_value != "":
                yield new_value
                
class StdInParser:
    """
    Class StdInParser - parser that 
    return values from standart input that splitted by separators.
    To start iteration call: iter(file_parser)
    Then iterable object handeled as common iterator.
    """
    def __init__(self, separators = [" ",]):
        """
        separators: List - list of separators that separete data points.
        """
        self.separators = separators
        self.separators.append("")
        self.separators.append("\n")
    def __iter__(self):
        """
        Use to create iterator througth data values in file.
        """
        states = {"EndOfFile": 0, "IsGoing": 1}
        def getNextValue(current_state):
            value = []
            char = file.read(1)
            while not char in self.separators:
                value.append(char)
                char = file.read(1)
            if char == '' or  char == '\n':
                current_state = states["EndOfFile"]
                file.seek(0)
            result =  "".join(value)
            return result, current_state
        file = sys.stdin
        current_state = states["IsGoing"]
        new_value, current_state = getNextValue(current_state)
        while current_state == states["IsGoing"]:
            yield new_value
            new_value, current_state = getNextValue(current_state)
        if new_value != "":
            yield new_value  
        
        
class RollingWindow:
    """
    Class RollingWindow- use to create rolling window iterable obejct from iterator.    
    """
    def __init__(self, parser,  window_size = 100, number_of_updated_values = 1):
        """
        parser: iterator
        window_size: int - current window size
        number_of_updated_values: int - number of values that added to winodow and deleted from it per iteration. 
        """
        self.parser = parser
        self.window_size = window_size
        self.number_of_updated_values =  number_of_updated_values
    def setWindowSize(self, window_size):
        self.winodw_size = window_size
    def getWindowSize(self):
        return self.window_size
    def setNumberOfUpdatedValues(self, number_of_updated_values):
        self.number_of_updated_values =  number_of_updated_values
    def getNumberOfUpdatedValues(self):
        return self.number_of_updated_values
   
    def __iter__(self):
        """
        Generator function that return windows created from data in parser.
        Example of usage:
        >>> roling_window = RollingWindow([1,2,3,4,5], 2, 1)
        >>> iterable_window = roling_window()
        >>> for window in iterable_window:
        >>>     print window
        Output:
        [1,2]
        [2,3]
        [3,4]
        [4,5]
        [5,]
        """
        states = {"StopIteration": 0, "IsGoing": 1}
        def new_window(seq, state):
            nonlocal current_window
            try:
                if current_window:
                    current_window = current_window[self.number_of_updated_values:]
                while len(current_window) < self.window_size:
                      current_window.append(next(seq))
            except StopIteration:
                state = states["StopIteration"]
            finally:    
               if current_window:
                   return current_window.copy(), state
               else: 
                   return None, state
        seq = iter(self.parser)
        current_window = []
        current_state = states["IsGoing"]
        new_value, current_state = new_window(seq, current_state)
        while current_state == states["IsGoing"]:
             yield new_value
             new_value, current_state = new_window(seq, current_state)
        if new_value:
            yield new_value