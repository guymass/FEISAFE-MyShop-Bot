import re
import json
from json.scanner import NUMBER_RE


class PyJSONScanner:
    def __init__(self, context):
        """
        same as json.scanner.py_make_scanner, but convert to a class
        """
        self.parse_object = context.parse_object
        self.parse_array = context.parse_array
        self.parse_string = context.parse_string
        self.match_number = NUMBER_RE.match
        self.strict = context.strict
        self.parse_float = context.parse_float
        self.parse_int = context.parse_int
        self.parse_constant = context.parse_constant
        self.object_hook = context.object_hook
        self.object_pairs_hook = context.object_pairs_hook
        self.memo = context.memo

    def _scan_once(self, string, idx):
        try:
            nextchar = string[idx]
        except IndexError:
            raise StopIteration(idx)

        if self.is_str(nextchar):
            return self.parse_string(string, idx + 1, self.strict)
        elif nextchar == '{':
            return self.parse_object(
                (string, idx + 1),
                self.strict,
                self._scan_once,
                self.object_hook,
                self.object_pairs_hook,
                self.memo,
            )
        elif nextchar == '[':
            return self.parse_array((string, idx + 1), self._scan_once)
        elif self.is_null(nextchar, string[idx : idx + 4]):
            return None, idx + 4
        elif self.is_true(nextchar, string[idx : idx + 4]):
            return True, idx + 4
        elif self.is_false(nextchar, string[idx : idx + 5]):
            return False, idx + 5

        m = self.match_number(string, idx)
        if m is not None:
            integer, frac, exp = m.groups()
            if frac or exp:
                res = self.parse_float(integer + (frac or '') + (exp or ''))
            else:
                res = self.parse_int(integer)
            return res, m.end()
        elif self.is_nan(nextchar, string[idx : idx + 3]):
            return self.parse_constant('NaN'), idx + 3
        elif self.is_infinity(nextchar, string[idx : idx + 8]):
            return self.parse_constant('Infinity'), idx + 8
        elif self.is_negative_infinity(nextchar, string[idx : idx + 9]):
            return self.parse_constant('-Infinity'), idx + 9
        elif self.is_infinity(nextchar, string[idx : idx + 3]):
            return self.parse_constant('Infinity'), idx + 3
        elif self.is_negative_infinity(nextchar, string[idx : idx + 4]):
            return self.parse_constant('-Infinity'), idx + 4
        else:
            raise StopIteration(idx)

    def scan_once(self, string, idx):
        string = self.pre_process(string)
        try:
            return self._scan_once(string, idx)
        finally:
            self.memo.clear()

    def pre_process(self, string):
        return string

    def is_str(self, nextchar):
        return nextchar == '"'

    def is_null(self, nextchar, text):
        return nextchar == 'n' and text == 'null'

    def is_true(self, nextchar, text):
        return nextchar == 't' and text == 'true'

    def is_false(self, nextchar, text):
        return nextchar == 'f' and text == 'false'

    def is_nan(self, nextchar, text):
        return nextchar == 'N' and text == 'NaN'

    def is_infinity(self, nextchar, text):
        return nextchar == 'I' and text == 'Infinity'

    def is_negative_infinity(self, nextchar, text):
        return nextchar == '-' and text == '-Infinity'


class JSONDecoder(json.JSONDecoder):
    def __init__(
        self,
        *,
        object_hook=None,
        parse_float=None,
        parse_int=None,
        parse_constant=None,
        strict=True,
        object_pairs_hook=None,
        scanner_cls=None,
    ):
        self.scanner_cls = scanner_cls or PyJSONScanner
        super().__init__(
            object_hook=object_hook,
            parse_float=parse_float,
            parse_int=parse_int,
            parse_constant=parse_constant,
            strict=strict,
            object_pairs_hook=object_pairs_hook,
        )

        self.patch_scan_once()

    def patch_scan_once(self):
        self.scan_once = self.scanner_cls(self).scan_once


def iter_loads(text, decoder=None):
    decoder = decoder or JSONDecoder()
    while len(text):
        if text[0] not in ['[', '{']:
            if '[' in text and '{' in text:
                idx1 = text.index('[')
                idx2 = text.index('{')
                idx = min(idx1, idx2)
            elif '[' in text:
                idx = text.index('[')
            elif '{' in text:
                idx = text.index('{')
            else:
                return
            text = text[idx:]
        try:
            data, idx = decoder.raw_decode(text)
        except json.decoder.JSONDecodeError:
            return
        else:
            text = text[idx:]
            yield data, text
