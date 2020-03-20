#ifndef HEXAGONAL_H
#define HEXAGONAL_H
#include <vector>
#include <string>
#include <iostream>
#include <cmath>
#include <stdlib.h>
#include <bits/stdc++.h>

using namespace std;

class Hexagonal {
	private:


		vector<pair<int, int>> neighbours = {
			make_pair(-1, 0), make_pair(-1, 1), make_pair(0, -1),
		       	make_pair(0, 1), make_pair(1, -1), make_pair(1, 0)
		};
		vector<vector<int>> board;

	public:
		Hexagonal(int);

		Hexagonal(void);

		void createBoard(int);

		vector<vector<int>> getBoard(void);

		void setBoard(vector<vector<int>>);

		vector<string> getUnoccupied(void);

		vector<int> getNeighbours(int, int);
		
		pair<int, int> border(int);

		int getSquare(int);

		int setSquare(int, int);
};

#endif
