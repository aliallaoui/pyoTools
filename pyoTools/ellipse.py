from pyo import *


class Ellipse(PyoObject):

    def __init__(self, rotation_frequency=0.5, axis="x", phase=0.,
                 center_x=0., center_y=0., center_z=0.,
                 radius_x=1., radius_y=1., radius_z=1.):
        # Properly initialize PyoObject's basic attributes
        PyoObject.__init__(self)
        self._center_x = center_x
        self._center_y = center_y
        self._center_z = center_z
        self._radius_x = radius_x
        self._radius_y = radius_y
        self._radius_z = radius_z
        self._rotation_frequency = rotation_frequency
        self._axis = axis

        self._phase = phase

        if axis == "x":
            self._position = Sine(freq=self._rotation_frequency,
                                  add=self._center_x,
                                  mul=self._radius_x,
                                  phase=self._phase)
        elif axis == "y":
            self._position = Sine(freq=self._rotation_frequency,
                                  add=self._center_y,
                                  mul=self._radius_y,
                                  phase=self._phase)
        elif axis == "z":
            self._position = Sine(freq=self._rotation_frequency,
                                  add=self._center_z,
                                  mul=self._radius_z,
                                  phase=self._phase)
        else:
            raise Exception("Unknown axis " + axis)
        self._base_objs = self._position.getBaseObjects()

    @property
    def axis(self):
        return self._axis

    @axis.setter
    def axis(self, axis):
        self._axis = axis
        if axis == "x":
            self._position = Sine(freq=self._rotation_frequency,
                                  add=self._center_x,
                                  mul=self._radius_x,
                                  phase=self._phase)
        elif axis == "y":
            self._position = Sine(freq=self._rotation_frequency,
                                  add=self._center_y,
                                  mul=self._radius_y,
                                  phase=self._phase)
        elif axis == "z":
            self._position = Sine(freq=self._rotation_frequency,
                                  add=self._center_z,
                                  mul=self._radius_z,
                                  phase=self._phase)
        else :
            raise Exception("Unknown axis " + axis)

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self,phase):
        self._phase = phase
        self._position.phase = phase

    @property
    def rotation_frequency(self):
        return self._rotation_frequency

    @rotation_frequency.setter
    def rotation_frequency(self,rotation_frequency):
        self._rotation_frequency = rotation_frequency
        self._position.freq = rotation_frequency
        
    @property
    def center_x(self):
        return self._center_x

    @center_x.setter
    def center_x(self,center_x):
        self._center_x = center_x
        self._position.add = center_x

    @property
    def center_y(self):
        return self._center_y

    @center_y.setter
    def center_y(self, center_y):
        self._center_y = center_y
        self._position.add = center_y

    @property
    def center_z(self):
        return self._center_z

    @center_z.setter
    def center_z(self, center_z):
        self._center_z = center_z
        self._position.add = center_z

    @property
    def radius_x(self):
        return self._radius_x

    @radius_x.setter
    def radius_x(self, radius_x):
        self._radius_x = radius_x
        self._position.mul = radius_x

    @property
    def radius_y(self):
        return self._radius_y

    @radius_y.setter
    def radius_y(self, radius_y):
        self._radius_y = radius_y
        self._position.mul = radius_y

    @property
    def radius_z(self):
        return self._radius_z

    @radius_z.setter
    def radius_z(self, radius_z):
        self._radius_z = radius_z
        self._position.mul = radius_z

    def play(self, dur=0, delay=0):
        self._position.play(dur, delay)
        return PyoObject.play(self, dur, delay)

    def stop(self, wait=0):
        self._position.stop(wait)
        return PyoObject.stop(self, wait)

    def out(self, chnl=0, inc=1, dur=0, delay=0):
        self._position.play(dur, delay)
        return PyoObject.out(self, chnl, inc, dur, delay)


class EllipseX(Ellipse):

    def __init__(self, rotation_frequency=0.5, phase=0.,
                 center_x=0., center_y=0., center_z=0.,
                 radius_x=1., radius_y=1., radius_z=1.):
        Ellipse.__init__(self, rotation_frequency, "x", phase,
                         center_x, center_y, center_z,
                         radius_x, radius_y, radius_z)


class EllipseY(Ellipse):
    def __init__(self, rotation_frequency=0.5, phase=0.,
                 center_x=0., center_y=0., center_z=0.,
                 radius_x=1., radius_y=1., radius_z=1.):
        Ellipse.__init__(self, rotation_frequency, "y", phase,
                         center_x, center_y, center_z,
                         radius_x, radius_y, radius_z)


class EllipseZ(Ellipse):
    def __init__(self, rotation_frequency=0.5, phase=0.,
                 center_x=0., center_y=0., center_z=0.,
                 radius_x=1., radius_y=1., radius_z=1.):
        Ellipse.__init__(self, rotation_frequency, "z", phase,
                         center_x, center_y, center_z,
                         radius_x, radius_y, radius_z)
