import matplotlib.pyplot as plt
import numpy as np

from .reader import read_maybe_convert


class Analyzer(object):

    def __init__(self, filepath):
        self._samplerate, data = read_maybe_convert(filepath)
        self.set_data(data)

    @property
    def samplerate(self):
        return self._samplerate

    @property
    def data(self):
        return self._data

    def set_data(self, value):
        self._data = value
        self._ldata = [d[0] for d in self._data]
        self._rdata = [d[1] for d in self._data]

    @property
    def rdata(self):
        return self._rdata

    @property
    def ldata(self):
        return self._ldata

    def plotr(self):
        self._plot(self.rdata)

    def plotl(self):
        self._plot(self.ldata)

    def _plot(self, data):
        plt.plot(range(len(data)), data)
        plt.show()

    @property
    def fft_rdata(self):
        return np.fft.fft(self.rdata)

    @property
    def fft_ldata(self):
        return np.fft.fft(self.ldata)

    def plot_fftr(self):
        self._plot(np.fft.fftshift(self.fft_rdata))

    def plot_fftl(self):
        self._plot(np.fft.fftshift(self.fft_ldata))
