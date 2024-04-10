import numpy as np
from gnuradio import gr


class average_speed(gr.sync_block): 
    def __init__(self, target_points = 262144):  
        gr.sync_block.__init__(self, name='average_speed', in_sig=[np.float32], out_sig=[np.float32])
        self.target_points = target_points


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        accumulated_points = np.array([])
        while accumulated_points.size < self.target_points:
            accumulated_points = np.concatenate((accumulated_points, in0))
        accumulated_points = accumulated_points[:self.target_points]
        sum_of_points = np.sum(accumulated_points)
        average = sum_of_points / self.target_points
        accumulated_points = np.array([])
        out[:] = average
        return len(output_items[0])
