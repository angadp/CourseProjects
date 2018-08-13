#include <stdio.h>
#include <stack>
#include <fstream>
#include <stdlib.h>
#include <queue>
#include <stdlib.h>
#include <iostream>
#include <cstring>
#include <ctime>
#include <math.h>

using namespace std;

stack <int> sx,sy;
struct node
{
	int queens;
	int col;
	std::vector< pair <int, int> > v;
};

queue <node> q;

void printarr(void* board1d, int n, ofstream &out)
{
	out << "OK\n";
	int (*board)[n] = (int (*)[n])board1d;
	int i, j;
	for(i=0;i<n;i++)
	{
		for(j=0;j<n;j++)
			out << board[i][j];
		out << "\n";
	}
}

bool isSafe(void* board1d, int row, int col, int n)
{
	int (*board)[n] = (int (*)[n])board1d;
	int i , j;
	if(board[row][col]!=0)
		return false;
	if((row>=n) || (row<0) || (col>=n) || (col<0))
		return false;
	for(i = col - 1; i>=0 ; i--)
	{
		if(board[row][i] == 1)
			return false;
		if(board[row][i] == 2)
			break;
	}
	// for(i = col + 1 ; i<n ; i++)
	// {
	// 	if(board[row][i] == 1)
	// 		return false;
	// 	if(board[row][i] == 2)
	// 		break;
	// }
	for(i = row - 1; i>=0 ; i--)
	{
		if(board[i][col] == 1)
			return false;
		if(board[i][col] == 2)
			break;
	}
	for(i = row + 1 ; i<n ; i++)
	{
		if(board[i][col] == 1)
			return false;
		if(board[i][col] == 2)
			break;
	}
	i = row -1, j = col - 1;
	while(i >=0 && j >=0)
	{
		if(board[i][j] == 1)
			return false;
		if(board[i][j] == 2)
			break;
		i--;
		j--;
	}
	// i = row +1, j = col + 1;
	// while(i < n && j < n)
	// {
	// 	if(board[i][j] == 1)
	// 		return false;
	// 	if(board[i][j] == 2)
	// 		break;
	// 	i++;
	// 	j++;
	// }
	i = row +1, j = col - 1;
	while(i < n && j >= 0)
	{
		if(board[i][j] == 1)
			return false;
		if(board[i][j] == 2)
			break;
		i++;
		j--;
	}
	// i = row -1, j = col + 1;
	// while(i >=0 && j < n)
	// {
	// 	if(board[i][j] == 1)
	// 		return false;
	// 	if(board[i][j] == 2)
	// 		break;
	// 	i--;
	// 	j++;
	// }
	return true;
}

int Energy(void *board1d, int n)
{
	int (* board)[n] = (int (*)[n]) board1d;
	int i,j,iteri, iterj,num_attacks = 0;
	for(i = 0; i < n ; i++)
	{
		for(j=0;j<n;j++)
		{
			if(board[i][j] == 1)
			{
				//Left
				for(iteri = i+1;iteri<n;iteri++)
				{
					if(board[iteri][j] == 1)
					{
						num_attacks++;
					}
					else if(board[iteri][j] == 2)
						break;
				}
				//Down
				for(iterj = j+1;iterj<n;iterj++)
				{
					if(board[i][iterj] == 1)
					{
						num_attacks++;
					}
					else if(board[i][iterj] == 2)
						break;
				}
				//Diagonal Down
				iteri = i + 1;
				iterj = j + 1;
				while(iteri<n && iterj < n)
				{
					if(board[iteri][iterj] == 1)
					{
						num_attacks++;
					}
					else if(board[iteri][iterj] == 2)
						break;
					iteri++;
					iterj++;
				}
				//Diagonal Up
				iteri = i - 1;
				iterj = j + 1;
				while(iteri>=0 && iterj < n)
				{
					if(board[iteri][iterj] == 1)
					{
						num_attacks++;
					}
					else if(board[iteri][iterj] == 2)
						break;
					iteri--;
					iterj++;
				}
			}
		}
	}
	return num_attacks;
}

bool probablityFunction(int deltaEnergy, float Temp, int n)
{
	if(deltaEnergy<0)
		return true;
	else
	{
		double c = exp(-deltaEnergy/Temp);
		double r = ((double) rand() / (RAND_MAX));
		if(r<c)
			return true;
		return false;
	}
}

bool placedSA(void* board1d, int n, int num_queens, ofstream &out)
{
	bool sol = false;
	clock_t start, end;
    double duration;
    time (&start);
	int (*board)[n] = (int (*)[n])board1d;
	int i=0,j=0,k =0;
	int queens = num_queens;
	int randomqueen, newxpos, newypos;
	int xpos[num_queens], ypos[num_queens],NewEnergy;
	float Temp = (float)queens, CoolingFactor = 0.98, heatingFactor = 1.2;
	bool newpos = false, cooling = true, stlllooking = true;
	while(num_queens>0)
	{
		while(board[i][j]==1 || board[i][j] == 2)
        {	
        	i++;
     		if(i>=n)
            {
				i=0;
             	j++;
            }
			if(j>=n)
				j=0;
        }
        board[i][j] = 1;
		num_queens--;
		xpos[k] = i;
		ypos[k] = j;
		k++;
		i++;
		j++;
		if(i>=n)
        {
			i=0;
         	j++;
        }
		if(j>=n)
			j=0;
	}
	int Init = Energy(board, n);
	if(Init == 0)
	{
		stlllooking = false;
		sol = true;
	}
	while(stlllooking)
	{
		randomqueen = rand()%queens;
		//random x and y position
		while(newpos == false)
		{
			newxpos = rand()%n;
			newypos = rand()%n;
			if(board[newxpos][newypos] == 0)
				newpos = true;
		}
		newpos = false;
		board[xpos[randomqueen]][ypos[randomqueen]] = 0;
		board[newxpos][newypos] = 1;
		NewEnergy = Energy(board,n);
		board[xpos[randomqueen]][ypos[randomqueen]] = 1;
		board[newxpos][newypos] = 0;
		int deltaEnergy = NewEnergy - Init;
		if(probablityFunction(deltaEnergy, Temp, queens))
		{
			board[xpos[randomqueen]][ypos[randomqueen]] = 0;
			ypos[randomqueen] = newypos;
			xpos[randomqueen] = newxpos;
			board[xpos[randomqueen]][ypos[randomqueen]] = 1;
			Init = NewEnergy;
			if(cooling == true)
				Temp = Temp * CoolingFactor;
		}
		if(cooling == false)
			Temp = Temp * heatingFactor;
		if(Init == 0)
		{
			sol = true;
			break;
		}
     	time(&end);
		if(difftime (end,start) >= 290)
        {
			stlllooking = false;
        }
		if(Temp < 0.0001)
		{
			cooling = false;
		}
		if(Temp > 5)
		{
			cooling  = true;
		}
	}
	if(sol == true)
		printarr(board, n, out);
	else
		out << "FAIL";
}

void placedBFS(void* board1d, int n, int num_queens, ofstream &out)
{
	int i=0, col = 0;
	bool found = false;
	int consti, constj;
	clock_t start, end;
    double duration;
    time (&start);
	std::vector< pair < int, int> > rocks;
	int (*board)[n] = (int (*)[n])board1d;
	int checking[n][n];
	for(consti =0; consti<n;consti++)
		for(constj = 0; constj<n;constj++)
			if(board[consti][constj] == 2)
				rocks.push_back(std::make_pair(consti, constj));
	while(true)
	{
		if(board[i][col]!=2)
		{
			struct node n1;
			n1.v.push_back(std::make_pair(i,col));
			n1.col = col;
			n1.queens = 1;
			q.push(n1);
		}
		i++;
		if(i == n)
		{
			i=0;
			col++;
		}
		if(col == n)
			break;
	}
	while(!q.empty()&&!found)
	{
		time(&end);
		if(difftime (end,start) >= 290)
        	break;
		int rockrow = 0, queenspl = 0;
		int op, column, queensplaced;
		for(op = 0; op<n ;op++)
			memset(checking, 0, n*n*sizeof(int));
		struct node invest = q.front();
		std::vector< pair <int, int> > queens = invest.v;
		column = invest.col;
		queensplaced = invest.queens;
		vector<pair <int, int> > :: iterator it;
		for(it = queens.begin();it<queens.end();it++)
			checking[it->first][it->second] = 1;
		for(it = rocks.begin();it<rocks.end();it++)
			checking[it->first][it->second] = 2;
		while(queenspl == 0 && column < n)
		{
			for(i=0;i<n;i++)
			{
				if(isSafe(checking, i, column, n))
				{
					std::vector< pair <int, int> > newqueens = queens;
					newqueens.push_back(std::make_pair(i, column));
					struct node newnode;
					newnode.col = column;
					newnode.v = newqueens;
					newnode.queens = queensplaced+1;
					q.push(newnode);
					if(queensplaced+1 == num_queens)
					{
						found = true;
						checking[i][column] = 1;
						break;
					}
					queenspl++;
				}
			}
			column++;
		}
		q.pop();
	}
	if(found == true)
		printarr(checking, n, out);
	else
		out << "FAIL";
}

bool placedDFS(void* board1d, int n, int num_queens, int *trees)
{
	int (*board)[n] = (int (*)[n])board1d;
	clock_t start, end;
    double duration;
    time (&start);
	int row = 0;
	int col = 0;
	int num_placed = 0, num_tries_to_place = 0;
	int i, j;
	bool still_looking = true, backtrack = false;
	while(col<n)
	{
		bool placed = false;
		i = row;
		j = col;
		while(!placed)
		{
			if(board[i][j]!=2)
			{
				board[i][j] = 1;
				placed = true;
				break;
			}
			i++;
			if(i == n)
			{
				col++;
				row=0;
				i=row;
				j=col;
			}
		}
		sx.push(i);
		sy.push(j);
		num_placed++;
		i++;
		while(sx.size() > 0)
		{
			if(backtrack == false)
			{
				if(isSafe(board, i, j, n))
				{
					board[i][j] = 1;
					sx.push(i);
					sy.push(j);
					still_looking = true;
					num_placed++;
				}
			}
			if(num_placed == num_queens)
				return true;
			if(i > n - 1)
			{
				if(j+1 < n)
				{
					if((num_queens - num_placed) > (n - j - 1 + trees[j+1]))
					{
						backtrack = true;	
					}
				}
				i=-1;
				j++;
			}
			if(j>n || backtrack == true)
			{
				i = sx.top();
				j = sy.top();
				board[i][j] = 0;
				sx.pop();
				sy.pop();
				num_placed--;
				backtrack = false;
			}
			i++;
			time(&end);
			if(difftime (end,start) >= 290)
        		return false;
		}
		row++;
		if(row >= n)
		{
			row =0;
			col++;
		}
	}
	return false;
}

int main()
{
	ifstream input;
	ofstream output;
 	remove("output.txt");
	input.open("input.txt");
	output.open("output.txt");
	char method[3];
	int N , i, j, num_queens, row = 0, ach = 0, rocks=0;
	input >> method;
	input >> N;
	input >> num_queens;
	int board[N][N];
	char string[N];
	int trees[N];
	memset(trees, 0, N*sizeof(int));
	for(i =0; i<N;i++)
	{
		input >> string;
		for(j=0;j<N;j++)
		{
			board[i][j] = string[j] - '0';
			if(board[i][j] == 2)
			{	
				rocks++;
				trees[i]++;
			}
		}
	}
	for(i=1; i<N; i++)
		trees[N-i-1] += trees[N-i];

	if(N+rocks < num_queens)
    {
		output << "FAIL";
    }
	else if(rocks+num_queens > N*N)
		output << "FAIL";
	else if(method[0] == 'D')
	{
		ach = placedDFS(board, N, num_queens, trees);
		if(ach == 1)
			printarr(board, N, output);
		else
			output << "FAIL";
	}
	else if(method[0] == 'B')
	{
		placedBFS(board, N, num_queens, output);
	}
	else if(method[0] == 'S')
	{
		placedSA(board, N, num_queens, output);
	}
}