#include <vector>
#include <iostream>
#include <set>
#include <string>
#include "Hexagonal.h"


class Hex {

	private:
		Hexagonal hexBoard;
		int startingPlayer;
		string state;


	public:

		Hex(int boardSize, int inpStartingPlayer){
			hexBoard = Hexagonal(boardSize);
			vector<vector<int>> storeBoard;
			vector<int> history;
			vector<int> storeHistory;
			startingPlayer = inpStartingPlayer;
			state = "";
		}

		string getState(){
			return state;
		}

		int getTurn(){
			return (hitsory.size() + inpStartingPlayer + 1) % 2 + 1;
		}

		void storeState(){
			storeBoard = hexBoard.getBoard();
			storeHistory = history;
		}

		void loadState(){
			hex.setBoard(storeBoard);
			history = storeHistory;
		}

		vector<int> getLegalMoves(){
			return hexBoard.getUnoccupied();
		}

		void executeMove(int move){
			state = state + "_" + to_string(move);
			hexBoard.setSquare(move, getTurn());
			history.push_back(move);
		}

		void undoMove(){
			int move = history.back();
			history.pop();
			hexBoard.seqSquare(move, 0);
			state = state.substr(0, state.length() - to_string(move).length()-1);
		}	
		
		bool isFinished(){
			if (history.length() == 0){
				return false;
			}
			vector<bool> border = {false, false, false, false};
			vector<int> neighbours = {history.back()};
			set<int> addedNeighbours = {history.back()};
			int colour = hexBoard.getSquare(history.back());
			int pos = 0;

			while (pos < neighbours.length()){
				int currPos = neighbours[pos];
				pair<int, int> borderSides = hexBoard.border(currPos);
				if (borderSides.first != -1){
					border[borderSides.first] = true;
				}
				if (borderSides.second != -1){
					border[borderSides.second] = true;
				}
				vector<int> currNeighbours = hexBoard.getNeighbours(currPos);
				
				for (int x = 0; x < currNeighbours.size(); x++){
					if (addedNeighbours.find(currNeighbours[x]) == s.end()){
						neighbours.push_back(currNeighbours[x]);
						addedNeighbours.insert(currNeighbours[x]);
					}
				}
				pos++;
			}
			bool wonPlayerOne = border[0] && border[3] && colour == 1;
			bool wonPlayerTwo = border[1] && border[2] && colour == 2;
			return (wonPlayerOne || wonPlayerTwo) ? true : false;
		}

		int outcome(){
			return (history.length() + startingPlayer ) % 2;
		}
}

set<string> visited;
int endPos = 0;

int dfs(Hex game, int depth){
	if (depth == 0) {
		endpos++;
		return 0;
	}
	if (game.isFinished()){
		return 0;
	}
	vector<int> moves = game.getLegalMoves();

	for (int x = 0; x < moves.size(); x++){
		game.executeMove(moves[x]);
		dfs(game, depth-1);
		game.undoMove();
	}
	return 0;
}


int main(){
	Hex game(5, 1);
	dfs(game, 4);
	cout << endPos << endl;

}

