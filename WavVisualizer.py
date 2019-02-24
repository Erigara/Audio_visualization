# -*- coding: utf-8 -*-
"""
@author: Shanin Roman (Erigara)
@email: shanin1000@yandex.ru

Exmple of use animated plots to visuize wav data.
"""

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

import tkinter as tk

import Parsers as pr
import AnimatedPlots as ap

def _quit():
        root.quit()     
        root.destroy()  

def update(root, init, frames, redraw, delay):
    """
    root: tkinter.root
    init: callable - function to draw before first frame.
    redraw: callable - function called at each frame.
    delay: int - delay between frames in milliseconds.
    """
    frame_seq = frames()
    def start():
        def one_step():
            try:
                frame = next(frame_seq)
            except StopIteration:
                return
            redraw(frame)
            root.after(delay, one_step)
            return
        
        init()
        root.after(delay, one_step)
        return one_step
    return start

if __name__ == "__main__":
    # Data preparation
    parser = pr.StdInParser()
    wave_data = pr.RollingWindow(parser, 1764, 882)
    
    fig, (ax_l, ax_r) = plt.subplots(2,1)
    tmv = ap.TwoChanelsAnimatedPlot(ax_l, ax_r, wave_data, vmin=0, vmax=2**16)
    
    
    root = tk.Tk()
    root.wm_title("Wave visualizer")
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.draw()
   

    button = tk.Button(master=root, text='Quit', command=_quit)
    button.pack(side=tk.BOTTOM)

    updateAnim = update(root, tmv.init_draw, tmv.new_frame_seq, tmv.redraw, delay=1)
    
    root.after_idle(updateAnim)
    tk.mainloop()