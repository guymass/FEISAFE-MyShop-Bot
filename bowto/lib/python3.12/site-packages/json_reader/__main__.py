import sys
import json
import os
from json_reader.decoder import JSONDecoder, iter_loads
from json_reader.decoder_node_py import NodePyCompatibleScanner


def main():
    decoder = JSONDecoder(scanner_cls=NodePyCompatibleScanner)
    if os.getenv("BY_LINES"):
        texts = sys.stdin
    else:
        texts = [sys.stdin.read()]
    for text in texts:
        for data, _ in iter_loads(text, decoder=decoder):
            print(
                json.dumps(
                    data,
                    indent=int(os.getenv("JSON_INDENT", "0")) or None,
                    ensure_ascii=False,
                )
            )


if __name__ == '__main__':
    main()
