def prettify_schematics_errors(e):
    errors = {}
    for k, v in e.value.errors.items():
        if hasattr(v, 'keys'):
            errors[k] = v
        else:
            errors[k] = [str(e) for e in v]
    return errors
