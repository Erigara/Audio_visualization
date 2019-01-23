# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 20:26:50 2019

@author: user
"""
import numpy as np
import sys
class FileParser:
    """
    Класс FileParser - генератор, 
    возвращающий элементы файла разделенные символами разделителями. 
    """
    def __init__(self, filename, separators = [" ",]):
        """
        filename: String - имя(путь) до файла, 
                           из которого будут считываться данные.
        separators: List - Список разделителей по, 
                           которым следует разделять элементы данных
        """
        self.filename = filename
        self.separators = separators
        self.separators.append("")
    def __iter__(self):
        """
        Переоткрывает файл и создает генератор по его значениям.
        """
        states = {"EndOfFile": 0, "IsGoing": 1}
        def getNextValue(current_state):
            # Не допускать вывод конца строки
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
                
class CommandLineParser:
    """
    Класс CommandLineParser - генератор, 
    возвращающий элементы стандартного ввода разделенные символами разделителями. 
    """
    def __init__(self, separators = [" ",]):
        """
        separators: List - Список разделителей по, 
                           которым следует разделять элементы данных
        """
        self.separators = separators
        self.separators.append("")
    def __iter__(self):
        """
        Переоткрывает файл и создает генератор по его значениям.
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
        file = sys.stdin
        file.seek(0)
        current_state = states["IsGoing"]
        new_value, current_state = getNextValue(current_state)
        while current_state == states["IsGoing"]:
            yield new_value
            new_value, current_state = getNextValue(current_state)
        if new_value != "":
            yield new_value  
        
        
class WaveData():
    def __init__(self, parser,  window_size = 100, number_of_updated_values = 1):
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
   
    def __call__(self):
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
                   y = np.array(current_window, dtype = np.float64)
                   x = np.arange(len(current_window)) + (number_of_iterations * self.number_of_updated_values)
                   return (x, y), state
               else: 
                   return None, state
               
         seq = iter(self.parser)
         current_window = []
         current_state = states["IsGoing"]
         number_of_iterations = 0
         new_value, current_state = new_window(seq, current_state)
         while current_state == states["IsGoing"]:
             yield new_value
             number_of_iterations +=1
             new_value, current_state = new_window(seq, current_state)
         if new_value:
            yield new_value
             