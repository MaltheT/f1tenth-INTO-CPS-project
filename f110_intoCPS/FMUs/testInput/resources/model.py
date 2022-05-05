from optparse import Values
import pickle


class Input:
    def __init__(self) -> None:
        self.a = 0.0
        self.b = 0.0 

        self.reference_to_attribute = {
            0: "a",
            1: "b",
        }

        self.references_input = [0]
        self.references_output = [1]

        self.a = self.fmi2GetReal(self.references_input)


    def fmi2DoStep(self, current_time, step_size, no_step_prior):
        self._update_outputs()
        return Fmi2Status.ok
    
    def fmi2SetupExperiment(self, start_time, stop_time, tolerance):
        return Fmi2Status.ok

    def fmi2EnterInitializationMode(self):
        return Fmi2Status.ok

    def fmi2ExitInitializationMode(self):
        return Fmi2Status.ok

    def fmi2SetupExperiment(self, start_time, stop_time, tolerance):
        return Fmi2Status.ok

    def fmi2GetReal(self, references):
        return self._get_value(references)
    
    def fmi2SetReal(self, references, values):
        return self._set_value(references, values)

    def _set_value(self, references, values):

        for r, v in zip(references, values):
            setattr(self, self.reference_to_attribute[r], v)

        return Fmi2Status.ok


    def _get_value(self, references):

        values = []

        for r in references:
            values.append(getattr(self, self.reference_to_attribute[r]))

        return values

    def fmi2Reset(self):
        return Fmi2Status.ok

    def fmi2Terminate(self):
        return Fmi2Status.ok

    def _update_outputs(self):
        output = self.a + 5
        self.b = []
        self.b.append(output)

        print(self.b)
        print(self.references_output[0])
        self.fmi2SetReal(self.references_output, self.b)
    

class Fmi2Status:
    """Represents the status of the FMU or the results of function calls.

    Values:
        * ok: all well
        * warning: an issue has arisen, but the computation can continue.
        * discard: an operation has resulted in invalid output, which must be discarded
        * error: an error has ocurred for this specific FMU instance.
        * fatal: an fatal error has ocurred which has corrupted ALL FMU instances.
        * pending: indicates that the FMu is doing work asynchronously, which can be retrived later.

    Notes:
        FMI section 2.1.3

    """

    ok = 0
    warning = 1
    discard = 2
    error = 3
    fatal = 4
    pending = 5
