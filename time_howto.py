import itertools
import pandas as pd
import math

nums = [[4, 5], [6, 7], [11]]
flat_nums = list(itertools.chain.from_iterable(nums))
print(flat_nums)  # prints [4, 5, 6, 7, 11]
# find most frequest number in list

nums = [3, 4, 20, 2, 31]

zeros = [0]*100

print(zeros)
