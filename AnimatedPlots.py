# -*- coding: utf-8 -*-
"""
@author: Shanin Roman (Erigara)
@email: shanin1000@yandex.

Module contain classes for 1,2 channels plots.
"""
import numpy as np
import itertools


class AbstractAnimatedPlot:
    """
    Abstract class that contain interface for every real plot class.
    """
    def __init__(self, data):
        self.data = data
    def redraw(self, frame_date):
        raise Exception("Not supported yet!")
    def init_draw(self):
        raise Exception("Not supported yet!")
    def new_frame_seq(self):
        seq = iter(self.data)
        iter_number = itertools.count(0, 1)
        # map data seq with needed data transformation.
        return map(self.transform_data, seq, iter_number)
    def transform_data(self, seq, i):
        raise Exception("Not supported yet!")
        
class TwoChanelsAnimatedPlot(AbstractAnimatedPlot):
    """
    Animated plot that draw data in two different axes.
    """
    def __init__(self, l_ax, r_ax, wave_data, vmin=-1, vmax=1):
       """
       l_ax: Axes - left channel axes.
       r_ax: Axes - right channel axes.
       wawe_data: iterable object contain rolling window of data points
       vmax: int - maximum amplitude in data points
       vmin: minimum amplitude in data poinsts
       """
       self.data = wave_data
       self.vmin = vmin
       self.vmax = vmax
       # Left channel
       self.l_ax = l_ax
       self.l_line, = l_ax.plot([], [], 'k-')
       self.l_ax.set_ylim(vmin, vmax)
       self.l_ax.grid(True)
       # Right channel
       self.r_ax = r_ax
       self.r_line, = r_ax.plot([], [], 'k-')
       self.r_ax.set_ylim(vmin, vmax)
       self.r_ax.grid(True)
       
    def init_draw(self):
        """
        Draw before first frame.
        """
        def start_init(ax, line):
             ax.set_xlim(0, 1)
             ax.figure.canvas.draw()
             line.set_data([], [])
             return line
        return start_init(self.l_ax, self.l_line), start_init(self.r_ax, self.r_line)  
    
    def redraw(self, plot_data):
        """
        Redraw plots for every new frame.
        plot_data: tuple contain data point (x, y) for left and right axes.
        """
        def update_plot(plot, line, x, y):
            left_xlim = x[0]
            right_xlim = x[0] + self.data.getWindowSize()//2-1
            plot.set_xlim(left_xlim, right_xlim)
            plot.figure.canvas.draw()
            line.set_data(x, y)
            return line
        
        if plot_data:
            l, r = plot_data
            return (update_plot(self.l_ax, self.l_line, *l),
                    update_plot(self.r_ax, self.r_line, *r))
        else: 
            return (self.l_line, self.r_line)
    def transform_data(self, seq, i):
        """
        Needed transformation of data to properly visulize it.
        seq: container - rolling window of y
        i: int - number of current frame
        """
        if seq:
            y = np.array(seq, dtype = np.float)
            x = (np.arange(len(y))+i*self.data.getNumberOfUpdatedValues())
            left_chanel_indexes = x % 2 == 0
            right_chanel_indexes = ~left_chanel_indexes
            x_l = x[left_chanel_indexes]//2
            y_l = y[left_chanel_indexes]
            x_r = x[right_chanel_indexes]//2
            y_r = y[right_chanel_indexes]
            return ((x_l, y_l), (x_r, y_r))
        else:
            return None


class OneChannelAnimatedPlot(AbstractAnimatedPlot):
     """

     """
     def __init__(self, ax,  wave_data):
       """
       ax: Axes
       wawe_data: iterable object contain rolling window of data points
       """
       self.wave_data = wave_data
       self.line, = ax.plot([], [], 'k-')
       self.ax = ax
       self.ax.set_ylim(-1, 1)
       self.ax.grid(True)
       
     def init_draw(self):
        self.ax.set_xlim(0, 1)
        self.ax.figure.canvas.draw()
        self.line.set_data([], [])
        return self.line,
    
     def redraw(self, plot_data):
        """
        Redraw plots for every new frame.
        plot_data: tuple contain data point (x, y)
        """
        if plot_data:
            x, y = plot_data
            left_xlim = x[0]
            right_xlim = x[0]+self.wave_data.getWindowSize()-1
            self.ax.set_xlim(left_xlim, right_xlim)
            self.ax.figure.canvas.draw()
            self.line.set_data(x, y)
        return self.line, 

     def transform_data(self, seq, i):
        """
        Needed transformation of data to properly visulize it.
        seq: container - rolling window of y
        i: int - number of current frame
        """
        if seq:
            y = np.array(seq, dtype = np.float)/2**15 - 1
            x = (np.arange(len(y))+i*self.data.getNumberOfUpdatedValues())
            return x, y
        else:
            return None
