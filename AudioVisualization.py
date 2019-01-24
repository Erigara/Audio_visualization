# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 18:33:07 2018

@author: user
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import ReadDataScript as rds
import sys

class TwoChanelsMovingPlot:
    """
    Класс, отображающий график.
    Вход: класс WaweData, предоставляющий данные для отображения
    @Создает линию которая будет перерисовываться;
    @Задает облать отрисовки.
    """
    def __init__(self, l_ax, r_ax,  wave_data):
       """
       ax: Axes -  Координатная сетка, на которой будет отображаться график.
       wawe_data: Wave_data - итерируемый объект, 
                              который формирует новые данные (plot_data) для отрисовки
                              и предоставляет их для MovingWave при вызове
                              moving_wave(plot_data) === MovingWave.__call__(moving_wave, plot_data)
       """
       self.wave_data = wave_data
       self.l_line, = l_ax.plot([], [], 'k-')
       self.r_line, = r_ax.plot([], [], 'k-')
       self.l_ax = l_ax
       self.l_ax.set_ylim(-1, 1)
       self.l_ax.grid(True)
       self.r_ax = r_ax
       self.r_ax.set_ylim(-1, 1)
       self.r_ax.grid(True)
       
    def init(self):
        def start_init(ax, line):
             ax.set_xlim(0, 1)
             ax.figure.canvas.draw()
             line.set_data([], [])
             return line
        return start_init(self.l_ax, self.l_line), start_init(self.r_ax, self.r_line)  
    
    def __call__(self, plot_data):
        """
        Обновляет данные графика для нового кадра.
        plot_data: tuple - кортеж, предоставляемый self.wave_data имеет следующую структуру:
                                                    (x, y)        
                                                    x - значения по оси oX;
                                                    y - значения по оси oY.
        """
        def update_plot(plot, line, x, y):
            left_xlim = x[0]
            right_xlim = x[0]+self.wave_data.getWindowSize()//2-1
            plot.set_xlim(left_xlim, right_xlim)
            plot.figure.canvas.draw()
            line.set_data(x, y)
            return line
        
        if plot_data:
            x, y = plot_data
            left_chanel_indexes = x % 2 == 0
            right_chanel_indexes = ~left_chanel_indexes
            x_l = x[left_chanel_indexes]//2
            y_l = y[left_chanel_indexes]/2**15 - 1
            x_r = x[right_chanel_indexes]//2
            y_r = y[right_chanel_indexes]/2**15 - 1
            return (update_plot(self.l_ax, self.l_line, x_l, y_l),
                    update_plot(self.r_ax, self.r_line, x_r, y_r))
        else: 
            return (self.l_line, self.r_line)
        
class MovingPlot:
     """
    Класс, отображающий график.
    Вход: класс WaweData, предоставляющий данные для отображения
    @Создает линию которая будет перерисовываться;
    @Задает облать отрисовки.
    """
     def __init__(self, ax,  wave_data):
       """
       ax: Axes -  Координатная сетка, на которой будет отображаться график.
       wawe_data: Wave_data - итерируемый объект, 
                              который формирует новые данные (plot_data) для отрисовки
                              и предоставляет их для MovingWave при вызове
                              moving_wave(plot_data) === MovingWave.__call__(moving_wave, plot_data)
       """
       self.wave_data = wave_data
       self.line, = ax.plot([], [], 'k-')
       self.ax = ax
       self.ax.set_ylim(-1, 1)
       self.ax.grid(True)
       
     def init(self):
        self.ax.set_xlim(0, 1)
        self.ax.figure.canvas.draw()
        self.line.set_data([], [])
        return self.line,
    
     def __call__(self, plot_data):
        """
        Обновляет данные графика для нового кадра.
        plot_data: tuple - кортеж, предоставляемый self.wave_data имеет следующую структуру:
                                                    (x, y)        
                                                    x - значения по оси oX;
                                                    y - значения по оси oY.
        """
        if plot_data:
            x, y = plot_data
            left_xlim = x[0]
            right_xlim = x[0]+self.wave_data.getWindowSize()-1
            self.ax.set_xlim(left_xlim, right_xlim)
            self.ax.figure.canvas.draw()
            self.line.set_data(x, y)
        return self.line, 
    
if __name__ == "__main__":
    parser = rds.CommandLineParser()
    wave_data = rds.WaveData(parser, 1684, 842)
    fig, (ax_l, ax_r) = plt.subplots(1,2)
    #mv = MovingWave(ax1, wave_data)
    tmv = TwoChanelsMovingPlot(ax_l, ax_r, wave_data)
    anim = FuncAnimation(fig, tmv, frames = tmv.wave_data, init_func = tmv.init,
                         interval=10, blit=True, repeat= True)
    #Writer = animation.writers["ffmpeg"]
    #writer = Writer(fps=15, bitrate= 1080)
    #anim.save("two_chanels.mp4", writer)
    plt.show()
    sys.exit(0);