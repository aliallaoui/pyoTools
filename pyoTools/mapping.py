from pyo import *
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
                self.controls[m['parameter']]["midictl"] = Midictl(ctlnumber=m['ctrl'],
                                                                   minscale=m['min'],
                                                                   maxscale=m['max'],
                                                                   init=m['start'],
                                                                   channel=1)
                self.controls[m['parameter']]["portamento"] = Port(self.controls[m['parameter']]["midictl"]).out(m["channel"])

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
                if type(value) == dict:
                    for pyoo_param in value.keys():
                        self.controls[module + "." + param]["ctrls"][pyoo_param]["value"] = Sig(value[pyoo_param])
                        self.controls[module + "." + param]["ctrls"][pyoo_param]["portamento"].setInput(
                            self.controls[module + "." + param]["ctrls"][pyoo_param]["value"])

                else:
                    self.controls[module + "." + param]["value"] = Sig(value)
                    self.controls[module + "." + param]["portamento"].setInput(controls[module + "." + param]["value"])

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
                            v = getattr(controls[p]["pyoo"], c["parameter"])
                            modules_parameters[module][param][c["parameter"]] = v.get()
                    else:
                        modules_parameters[module][param] = controls[p]["portamento"].get()

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
