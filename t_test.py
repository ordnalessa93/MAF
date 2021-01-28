import glob
import sys
import json
from pathlib import Path
from scipy import stats
import numpy as np
import os

l = []
for file_ in glob.glob('*.json'):
	l.append(json.loads(Path(file_).read_text()))

maf = [result['results']['MAF']['elapsed_time_MAF'] for results in l for result in results]
imaf = [result['results']['IMAF']['elapsed_time_IMAF'] for results in l for result in results]

print(stats.ttest_rel(maf, imaf))
print('MAF avg time: ', np.mean(maf),'e-MAF avg time: ', np.mean(imaf))

maf = [result['results']['MAF']['targets_saved'] for results in l for result in results]
imaf = [result['results']['IMAF']['targets_saved'] for results in l for result in results]

print(stats.ttest_rel(maf, imaf))
print('MAF avg score: ', np.mean(maf),'e-MAF avg score: ', np.mean(imaf))

for world in os.listdir('world-data'):
	maf = [result['results']['MAF']['targets_saved'] for results in l for result in results if result['world'] == world]
	imaf = [result['results']['IMAF']['targets_saved'] for results in l for result in results if result['world'] == world]
	print(stats.ttest_rel(maf, imaf)[1])
	print(world, 'MAF avg score: ', np.mean(maf),'e-MAF avg score: ', np.mean(imaf))
