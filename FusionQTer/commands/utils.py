from ..apper import apper


# Send Updated mass to the QT App
def get_mass_message():
    ao = apper.AppObjects()
    props = ao.design.rootComponent.getPhysicalProperties()
    msg = {'mass': props.mass}
    return msg

