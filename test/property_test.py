import unittest 
from src.models.properties import Property
from unittest.mock import Mock
from src.views import IObserver


class PropertyTest(unittest.TestCase):
    def test_to_hex_with_value_is_6(self):
        new_value = 6
        expected_result = b'\x00\x06'

        address_property = Property() 
        address_property.set_value(new_value)

        result = address_property.to_hex()

        assert result == expected_result


    def test_to_hex_with_value_is_226(self):
        new_value = 326
        expected_result = b'\x01\x46'

        address_property = Property() 
        address_property.set_value(new_value)

        result = address_property.to_hex()

        assert result == expected_result

    def test_to_hex_with_value_is_326_4_bytes_capacity(self):
        new_value = 326
        num_bytes = 4 
        expected_result = b'\x00\x00\x01\x46'

        test_param = Property(num_bytes=num_bytes)
        test_param.set_value(new_value)

        result = test_param.to_hex()

        assert result == expected_result

    def test_call_one_observer_each_time_the_value_is_changed(self):
        new_value = 4
        observer = Mock(spec=IObserver)
        test_property = Property()
        test_property.add_observer(observer)

        test_property.set_value(new_value)

        observer.update.assert_called_once_with(test_property)

    def test_multiple_observers(self):
        new_value = 4
        observer_1 = Mock(spec=IObserver)
        observer_2 = Mock(spec=IObserver)
        observer_3 = Mock(spec=IObserver)
        test_property = Property()
        test_property.add_observer(observer_1)
        test_property.add_observer(observer_2)
        test_property.add_observer(observer_3)

        test_property.set_value(new_value)

        observer_1.update.assert_called_once_with(test_property)
        observer_2.update.assert_called_once_with(test_property)
        observer_3.update.assert_called_once_with(test_property)

    def test_remove_observer_function(self):
        new_value = 4
        observer_1 = Mock(spec=IObserver)
        observer_2 = Mock(spec=IObserver)
        observer_3 = Mock(spec=IObserver)
        test_property = Property()
        test_property.add_observer(observer_1)
        test_property.add_observer(observer_2)
        test_property.add_observer(observer_3)

        test_property.remove_observer(observer_2)
        test_property.set_value(new_value)

        observer_1.update.assert_called_once_with(test_property)
        observer_2.update.assert_not_called()
        observer_3.update.assert_called_once_with(test_property)
