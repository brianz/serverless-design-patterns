import json

from schematics.exceptions import (
        ConversionError,
        DataError,
)


def decode_json(fn):
    def _decode_json_from_payload(payload):
        json_payload = json.loads(payload['body'])
        return fn(json_payload)
    return _decode_json_from_payload


def to_pretty_dict(d):
    pretty = {}
    for k, v in d.items():
        if hasattr(v, 'keys'):
            v = to_pretty_dict(v)
        elif isinstance(v, ConversionError):
            v = ' '.join([str(i) for i in v])
        pretty[k] = v

    return pretty


def prettify_schematics_errors(e):
    # Hook for running via py.test. When exceptions are raised they wind up in the exception
    # `value` object, so we need to access them differently when running tests. Normally the first
    # access will work.
    try:
        errors = e.errors
    except AttributeError:
        errors = e.value.errors

    pretty_errors = {}
    for k, v in errors.items():
        if hasattr(v, 'keys'):
            pretty_errors[k] = to_pretty_dict(v)
        else:
            pretty_errors[k] = ' '.join([str(e) for e in v])
    return pretty_errors
