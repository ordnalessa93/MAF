import sys
import json
import glob
from pathlib import Path

def extract_int(fullstring):
    _, v = fullstring[:-5].rsplit('-', 1)
    return int(v)

file_part = sys.argv[1]

values = {extract_int(fname): json.loads(Path(fname).read_text()) for fname in glob.iglob(f'test-results-{file_part}-*.json')}
print(file_part.rsplit('-', 1)[0], 'MAF time', 'IMAF time', sep=', ')
for key in sorted(values):
    v = values[key]
    print(key, v['MAF']['time_elapsed'], v['IMAF']['time_elapsed'], sep=', ')
