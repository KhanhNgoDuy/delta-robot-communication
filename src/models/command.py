from .i_command import ICommand
from ..models.properties import IProperty, FrameHeaderProperty, DefaultParam, ISetValuableProperty
from ..utils.exceptions import ChangeNonChangaleProperty
from copy import deepcopy


class Command(ICommand):
    NUM_PARAMS = 6

    def __init__(self, address_property:IProperty=None, params=[DefaultParam() for _ in range(NUM_PARAMS)]):
        self._header_frame = FrameHeaderProperty()
        self._address_property = address_property
        self._params = params

    def set_function(self, function:int) -> None:
        self._address_property.set_value(int(function)) 

    def get_function(self) -> object:
        if self._address_property is None:
            return 6
        else:
            return self._address_property.get_value()

    def _get_params_to_hex(self):
        return b''.join([param.to_hex() for param in self._params])

    def to_hex(self) -> bytearray:
        if self._address_property is None:
            address = b'\x00\x06'
        else:
            address = self._address_property.to_hex()

        return self._header_frame.to_hex() + address + self._get_params_to_hex()

    def set_param_value(self, param_index:int, param_value:object) -> None:
        if self._params[param_index].changable:
            self._params[param_index].set_value(param_value)
        else:
            raise ChangeNonChangaleProperty("You cannot change the value of an non-changable property")

    def check_param_changable(self, param_index:int) -> bool:
        return self._params[param_index].changable

    def set_param(self, param_index:int, param:ISetValuableProperty) -> None:
        self._params[param_index] = param
