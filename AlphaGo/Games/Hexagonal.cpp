#include "Hexagonal.h"
#include<vector>
#include<string>
#include<iostream>

using namespace std;

Hexagonal::Hexagonal(int boardSize){
			createBoard(boardSize);
		}
vector<vector<int>> Hexagonal::createBoard(int size){
			board.assign(size, vector<int> (size, 0));
		}
vector<vector<int>> Hexagonal::getBoard(){
			//TODO: make this a return a reference
			return board;
		}
void Hexagonal::setBoard(vector<vector<int>> inpBoard){
			//TODO: make this a return a reference
			board = inpBoard;
		}

		vector<int> Hexagonal::getUnoccupied(){
			//TODO: make this a return a reference
			vector<int> unoccupied;
			for (int x=0; x < board.size(); x++){
				for (int y=0; y < board[0].size(); y++){
					if (board[x][y] == 0){
						int pos = x * board[0].size() + y;
						unoccupied.push_back(pos);
					}
				}
			}
			return unoccupied;
		}


		vector<int> Hexagonal::getNeighbours(int pos, int value){
			//TODO: make this a return a reference
			int x = pos / board[0].size();
			int y = pos % board[0].size();
			vector<int> actualNeighbours;
			for (int dir = 0; dir < neighbours.size(); dir++){
				int neigh_x = x + neighbours[dir].first;
				int neigh_y = y + neighbours[dir].second;
				if (neigh_x >= 0 && neigh_x < board.size() &&
				       	neigh_y >= 0 && neigh_y < board.size() && 
					board[neigh_x][neigh_y] == value){
					actualNeighbours.push_back(neigh_x * board[0].size() + neigh_y);
				}
			}
			return actualNeighbours;
		}

		pair<int, int> Hexagonal::border(int position){
			/*	0/\1
			 *	2\/3
			 */
			pair<int, int> borders = make_pair(-1, -1);
			int x = position / board[0].size();
			int y = position % board[0].size();

			if (x == 0){
				borders.first == 1;
			}
			else if (x == board.size()-1){
				borders.first == 2;
			}
			if (y == 0){
				borders.second == 0;
			}
			else if (y == board[0].size()-1){
				borders.second == 3;
			}
			return borders;
		}

		int Hexagonal::getSquare(int pos){
			return board[pos / board[0].size()][pos % board[0].size()];
		}

	
		int Hexagonal::setSquare(int pos, int value){
			board[pos / board[0].size()][pos % board[0].size()] = value;
		}




/*
class Hexagonal {
		
	private:
		vector<pair<int, int>> neighbours = {
			make_pair(-1, 0), make_pair(-1, 1), make_pair(0, -1),
		       	make_pair(0, 1), make_pair(1, -1), make_pair(1, 0)
		};
		vector<vector<int>> board;
	
	
	public:

		Hexagonal(int boardSize){
			createBoard(boardSize);
		}

		vector<vector<int>> createBoard(int size){
			board.assign(size, vector<int> (size, 0));
		}

		vector<vector<int>> getBoard(){
			//TODO: make this a return a reference
			return board;
		}

		void setBoard(vector<vector<int>> inpBoard){
			//TODO: make this a return a reference
			board = inpBoard;
		}

		vector<int> getUnoccupied(){
			//TODO: make this a return a reference
			vector<int> unoccupied;
			for (int x=0; x < board.size(); x++){
				for (int y=0; y < board[0].size(); y++){
					if (board[x][y] == 0){
						int pos = x * board[0].size() + y;
						unoccupied.push_back(pos);
					}
				}
			}
			return unoccupied;
		}


		vector<int> getNeighbours(int pos, int value){
			//TODO: make this a return a reference
			int x = pos / board[0].size();
			int y = pos % board[0].size();
			vector<int> actualNeighbours;
			for (int dir = 0; dir < neighbours.size(); dir++){
				int neigh_x = x + neighbours[dir].first;
				int neigh_y = y + neighbours[dir].second;
				if (neigh_x >= 0 && neigh_x < board.size() &&
				       	neigh_y >= 0 && neigh_y < board.size() && 
					board[neigh_x][neigh_y] == value){
					actualNeighbours.push_back(neigh_x * board[0].size() + neigh_y);
				}
			}
			return actualNeighbours;
		}

		pair<int, int> border(int position){
			pair<int, int> borders = make_pair(NULL, NULL);
			int x = position / board[0].size();
			int y = position % board[0].size();

			if (x == 0){
				borders.first == 1;
			}
			else if (x == board.size()-1){
				borders.first == 2;
			}
			if (y == 0){
				borders.second == 0;
			}
			else if (y == board[0].size()-1){
				borders.second == 3;
			}
			return borders;
		}

		int getSquare(int pos){
			return board[pos / board[0].size()][pos % board[0].size()];
		}

	
		int setSquare(int pos, int value){
			board[pos / board[0].size()][pos % board[0].size()] = value;
		}
};
*/

/*
int main(){
	Hexagonal hex_board(5);
};
*/