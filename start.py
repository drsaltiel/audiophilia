from scipy.io.wavfile import read
import matplotlib.pyplot as plt


class Analyzer(object):

    def __init__(self, filename):
        self.filename = filename
        self._samplerate = self._data = None
        self._samplerate, data = read(filename)
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
