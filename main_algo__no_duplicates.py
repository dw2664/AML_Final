import pandas as pd
import numpy as np
import random
import math

def generate_samples(s):
  sample = []
  for i in range(s):
    sample.append(random.randint(0, s)/s)
  return sample

#flip function
def flip(p):
  return 1 if random.random() < p else 0

def challenge(king, challenger, level, c, budget):
  if budget <= 0:
    return challenger
  s_l = int(c * math.pow(3, level))
  king_bias = np.sum([flip(king) for j in range(s_l)])
  challenger_bias = np.sum([flip(challenger) for j in range(s_l)])
  if king_bias >= challenger_bias :
    return king
  else:
    return challenge(king, challenger, level + 1, c, budget - s_l)

def main_algo():
  #the most biased coin in the sample and its id
  coin_ = 0
  id_ = 0
  gap = 0
  size = 100
  sample = [];
  while gap == 0 : 
      sample = generate_samples(size)
      coin_ = np.amax(sample)
      id_ = np.argmax(sample)
      gap = coin_ - np.partition(sample, -2)[-2]
  #confidence param
  delta = 0.1 
  b = 4 / (gap * gap) * math.log(1/delta) * (1 + 3)
  #init king and challenger
  king = sample[0]
  king_budget = 0
  c = 4 / (gap * gap) * math.log(1/delta)
  for i in range(1,len(sample)):
    king_budget += b
    challenger = sample[i]
    king = challenge(king, challenger, 1, c, king_budget)
  return int(sample.index(king) == id_)

def main_algo_gap(gap):
  #the most biased coin in the sample and its id
  coin_ = 0
  id_ = 0
  size = 100
  sample = generate_samples(size)
  coin_ = np.amax(sample)
  id_ = np.argmax(sample)
  #confidence param
  delta = 0.1 
  b = 4 / (gap * gap) * math.log(1/delta) * (1 + 3)
  #init king and challenger
  king = sample[0]
  king_budget = 0
  c = 4 / (gap * gap) * math.log(1/delta)
  for i in range(1,len(sample)):
    king_budget += b
    challenger = sample[i]
    king = challenge(king, challenger, 1, c, king_budget)
  return int(sample.index(king) == id_)

# test the accuracy of the main algo in 10 iterations
result = []
for i in range(10):
  result.append(main_algo())