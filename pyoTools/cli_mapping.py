import argparse
from pyoTools.mapping import Mapping
from pyo import *
import jack

class handler:

    def __init__(self, mappings, server, jclient):
        self.mappings = mappings
        self.server = server
        self.jclient = jclient

def mapping_cli():
    parser = argparse.ArgumentParser(description="Launch pyo server for controlling miPhysics")

    parser.add_argument('mapping',
                        help="Path of a json file describing the mapping")

    parser.add_argument('--values', '-v')
    parser.add_argument('--no-gui',dest="no_gui", action="store_true", default=False)
    args = parser.parse_args()
    mapping(args.mapping,args.values,args.no_gui)
    
def mapping(mapping, values, no_gui=True):
    mappings = Mapping(mapping, values)

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
            try:
                jclient.connect('pyo:output_' + str(m["channel"] + 1), 'miPhy:Input_' + str(m["channel"] + 1))
            except Exception as e:
                print(f"Could not connect {m} : {e}")

    if not no_gui:
        s.gui(locals())
    else:
        return handler(mappings,s,jclient)
