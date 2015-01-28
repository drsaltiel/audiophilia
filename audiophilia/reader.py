import wave
import struct
import tempfile
from subprocess import Popen, PIPE, STDOUT

import numpy


def read_wav(f):
    '''
    Take a filepath or filehandle and try to parse it as a wave audio file.
    Return (sample_rate, data-frames(as a numpy array)). This mimics the
    signature of scipy.io.wavfile.read().
    '''
    close_file = False
    if isinstance(f, str):
        f = open(f, 'rb')
        close_file = True

    try:
        w = wave.open(f)
        nchannels, samp_width, framerate, nframes, _, _ = w.getparams()

        if nchannels > 2:
            raise ValueError('More than 2 channels not supported.')

        if samp_width == 1:
            c_type = 'B'  # unsigned char
        elif samp_width == 2:
            c_type = 'h'  # signed short
        else:
            raise ValueError('Sample width {} not supported.'
                             .format(samp_width))

        fmt = '<' + c_type * nchannels * nframes
        interleaved = struct.unpack(fmt, w.readframes(nframes))
        data = numpy.array(zip(*([iter(interleaved)] * nchannels)))

        return framerate, data

    finally:
        if close_file:
            f.close()


def read_maybe_convert(filepath):
    '''
    Try to read a file as a WAVE audio file. If not in WAVE format, attempt
    to convert it first, using a temporary file as output for the transcode.
    '''
    try:
        with open(filepath) as f:
            wave.open(f)
    except wave.Error:
        # try to convert to WAVE
        out = tempfile.NamedTemporaryFile()
        p = Popen(
            ['avconv', '-y', '-i', filepath, '-f', 'wav', out.name],
            stdout=PIPE,
            stderr=STDOUT)
        output, _ = p.communicate()
        if p.returncode != 0:
            out.close()
            print output
            raise ValueError('Error converting "{}" to WAVE format.'
                             .format(filepath))
        else:
            filepath = out.name

    return read_wav(filepath)
