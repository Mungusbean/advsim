import inspect

def get_params(class_object) -> dict:
    """_summary_ Gets the instanciation parameters of a class.

    Args:
        class_object (_type_): _description_ takes in a class and returns arguments/ parameters required for instanciation.
    """
    combined_params = {}
    if class_object.__bases__:
        init_parent_sig = inspect.signature(class_object.__bases__[0].__init__) # assume single inheritance so we only check the direct parent
        parent_params = list(init_parent_sig.parameters.items())
        combined_params = {name: param for name, param in parent_params if name != 'self'}
    init_child_sig = inspect.signature(class_object.__init__) 
    child_params = list(init_child_sig.parameters.items())

    combined_params.update({name: param for name, param in child_params if name != 'self'})

    # for testing
    for name, param in combined_params.items():
        print(f"{name}: {param.default if param.default != inspect.Parameter.empty else 'Required'}")

    return {key: val.default if val.default != inspect.Parameter.empty else "Required" for key, val in combined_params.items()}