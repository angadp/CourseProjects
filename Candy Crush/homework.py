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

def CalculateTimeForMove(array, time):
	calarray = copy.deepcopy(array)
	n = len(array)
	num_child = 0
	strt = datetime.now()
	for i in range(n):
		for j in range(n):
			if (calarray[i][j] <= 9 and calarray[i][j] >= 0):
				flooding(i, j, calarray)
				num_child += 1
	tim_node_generation = (datetime.now() - strt).total_seconds()
	if(tim_node_generation < 0.001):
		tim_node_generation = 0.001
	time_for_move = ((time/num_child) *2) + time/10
	level = 1
	print(num_child)
	if(num_child > 3):
		num_child /= 2
		while((tim_node_generation * num_child)<time_for_move):
			level+=1
			tim_node_generation *= num_child
		print(tim_node_generation)
		return level
	else:
		return 3

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
					fun_v, hun_i, hun_j = CalculateDP(temp, not(maxi), level - 1, lvlscore - (key*key), alpha, beta)
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
p = int(f.readline())
time = float(f.readline())
array = [[0]*n for i in range(n)]
for i in range(n):
	inp = f.readline()
	inpl = list(inp)
	for j in range(n):
		if(inpl[j]!='*'):
			array[i][j] = int(inpl[j])
		else:
			array[i][j] = -1
level = CalculateTimeForMove(array, time)
print(level)
fh, val_i, val_j = CalculateDP(array, True, level, 0, INT_MIN, INT_MAX)
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
print(li)
print(datetime.now() - start_time)