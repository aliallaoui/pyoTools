import argparse
from pyoTools.mapping import Mapping
from pyo import *
import jack


def mapping():
    parser = argparse.ArgumentParser(description="Launch pyo server for controlling miPhysics")

    parser.add_argument('mapping',
                        help="Path of a json file describing the mapping")

    parser.add_argument('--values', '-v')

    args = parser.parse_args()
    mappings = Mapping(args.mapping, args.values)

    s = Server(audio='jack', nchnls=mappings.nb_input_channels, ichnls=2)
    jclient = jack.Client("mapping")
    pm_list_devices()
    s.setMidiInputDevice(99)  # Open all input devices.
    s.boot()
    mappings.load()
    jclient.disconnect('pyo:output_1', 'system:playback_1')
    jclient.disconnect('pyo:output_2', 'system:playback_2')
    for m in mappings.mappings:
        if "channel" in m.keys():
            jclient.connect('pyo:output_' + str(m["channel"] + 1), 'miPhy:Input_' + str(m["channel"] + 1))

    s.gui(locals())
