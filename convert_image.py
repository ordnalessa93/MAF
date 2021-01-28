"""convert image to a text description of the walls."""

from PIL import Image
import numpy as np
import sys
from itertools import groupby
from pathlib import Path
import mimetypes


def convert(file):
    print('converting', file)
    img = Image.open(file)
    arr = np.array(img.convert('L'))
    a = np.transpose(np.nonzero(arr < 10))
    with file.with_suffix('.txt').open('w') as f:
        for k, g in groupby(a, key=lambda x: x[0]):
            print(k, ','.join(str(v[1]) for v in g), file=f)

if __name__ == '__main__':
    path = Path(sys.argv[1])
    if path.is_dir():
        for p in path.iterdir():
            t, _ = mimetypes.guess_type(str(p))
            if t is not None and t.startswith('image/'):
                convert(p)
    else:
        convert(path)
