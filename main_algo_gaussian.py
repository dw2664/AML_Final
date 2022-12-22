# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import random
import math

def generate_samples_g(s):
  sample = np.random.normal(0,1,s).tolist()
  min = np.min(sample)
  max = np.max(sample)
  r = max - min
  for i in range(s):
    sample[i] = (sample[i] - min)/r
  return sample
def generate_samples_lg(s):
  sample = np.abs(np.random.normal(0,1,s)).tolist()
  min = np.min(sample)
  max = np.max(sample)
  r = max - min
  for i in range(s):
    sample[i] = float(format((sample[i] - min)/r,  '.2f'))
  return sample
def generate_samples_rg(s):
  sample = np.abs(np.random.normal(0,1,s)).tolist()
  min = np.min(sample)
  max = np.max(sample)
  r = max - min
  for i in range(s):
    sample[i] = 1- float(format((sample[i] - min)/r,  '.2f'))
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
      sample = generate_samples_rg(size)
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

# test the accuracy of the main algo in 10 iterations
result = []
for i in range(10):
  result.append(main_algo())
