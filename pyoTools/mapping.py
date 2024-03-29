import datetime
import shutil
from pyo import *
from .fm import *
from .ellipse import *
import json


class Mapping:
    def __init__(self, mapping_path, auxiliary_values_path=None):
        self.controls = dict()
        with open(mapping_path) as f:
            self.mappings = json.load(f)
        if auxiliary_values_path is not None:
            with open(auxiliary_values_path) as f:
                self.values = json.load(f)
        else:
            self.values = None
        self.nb_input_channels = 0
        for m in self.mappings:
            if "channel" in m.keys():
                self.nb_input_channels = self.nb_input_channels + 1
        self.fadetime = 5
        
    def load(self):
        for m in self.mappings:
            self.controls[m['parameter']] = dict()
            if "pyoo" in m.keys():
                if m["pyoo"] not in globals():
                    raise Exception("Pyo object " + m["pyoo"] + " does not exist")
                self.controls[m['parameter']]["pyoo"] = globals()[m["pyoo"]]().out(m["channel"])
                self.nb_input_channels = self.nb_input_channels + 1
                self.controls[m['parameter']]["ctrls"] = dict()
                for c in m["controls"]:
                    if 'ctrl' in c:
                        self.controls[m['parameter']]["ctrls"][c["parameter"]] = dict()
                        a = self.controls[m['parameter']]["ctrls"][c["parameter"]]
                        a["midictl"] = Midictl(ctlnumber=c['ctrl'],
                                               minscale=c['min'],
                                               maxscale=c['max'])
                        a["portamento"] = Port(a["midictl"])
                        setattr(self.controls[m['parameter']]["pyoo"],
                                c["parameter"],
                                a["portamento"])
                    else:
                        setattr(self.controls[m['parameter']]["pyoo"],
                                c["parameter"],
                                c["value"])
            else:
                self.controls[m['parameter']]["midictl"] = Midictl(ctlnumber=m['ctrl'],
                                                                   minscale=m['min'],
                                                                   maxscale=m['max'],
                                                                   init=m['start'],
                                                                   channel=1)
                self.controls[m['parameter']]["portamento"] = Port(self.controls[m['parameter']]["midictl"]).out(m["channel"])
        print(self.controls)
        print(self.controls.keys())

        
    def restore_midi_ctl(self,parameters=[]):
        for m in self.mappings:
            if "pyoo" in m.keys():
                if m["parameter"] not in [".".join(p.split(".")[:-1]) for p in parameters] or not parameters:
                    continue
                
                if m["pyoo"] not in globals():
                    raise Exception("Pyo object " + m["pyoo"] + " does not exist")
                for c in m["controls"]:
                    if 'ctrl' in c:
                        if c["parameter"] not in [p.split(".")[-1] for p in parameters]:
                            continue
                        a = self.controls[m['parameter']]["ctrls"][c["parameter"]]
                        setattr(self.controls[m['parameter']]["pyoo"],
                                c["parameter"],
                                a["portamento"])
                        print(f"set {c} with a['midictl']")
                        self.controls[m['parameter']]["ctrls"][c["parameter"]]["portamento"].setInput(a["midictl"])
                        
            else:
                if m["parameter"] not in parameters or not parameters:
                    continue
                self.controls[m['parameter']]["portamento"].setInput(self.controls[m['parameter']]["midictl"])
        print(self.controls)
                
    def load_parameters(self, values_path=None):
        if values_path is not None:
            with open(values_path) as f:
                self.values = json.load(f)
        else:
            if self.values is None:
                raise Exception("No values defined")
        for module in self.values.keys():
            module_params = self.values[module]
            for param in module_params.keys():
                value = module_params[param]
                print(f"set {param} with {value}") 
                if type(value) == dict:
                    for pyoo_param in value.keys():
                        self.controls[module + "." + param]["ctrls"][pyoo_param]["value"] = Sig(value[pyoo_param])
                        self.controls[module + "." + param]["ctrls"][pyoo_param]["portamento"].setInput(
                            self.controls[module + "." + param]["ctrls"][pyoo_param]["value"])
                else:
                    self.controls[module + "." + param]["value"] = Sig(value)
                    # portamento = self.controls[f"{module}.{param}"]["portamento"]
                    # value_mod = 
                    # portamento.set
                    if "portamento" not in self.controls[f"{module}.{param}"].keys():
                        print("Cannot set param {param} on {module}")
                    else:
                        self.controls[f"{module}.{param}"]["portamento"].setInput(self.controls[f"{module}.{param}"]["value"],fadetime=self.fadetime)

    def export_values(self):
        modules_parameters = dict()
        for m in self.mappings:
            p = m["parameter"]
            module = p.split('.')[0]
            param = p.split('.')[1]
            if "channel" in m.keys():
                if "note" in m.keys():
                    print(str(m["note"]) + ":" + str(note_events[m["note"]]["portamento"].get()))
                else:
                    if module not in modules_parameters.keys():
                        modules_parameters[module] = dict()
                    if "controls" in m.keys():
                        modules_parameters[module][param] = dict()
                        for c in m["controls"]:
                            v = getattr(self.controls[p]["pyoo"], c["parameter"])
                            if type(v) == float:
                                modules_parameters[module][param][c["parameter"]] = v
                            else:
                                modules_parameters[module][param][c["parameter"]] = v.get()
                    else:
                        modules_parameters[module][param] = self.controls[p]["portamento"].get()

        lines = []
        for module in modules_parameters.keys():
            line = dict()
            for parameter in modules_parameters[module].keys():
                line[parameter] = modules_parameters[module][parameter]
            line["module"] = module
            lines.append(line)
#        params_df = pd.DataFrame(lines)
#        now = datetime.now()  # current date and time
#        params_df.to_csv("params" + now.strftime("%Y%m%d%H%M") + ".csv")
        return modules_parameters

    def save_parameters(self):
        now = datetime.datetime.now()  # current date and time
        with open("params" + now.strftime("%Y%m%d%H%M") + ".json", 'w') as f:
            json.dump(self.export_values(), f)

    def load_latest_paramters():
        self.load_parameters(glob.glob("params*.json")[-1])

        
    def print_parameters(self):
        vals = json.dumps(self.export_values(),indent=4,sort_keys=True)
        nb_lines = len(vals.split("\n"))

        for l in range(nb_lines):
            print("delete")
            _delete_last_line()
        print(vals, end="\r")

    def edit_range_min(self,param,value):
        param_dec = param.split(".")
        if len(param_dec) == 2:
            self.controls[param]["midictl"].setMinScale(value)
        else:
            self.controls[".".join(param_dec[:-1])]["ctrls"][param_dec[-1]]["midictl"].setMinScale(value)

    def edit_range_max(self,param,value):
        param_dec = param.split(".")
        if len(param_dec) == 2:
            self.controls[m['parameter']]["midictl"].setMaxScale(value)
        else:
            self.controls[".".join(param_dec[:-1])]["ctrls"][param_dec[-1]]["midictl"].setMaxScale(value)
                               
        
def _delete_last_line():
    sys.stdout.write('\b\b\r')
    sys.stdout.write(' ' * shutil.get_terminal_size((80, 20)).columns)
    sys.stdout.write('\b\r')
    sys.stdout.flush()
