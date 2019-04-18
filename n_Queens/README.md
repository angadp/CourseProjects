To run, use the following command - 

g++ n_Queens.cpp

The input file format is as follows:

First line the method:
1)DFS
2)BFS
3)SA

Second line Number of colums. Third the number of queens.
The rest are the configuration of the board. You can also place an obstacle using 2.

Example
BFS 
10
11
002000000000
000020000000
000000200000
200000000000
000000000000
000000200000
000000000000
000000000000
002000000000
000000000000
222222222222
002000000002

SA stands for Simulated Annealing. It uses energy function to guess which direction to go to next.

Assignment handout https://github.com/angadp/CourseProjects/blob/master/n_Queens/hw1-csci561-f17.pdf
