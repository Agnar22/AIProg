#include "Hexagonal.h"

Hexagonal::Hexagonal(int boardSize){
	createBoard(boardSize);
}
Hexagonal::Hexagonal(){
	createBoard(5);
}

void Hexagonal::createBoard(int size){
	board.assign(size, vector<int> (size, 0));
}
vector<vector<int>> Hexagonal::getBoard(){
	return board;
}
void Hexagonal::setBoard(vector<vector<int>> inpBoard){
	board = inpBoard;
}

vector<string>* Hexagonal::getUnoccupied(vector<string>* inpGetUnoccupied){
	inpGetUnoccupied->reserve(board.size()*board[0].size());
	for (int x=0; x < board.size(); x++){
		for (int y=0; y < board[0].size(); y++){
			if (board[x][y] == 0){
				int pos = x * board[0].size() + y;
				(*inpGetUnoccupied).push_back(to_string(pos));
			}
		}
	}
	return inpGetUnoccupied;
}


vector<int>* Hexagonal::getNeighbours(int pos, int value, vector<int>* inpActualNeighbours){
	int x = pos / board[0].size();
	int y = pos % board[0].size();
	inpActualNeighbours->reserve(neighbours.size());
	for (int dir = 0; dir < neighbours.size(); dir++){
		int neigh_x = x + neighbours[dir].first;
		int neigh_y = y + neighbours[dir].second;
		if (neigh_x >= 0 && neigh_x < board.size() &&
			neigh_y >= 0 && neigh_y < board.size() && 
			board[neigh_x][neigh_y] == value){
			(*inpActualNeighbours).push_back(neigh_x * board[0].size() + neigh_y);
		}
	}
	return inpActualNeighbours;
}

pair<int, int> Hexagonal::border(int position){
	/*
	 *	0/\1
	 *	2\/3
	 */
	pair<int, int> borders = make_pair(-1, -1);
	int x = position / board[0].size();
	int y = position % board[0].size();
	//cout << "pos " << position << " " << x << " " << y << endl;

	if (x == 0){
		borders.first = 1;
	}
	else if (x == board.size()-1){
		borders.first = 2;
	}
	if (y == 0){
		borders.second = 0;
	}
	else if (y == board[0].size()-1){
		borders.second = 3;
	}
	//cout << "borders " << borders.first << " " << borders.second << endl;
	return borders;
}

int Hexagonal::getSquare(int pos){
	return board[pos / board[0].size()][pos % board[0].size()];
}


void Hexagonal::setSquare(int pos, int value){
	board[pos / board[0].size()][pos % board[0].size()] = value;
}



/*
int main(){
	int num  = 5;
	cout << "hei" << endl;
	Hexagonal hexGame;
	cout << "Hei" << endl;
};
*/
