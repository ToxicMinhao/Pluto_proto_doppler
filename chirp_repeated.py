import numpy as np
from gnuradio import gr

class signal_source_repeating_chirp(gr.sync_block):
    """
    A Python block that generates a repeating linear chirp signal in GNU Radio.
    """
    def __init__(self, samp_rate = 1, start_freq = 0, end_freq = 0, duration = 1, amplitude = 0, offset = 0, initial_phase = 0):
        gr.sync_block.__init__(
            self,
            name='Signal Source Repeating Chirp',  
            in_sig=None,                           
            out_sig=[np.complex64]                 
        )
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
        out = output_items[0]
        for i in range(len(out)):
            current_sample = self.sample_count % self.num_samples
            phase_t = (2 * np.pi * (self.start_freq * current_sample + 0.5 * self.frequency_slope * current_sample**2) / self.samp_rate) + self.initial_phase            
            out[i] = self.amplitude * np.exp(1j * phase_t) + self.offset
            self.sample_count += 1
            if current_sample == self.num_samples - 1:
                self.initial_phase = phase_t % (2 * np.pi)
                self.sample_count = 0  
        return len(out)

