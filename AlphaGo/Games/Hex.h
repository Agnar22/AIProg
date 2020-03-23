#ifndef HEX_H
#define HEX_H
#include "Hexagonal.h"

class Hex {

	private:
		Hexagonal* hexBoard;
		vector<vector<int>> storeBoard;
		int startingPlayer;
		vector<int> history;
		vector<int> storeHistory;
		string state;


	public:

		Hex(int, int);

		void setHexagonal(Hexagonal* inpGame);

		string getState(void);

		int getTurn(void);

		void storeState(void);

		void loadState(void);

		vector<string>* getLegalMoves(vector<string>*);

		void executeMove(string);

		void undoMove(void);

		bool isFinished(void);

		pair<float, float> outcome(void);

		void printBoard(void);
};

#endif
