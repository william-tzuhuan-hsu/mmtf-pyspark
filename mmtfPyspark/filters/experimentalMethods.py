#!/user/bin/env python
'''
experimentalMethods.py:

This filter returns ture if all the specified experimental methods
match a PDB entry

The current list of support experimental method types can be found here:
<a href="http://mmcif.wwpdb.org/dictionaries/mmcif_pdbx_v40.dic/Items/_exptl.method.html">here</a>

Authorship information:
    __author__ = "Mars Huang"
    __maintainer__ = "Mars Huang"
    __email__ = "marshuang80@gmail.com:
    __status__ = "Done"
'''

class experimentalMethods(object):
    '''
    Attributes:
        experimental_methods (list(string)): A list of experimental methods to check
    '''
    # constants to be used as arguments to the Experimental Methods filter
    ELECTRON_CRYSTALLOGRAPHY = "ELECTRON CRYSTALLOGRAPHY"
    ELECTRON_MICROSCOPY = "ELECTRON MICROSCOPY"
    ERP = "EPR"
    FIBER_DIFFRACTION = "FIBER DIFFRACTION"
    FLUORESCENCE_TRANSFER = "FLUORESCENCE TRANSFER"
    INFRARED_SPECTROSCOPY = "INFRARED SPECTROSCOPY"
    NEUTRON_DIFFRACTION = "NEUTRON DIFFRACTION"
    POWDER_DIFFRACTION = "POWDER DIFFRACTION"
    SOLID_STATE_NMR = "SOLID-STATE NMR"
    SOLUTION_NMR = "SOLUTION NMR"
    SOLUTION_SCATTERING = "SOLUTION SCATTERING"
    THEORETICAL_MODEL = "THEORETICAL MODEL"
    X_RAY_DIFFRACTION = "X-RAY DIFFRACTION"

    def __init__(self, *experimentalMethods):
        self.experimental_methods = sorted(list(experimentalMethods))


    def __call__(self, t):
        structure = t[1]
        if len(structure.experimental_methods) != len(self.experimental_methods):
            return False

        methods = sorted([b.decode().upper()
                          for b in structure.experimental_methods])
        return methods == self.experimental_methods