import numpy as np
from gnuradio import gr


class doppler_velocity_calc(gr.sync_block):
    def __init__(self, transmitted_freq=500, speed_of_light=3e8, samp_rate=40000, fft_size = 8192, carrier_freq=3.5e9):
        gr.sync_block.__init__(self, name="doppler_velocity_calc", in_sig=[np.float32], out_sig=[np.float32])
        self.transmitted_freq = transmitted_freq
        self.speed_of_light = speed_of_light
        self.samp_rate = samp_rate
        self.fft_size = fft_size
        self.carrier_freq = carrier_freq

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        part_of_in0 = in0[4050:8192]
        input_max = np.argmax(part_of_in0)
        frequency_bin_width = self.samp_rate / self.fft_size
        if np.max(part_of_in0) < 50:
            out[:] = 0
        else: 
            delta_f = (input_max - (4198-4050)) * frequency_bin_width
            velocity = (delta_f * self.speed_of_light) / (2*self.carrier_freq)
            out[:] = velocity
        return len(output_items[0])