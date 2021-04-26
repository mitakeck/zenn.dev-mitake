#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pandocfilters import toJSONFilter, walk, Para, Image, get_caption
import base64
import json

def quickchart(key, value, format, _):
    if key != 'CodeBlock':
        return # skip

    [[ident, classes, keyvals], code] = value

    if not("chart" in classes):
        return # skip

    caption, typef, keyvals = get_caption(keyvals)

    code = json.loads(code)
    code = json.dumps(code, separators=(',', ':'))

    dest = "https://quickchart.io/chart?c=" + code

    return Para([Image([ident, [], keyvals], caption, [dest, typef])])

if __name__ == "__main__":
    toJSONFilter(quickchart)
