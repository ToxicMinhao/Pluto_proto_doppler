import numpy as np
from gnuradio import gr

class signal_source_chirp(gr.sync_block):
    """
    A Python block that generates a linear chirp signal in GNU Radio.
    """
    def __init__(self, samp_rate = 1, start_freq = 0, end_freq = 0, duration = 1, amplitude = 0, offset = 0, initial_phase = 0):
        gr.sync_block.__init__(self, name='Signal Source Chirp', in_sig=None, out_sig=[np.complex64])
        self.samp_rate = samp_rate
        self.start_freq = start_freq
        self.end_freq = end_freq
        self.amplitude = amplitude
        self.offset = offset
        self.initial_phase = initial_phase
        self.duration = duration
        self.num_samples = int(duration * samp_rate)
        self.frequency_slope = (end_freq - start_freq) / self.num_samples
        self.phase = initial_phase
        self.sample_count = 0

    def work(self, input_items, output_items):
        t = np.arange(self.sample_count, self.sample_count + len(output_items[0]))
        phase_t = 2 * np.pi * (self.start_freq * t + 0.5 * self.frequency_slope * t**2) / self.samp_rate + self.initial_phase
        output_items[0][:] = self.amplitude * np.exp(1j * phase_t) + self.offset
        self.sample_count += len(output_items[0])
        return len(output_items[0])