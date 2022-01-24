from pyo import *


class FMp(PyoObject):

    def __init__(self, carrier_frequency=440, modulation_freq=0.5, modulation_index=100, mul=1, add=0):
        # Properly initialize PyoObject's basic attributes
        PyoObject.__init__(self, mul, add)

        # Keep references of all raw arguments
        self._carrier_freq = carrier_frequency
        self._modulation_freq = modulation_freq
        self._modulation_index = modulation_index

        # Apply processing
        self._modulator = Sine(freq=self._modulation_freq, mul=self._modulation_index, add=self._carrier_freq)
        self._carrier = Sine(freq=self._modulator)

        # self._base_objs is the audio output seen by the outside world!
        self._base_objs = self._carrier.getBaseObjects()

    def setCarrierFreq(self, x):
        print("set carrier freq")
        self._carrier_freq = x
        self._modulator.add = x

    def setModulationFreq(self, x):
        print("set modulation freq")
        self._modulation_freq = x
        self._modulator.freq = x

    def setModulationIndex(self, x):
        print("set modulation index")
        self._modulation_index = x
        self._modulator.mul = x

    @property  # getter
    def carrier_freq(self):
        """PyoObject. Input signal to process."""
        return self._carrier_freq

    @carrier_freq.setter  # setter
    def carrier_freq(self, x):
        self.setCarrierFreq(x)

    @property
    def modulation_freq(self):
        """float or PyoObject. Frequency of the modulator."""
        return self._modulation_freq

    @modulation_freq.setter
    def modulation_freq(self, x):
        self.setModulationFreq(x)

    @property
    def modulation_index(self):
        """float or PyoObject. Frequency of the modulator."""
        return self._modulation_index

    @modulation_index.setter
    def modulation_index(self, x):
        self.setModulationIndex(x)

    def play(self, dur=0, delay=0):
        self._modulator.play(dur, delay)
        return PyoObject.play(self, dur, delay)

    def stop(self, wait=0):
        self._modulator.stop(wait)
        return PyoObject.stop(self, wait)

    def out(self, chnl=0, inc=1, dur=0, delay=0):
        self._modulator.play(dur, delay)
        return PyoObject.out(self, chnl, inc, dur, delay)
