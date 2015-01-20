# import os.path
from subprocess import Popen, PIPE, STDOUT, CalledProcessError
# from subprocess import CalledProcessError
# from StringIO import StringIO
import tempfile

import magic
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import numpy as np


class Analyzer(object):

    def __init__(self, filename):
        fileinfo = magic.from_file(filename)
        if 'WAVE audio' in fileinfo:
            wav = open(filename)
        # elif 'MPEG ADTS, layer III' in fileinfo:
        else:
            wav = tempfile.NamedTemporaryFile()
            print wav.name
            # output = StringIO()
            try:
                p = Popen(
                    ['avconv', '-y', '-i', filename, '-f', 'wav', wav.name],
                    stdout=PIPE,
                    stderr=STDOUT)
                output, _ = p.communicate()
            except CalledProcessError:
                wav.close()
                print output
                raise ValueError('Error converting encoding to wav.')

        # if filename[-4:] == '.wav':
        #     newfilename = filename
        #     self.filename = filename
        # elif filename[-4:] == '.mp3':
        #     newfilename = filename[:-4]+'.wav'
        #     if os.path.isfile(newfilename):
        #         self.filename = newfilename
        #     else:
        #         call(['avconv','-i', filename, newfilename])
        #         self.filename = newfilename
        # else:
        #     raise ValueError('Unrecognized filetype.')
        # self._samplerate = self._data = None
        self._samplerate, data = read(wav)
        self.set_data(data)
        wav.close()

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
