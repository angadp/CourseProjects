from __future__ import print_function
from collections import defaultdict
import copy
from datetime import datetime

INT_MIN = -500000
INT_MAX = 500000

stackx = []
stacky = []

def flooding(x, y, array):
	score = 0
	stackx.append(x)
	stacky.append(y)
	match = array[x][y]
	while(len(stackx)):
		x_val = stackx.pop(0)
		y_val = stacky.pop(0)
		if(array[x_val][y_val] == match):
			score+=1
			array[x_val][y_val] = -1
			if(x_val - 1 >= 0):
				stackx.append(x_val-1)
				stacky.append(y_val)
			if(x_val+1 <len(array)):
				stackx.append(x_val+1)
				stacky.append(y_val)
			if(y_val-1 >= 0):
				stackx.append(x_val)
				stacky.append(y_val-1)
			if(y_val+1 < len(array)):
				stackx.append(x_val)
				stacky.append(y_val+1)
	return score

def gravity(array):
	n = len(array)
	for i in range(n):
		change = 0
		for j in range(n-1, -1, -1):
			if(array[j][i] != -1):
				array[j+change][i] = array[j][i]
			else:
				change += 1
		for j in range(change - 1, -1, -1):
			array[j][i] = -1

def CalculateLevels(array, time):
	if(time < 10):
		return 1
	calarray = copy.deepcopy(array)
	n = len(array)
	num_child = 0
	for i in range(n):
		for j in range(n):
			if (calarray[i][j] <= 9 and calarray[i][j] >= 0):
				flooding(i, j, calarray)
				num_child += 1
	time_for_move = time/num_child

def CalculateDP(array, maxi, level, lvlscore, alpha, beta):
	if(level == 0):
		return lvlscore, -1, -1
	dic = defaultdict(list)
	n = len(array)
	lvlarray = copy.deepcopy(array)
	for i in range(n):
		for j in range(n):
			if(lvlarray[i][j]<=9 and lvlarray[i][j]>=0):
				val = flooding(i, j, lvlarray)
				dic[val].append([i, j])
	if(level == 3):
		print(len(dic))
	if(len(dic)):
		if(maxi):
			v = INT_MIN
			val_i = 0
			val_j = 0
			sorted_dic = sorted(dic.keys(), reverse = True)
			for key in sorted_dic:
				for value in dic[key]:
					temp = copy.deepcopy(array)
					ji = flooding(value[0], value[1], temp)
					gravity(temp)
					score_to_add = key*key
					fun_v, hun_i, hun_j = CalculateDP(temp, not(maxi), level - 1, lvlscore + score_to_add, alpha, beta)
					if(v < fun_v):
						v = fun_v
						val_i = value[0]
						val_j = value[1]
					if(v >= beta):
						return v, val_i, val_j
					alpha = max(alpha, v)
			return v, val_i, val_j
		else:
			v = INT_MAX
			val_i = 0
			val_j = 0
			sorted_dic = sorted(dic.keys(), reverse = True)
			for key in sorted_dic:
				for value in dic[key]:
					temp = copy.deepcopy(array)
					ji = flooding(value[0], value[1], temp)
					gravity(temp)
					fun_v, hun_i, hun_j = CalculateDP(temp, not(maxi), level - 1, lvlscore, alpha, beta)
					if(v > fun_v):
						v = fun_v
						val_i = value[0]
						val_j = value[1]
					if(v <= alpha):
						return v, val_i, val_j
					beta = min(beta, v)
			return v, val_i, val_j
	else:
		return lvlscore, -1, -1

start_time = datetime.now()
f = open("input.txt", "r")
n = int(f.readline())
print(n)
p = int(f.readline())
time = float(f.readline())
print(time)
array = [[0]*n for i in range(n)]
for i in range(n):
	inp = f.readline()
	inpl = list(inp)
	for j in range(n):
		print(inpl[j], end='')
		if(inpl[j]!='*'):
			array[i][j] = int(inpl[j])
		else:
			array[i][j] = -1
	print('')
if(n < 13):
	if(time < 10):
		fh, val_i, val_j = CalculateDP(array, True, 1, 0, INT_MIN, INT_MAX)
	elif(time < 30):
		fh, val_i, val_j = CalculateDP(array, True, 3, 0, INT_MIN, INT_MAX)
	else:
		fh, val_i, val_j = CalculateDP(array, True, 5, 0, INT_MIN, INT_MAX)
if(n < 19):
	if(time < 10):
		fh, val_i, val_j = CalculateDP(array, True, 1, 0, INT_MIN, INT_MAX)
	elif(time < 0):
		fh, val_i, val_j = CalculateDP(array, True, 3, 0, INT_MIN, INT_MAX)
	else:
		fh, val_i, val_j = CalculateDP(array, True, 5, 0, INT_MIN, INT_MAX)
else:
	if(time < 10):
		fh, val_i, val_j = CalculateDP(array, True, 1, 0, INT_MIN, INT_MAX)
	else:
		fh, val_i, val_j = CalculateDP(array, True, 3, 0, INT_MIN, INT_MAX)
fw = open("output.txt", "w")
fw.write(chr(val_j+65))
fw.write(str(val_i+1))
fw.write("\n")
li = flooding(val_i, val_j, array)
gravity(array)
for i in range(n):
	for j in range(n):
		if(array[i][j] == -1):
			fw.write("*")
		else:
			fw.write(str(array[i][j]))
	fw.write("\n")
print(datetime.now() - start_time)
print(li)