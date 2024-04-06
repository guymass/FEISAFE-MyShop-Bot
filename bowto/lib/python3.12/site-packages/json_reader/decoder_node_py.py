import re
from json_reader.decoder import PyJSONScanner


class NodePyCompatibleScanner(PyJSONScanner):
    def normalize(self, nextchar, text):
        nextchar = nextchar.lower()
        text = text.lower()
        return nextchar, text

    def pre_process(self, string):
        str_ex = re.compile(r"""(?<!\\)'(?P<value>.*?)(?<!\\)'""", re.S)
        rv = str_ex.sub(r'"\g<value>"', string)
        return rv

    def is_null(self, nextchar, text):
        nextchar, text = self.normalize(nextchar, text)
        return nextchar == 'n' and text == 'null'

    def is_true(self, nextchar, text):
        nextchar, text = self.normalize(nextchar, text)
        return nextchar == 't' and text == 'true'

    def is_false(self, nextchar, text):
        nextchar, text = self.normalize(nextchar, text)
        return nextchar == 'f' and text == 'false'

    def is_nan(self, nextchar, text):
        nextchar, text = self.normalize(nextchar, text)
        return nextchar == 'n' and text == 'nan'

    def is_infinity(self, nextchar, text):
        nextchar, text = self.normalize(nextchar, text)
        return nextchar == 'i' and text in ['infinity', 'inf']

    def is_negative_infinity(self, nextchar, text):
        nextchar, text = self.normalize(nextchar, text)
        return nextchar == '-' and text in ['-infinity', '-inf']
