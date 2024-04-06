from json_reader.decoder import iter_loads

example1 = """
{
  "a": 3,
  "b": 3.14,
  "c": {
    "d": [
      "x",
      "hello",
      3.14,
      4,
      true,
      false
    ],
    "key": {
      "key words": {
        "g": "abc"
      }
    }
  },
  "aa": NaN,
  "bb": Infinity,
  "cc": -Infinity
}
""".strip()
example2 = example1 + "extra text 1234 {} []"

example3 = r"""
{
  "a": 3,
  "b": 3.14,
  "c": {
    "d": [
      "x",
      "hello",
      3.14,
      4,
      True,
      False
    ],
    "key": {
      "key words": {
        "g": "abc"
      }
    }
  },
  "aa": nan,
  "bb": infinity,
  "cc": -infinity,
  "dd": "string1",
  "dd": 'string2',
  "ee": 'str\\'ing3'
}
""".strip()
example4 = example3 + "extra text 1234 {} []"

example5 = "any head" + example2 + example4 + "{"


def test_scanner_standard():
    from json_reader.decoder import JSONDecoder

    decoder = JSONDecoder()
    data, index = decoder.raw_decode(example2)
    print(data, example2[index:])


def test_scanner_changed():
    from json_reader.decoder import JSONDecoder
    from json_reader.decoder_node_py import NodePyCompatibleScanner

    decoder = JSONDecoder(scanner_cls=NodePyCompatibleScanner)
    data, index = decoder.raw_decode(example4)
    print(data, example4[index:])


def test_iter_loads():
    from json_reader.decoder import JSONDecoder
    from json_reader.decoder_node_py import NodePyCompatibleScanner

    decoder = JSONDecoder(scanner_cls=NodePyCompatibleScanner)
    for data, left in iter_loads(example5, decoder=decoder):
        print(data)
