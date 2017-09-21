import json


def decode_json(fn):
    def _decode_json_from_payload(payload):
        json_payload = json.loads(payload['body'])
        return fn(json_payload)
    return _decode_json_from_payload


def to_pretty_dict(d):
    pretty = {}
    #import pdb; pdb.set_trace()
    for k, v in d.items():
        if hasattr(v, 'keys'):
            v = dict(v)
        pretty[k] = v

    return pretty


def prettify_schematics_errors(e):
    errors = {}
    for k, v in e.errors.items():
        if hasattr(v, 'keys'):
            errors[k] = to_pretty_dict(v)
        else:
            errors[k] = [str(e) for e in v]
    return errors
