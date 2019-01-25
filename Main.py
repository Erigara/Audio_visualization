# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 20:28:21 2019

@author: user
"""

import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import ReadDataScript as rds
import AudioVisualization as av

def update(root, time, init, frames, redraw):
    frame_seq = frames()
    def start():
        def one_step():
            try:
                frame = next(frame_seq)
            except StopIteration:
                return
            redraw(frame)
            root.after(time, one_step)
            return
        
        init()
        root.after(time, one_step)
        return one_step
    return start

if __name__ == "__main__":
    # Data preparation
    parser = rds.CommandLineParser()
    wave_data = rds.WaveData(parser, 1764, 882)
    fig, (ax_l, ax_r) = plt.subplots(1,2)
    tmv = av.TwoChanelsMovingPlot(ax_l, ax_r, wave_data)
    
    root = tk.Tk()
    root.wm_title("Embedding in TK")
    # a tk.DrawingArea
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    def _quit():
        root.quit()     # stops mainloop
        root.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate

    button = tk.Button(master=root, text='Quit', command=_quit)
    button.pack(side=tk.BOTTOM)

    updateAnim = update(root, 1, tmv.init, tmv.wave_data, tmv)
    
    root.after_idle(updateAnim)
    tk.mainloop()