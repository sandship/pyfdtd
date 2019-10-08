import numpy as np
from scipy.ndimage.interpolation import shift
# FIX: in update_field, cannot use 'np.roll', because roll method does not support 3d-array, maybe. 
class Field(object):
    """[summary]
    
    Arguments:
        object {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    def __init__(self, InitializedParameter):
        self.time = 0.0
        self.step = 0
        self.param = InitializedParameter

        self.set_parameter = self.param.set_parameter
        self.general_parameter = self.param.general_parameter

        self.Xaxis = self.init_field()
        self.Yaxis = self.init_field()
        self.Zaxis = self.init_field()

        return None

    def init_field(self):
        return np.zeros(shape=(self.param.model_size["x"] + 1, self.param.model_size["y"] + 1, self.param.model_size["z"] + 1))

    def load_field(self):
        return None

    def calc_norm(self):
        self.norm = np.sqrt(
            self.Xaxis ** 2 +
            self.Yaxis ** 2 +
            self.Zaxis ** 2
        )
        return None

    def calc_phase(self):
        self.phase = 0
        return None


class Efield(Field):
    """[summary]
    
    Arguments:
        Field {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    def __init__(self, InitializedParameter):
        super().__init__(InitializedParameter)
        return None

    def update_field(self, Hfield):
        self.Xaxis[25, 25, 25] = np.sin(2.0 * 3.14159265 * self.param.freq * self.time)
        self.time = Hfield.time + self.param.dt /2.0
        self.step = Hfield.step + 1/2

        self.Xaxis += self.param.ce * (
                        (Hfield.Zaxis - shift(Hfield.Zaxis, shift=(0, 1, 0))) - 
                        (Hfield.Yaxis - shift(Hfield.Yaxis, shift=(0, 0, 1)))
                    )

        self.Yaxis += self.param.ce * (
                        (Hfield.Xaxis - shift(Hfield.Xaxis, shift=(0, 0, 1))) - 
                        (Hfield.Zaxis - shift(Hfield.Zaxis, shift=(1, 0, 0)))
                    )

        self.Zaxis += self.param.ce * (
                        (Hfield.Yaxis - shift(Hfield.Yaxis, shift=(1, 0, 0))) - 
                        (Hfield.Xaxis - shift(Hfield.Xaxis, shift=(0, 1, 0)))
                    )

        print(self.Xaxis[25, 25, 25], self.Yaxis[25, 25, 25], self.Zaxis[25, 25, 25])

        return None

    def calc_scatterfield(self):
        return None

    def calc_totalfield(self):
        return None

class Hfield(Field):
    """[summary]
    
    Arguments:
        Field {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    def __init__(self, InitializedParameter):
        super().__init__(InitializedParameter)
        return None

    def update_field(self, Efield):
        Efield.Xaxis[25, 25, 25] = np.sin(2.0 * 3.14159265 * self.param.freq * self.time)
        self.time = Efield.time + self.param.dt /2.0

        self.Xaxis += self.param.ch * (
                        (Efield.Zaxis - shift(Efield.Zaxis, shift=(0, -1, 0))) - 
                        (Efield.Yaxis - shift(Efield.Yaxis, shift=(0, 0, -1)))
                    )

        self.Yaxis += self.param.ch * (
                        (Efield.Xaxis - shift(Efield.Xaxis, shift=(0, 0, -1))) - 
                        (Efield.Zaxis - shift(Efield.Zaxis, shift=(-1, 0, 0)))
                    )

        self.Zaxis += self.param.ch * (
                        (Efield.Yaxis - shift(Efield.Yaxis, shift=(-1, 0, 0))) - 
                        (Efield.Xaxis - shift(Efield.Xaxis, shift=(0, -1, 0)))
                    )


        return None