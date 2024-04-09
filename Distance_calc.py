import numpy as np
from gnuradio import gr


class Distance_calc(gr.sync_block):
    """
    A custom GNU Radio block to calculate velocity from a simulated frequency shift.

    Attributes:
        transmitted_freq (float): The frequency of the transmitted signal in Hz.
        speed_of_light (float): The speed of light in meters per second, typically 3e8.
    """
    def __init__(self, slope=500, speed_of_light=3e8, samp_rate=40000, fft_size = 8192):
        gr.sync_block.__init__(self, name="Distance_calc", in_sig=[np.float32], out_sig=[np.float32])
        self.slope = slope
        self.speed_of_light = speed_of_light
        self.samp_rate = samp_rate
        self.fft_size = fft_size

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        input_max = np.argmax(in0)
        frequency_bin_width = self.samp_rate / self.fft_size
        delta_f = (input_max - 4095) * frequency_bin_width
        distance = np.abs(self.slope * delta_f * (self.speed_of_light / 2))
        out[:] = distance
        return len(output_items[0])