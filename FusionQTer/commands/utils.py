from .. import config
from ..apper import apper


# Send Updated mass to the QT App
def send_mass_message():
    ao = apper.AppObjects()
    props = ao.design.rootComponent.getPhysicalProperties()
    config.conn.send({'type': 'MASS', 'mass': props.mass})


# Send Parameters to the QT App
def send_parameters_message():
    parameter_list = get_parameters()
    config.conn.send({'type': 'PARAMETERS', 'parameters': parameter_list})


def get_parameters():
    ao = apper.AppObjects()
    um = ao.f_units_manager
    units = um.defaultLengthUnits
    user_parameters = ao.design.userParameters

    parameter_list = []
    for parameter in user_parameters:
        parameter_list.append({
            'name': parameter.name,
            'value': um.formatInternalValue(parameter.value, units, False)
        })

    return parameter_list


def change_parameters(new_parameters: dict):
    ao = apper.AppObjects()
    um = ao.f_units_manager
    units = um.defaultLengthUnits

    for new_parameter in new_parameters:
        current_parameter = ao.design.userParameters.itemByName(new_parameter['name'])
        if current_parameter is not None:

            new_value_str = new_parameter.get('value')
            if isinstance(new_value_str, str):
                if um.isValidExpression(new_value_str, units):
                    new_value = um.evaluateExpression(new_value_str, units)
                    if current_parameter.value != new_value:
                        current_parameter.value = new_value
