#include "Hex.h"
#include <set>
#include <chrono>



Hex::Hex(int boardSize, int inpStartingPlayer) {
			Hexagonal gameOfHex(boardSize);
			hexBoard = &gameOfHex;
			startingPlayer = inpStartingPlayer;
			state = "";
		}

		string Hex::getState(){
			return state;
		}

		int Hex::getTurn() {
			return (history.size() + startingPlayer + 1) % 2 + 1;
		}

		void Hex::storeState(){
			storeBoard = hexBoard->getBoard();
			storeHistory = history;
		}

		void Hex::loadState(){
			hexBoard->setBoard(storeBoard);
			history = storeHistory;
		}

		vector<string> Hex::getLegalMoves(){
			return hexBoard->getUnoccupied();
		}

		void Hex::executeMove(string move){
			//cout << "move" << move << endl;
			state += "_" + move;
			hexBoard->setSquare(stoi(move), getTurn());
			history.push_back(stoi(move));
			//cout << "done executing" << endl;
		}

		void Hex::undoMove(){
			int move = history.back();
			history.pop_back();
			hexBoard->setSquare(move, 0);
			state = state.substr(0, state.length() - to_string(move).length()-1);
		}	
		
		bool Hex::isFinished(){
			if (history.size() == 0){
				return false;
			}
			vector<bool> border = {false, false, false, false};
			vector<int> neighbours = {history.back()};
			set<int> addedNeighbours = {history.back()};
			int colour = hexBoard->getSquare(history.back());
			int pos = 0;

			while (pos < neighbours.size()){
				int currPos = neighbours[pos];
				pair<int, int> borderSides = hexBoard->border(currPos);
				if (borderSides.first != -1){
					border[borderSides.first] = true;
				}
				if (borderSides.second != -1){
					border[borderSides.second] = true;
				}
				vector<int> currNeighbours = hexBoard->getNeighbours(currPos, colour);
				
				for (int x = 0; x < currNeighbours.size(); x++){
					if (addedNeighbours.find(currNeighbours[x]) == addedNeighbours.end()){
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

		pair<float, float> Hex::outcome(){
			//cout << "historylength " << history.size()  << " " << startingPlayer << endl;
			return ((history.size() + startingPlayer) % 2 ) ? make_pair(-1.0, 1.0) : make_pair(1.0, -1.0);
		}

		void Hex::printBoard(){
			vector<vector<int>> board = hexBoard->getBoard();

			for (auto row : board){
				for (auto cell : row) {
					cout << to_string(cell) << " ";
				}
				cout << endl;
			}
		}

		void Hex::setHexagonal(Hexagonal* inpGame) {
			hexBoard = inpGame;
}
/*
set<string> visited;
int endPos = 0;

int dfs(Hex* game, int depth){
	//cout << depth << endl;
	if (depth == 0) {
		endPos++;
		return 0;
	}
	if (game->isFinished()){
		return 0;
	}
	vector<string> moves = game->getLegalMoves();
	//cout << moves.size() << endl;
	for (int x = 0; x < moves.size(); x++){
		game->executeMove(moves[x]);
		dfs(game, depth-1);
		game->undoMove();
	}
	return 0;
}
int main(){
	Hexagonal game2OfHex(5);
	Hex game(5, 1);
	game.setHexagonal(&game2OfHex);
	auto start = chrono::high_resolution_clock::now();
	dfs(&game, 4);
	auto stop = chrono::high_resolution_clock::now();
	cout << chrono::duration_cast<chrono::microseconds>(stop - start).count() << " " << endPos << endl;
	system("pause");
}

*/