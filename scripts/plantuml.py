#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pandocfilters import toJSONFilter, Para, Image, get_caption

from zlib import compress
import base64
import six
import string

from six.moves.urllib.parse import urlencode
if six.PY2:
    from string import maketrans
else:
    maketrans = bytes.maketrans

plantuml_alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'
base64_alphabet   = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
b64_to_plantuml = maketrans(base64_alphabet.encode('utf-8'), plantuml_alphabet.encode('utf-8'))

def deflate_and_encode(plantuml_text):
    """zlib compress the plantuml text and encode it for the plantuml server.
    """
    zlibbed_str = compress(plantuml_text.encode('utf-8'))
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode(compressed_string).translate(b64_to_plantuml).decode('utf-8')

def plantuml(key, value, format, _):
    if key != 'CodeBlock':
        return # skip

    [[ident, classes, keyvals], code] = value

    if not("plantuml" in classes):
        return # skip

    # convert planutml to encoded string
    caption, typef, keyvals = get_caption(keyvals)
    if not code.startswith("@start"):
        code = "@startuml\n" + code + "\n@enduml\n"
    compressed = deflate_and_encode(code)

    # concat
    dest = "https://www.plantuml.com/plantuml/png/" + compressed

    return Para([Image([ident, [], keyvals], caption, [dest, typef])])

if __name__ == "__main__":
    toJSONFilter(plantuml)
