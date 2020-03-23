#include "Hex.h"
#include <unordered_map>
#include <chrono>
#include <cstdlib>
#include <pthread.h>
#include <thread>

#define NEGINF -100000


class MCTS {
	private:
		
		unordered_map<string, int> stateVisits; // key = state : value = times visited
		unordered_map<string, vector<string>> actions; // key = state : values = actions
		unordered_map<string, vector<float>> stateAction; // key = state_action : values = {visits, sum q values}
		float expParam;
		Hex game;

		pair<int, int> singleSearch() {
			//cout << game.isFinished() << endl;
			//cout << "test" << endl;

			if (game.isFinished()) {
				//cout << "finished " << game.outcome().first << endl;
				//game.printBoard();
				return game.outcome();
			}

			string state = game.getState();

			// Tree search
			if (stateVisits.find(state) != stateVisits.end())
				return treeSearch(state);
			
			
			// Node expansion
			nodeExpansion(state);

			//Leaf evaluation
			pair<string, pair<float, float>> evaluation = rollout();			
			string action = evaluation.first;
			
			float outcome = (game.getTurn() == 1) ? evaluation.second.first : evaluation.second.second;
			//if (outcome > 0)
			//	cout << endl;
			
			//Backpropagation
			stateVisits[state] += 1;
			stateAction[state + "_" + action] = vector<float> {1, outcome};
			return evaluation.second;
		}

		pair<int, int> treeSearch(string state) {
			string move = selectAction(state);
			//cout << "treeSearch " << state << endl;
			game.executeMove(move);
			pair<int, int> outcome = singleSearch();
			game.undoMove();
			int playerOutcome = (game.getTurn() == 1) ? outcome.first : outcome.second;

			stateVisits[state] += 1;
			string stateActionName = state + "_" + move;
			stateAction[stateActionName][0] += 1;
			stateAction[stateActionName][1] += playerOutcome;
			return outcome;
		}

		string selectAction(string state) {
			float maxVal = NEGINF;
			string maxAction = "";
			//cout << state << " test" << endl;
			vector<string>* legalMoves = game.getLegalMoves(new vector<string>());

			for (auto action : (*legalMoves)) {
				float score = MCTS::uct(expParam, stateVisits[state], stateAction[state + "_" + action]);
				if (score == NEGINF) 
					return action;
				if (maxVal == NEGINF || score > maxVal) {
					maxVal = score;
					maxAction = action;
				}
			}
			return maxAction;
		}

		void nodeExpansion(string state) {
			stateVisits[state] = 0;
			vector<string>* legalActions = game.getLegalMoves(new vector<string>());
			actions[state] = (*legalActions);
			
			for (auto action : (*legalActions)) {
				string stateActionName = state + "_" + action;
				stateAction[stateActionName] = vector<float> {0, 0};
			}
		}

		pair<string, pair<float, float>> rollout() {
			string firstAction = "";
			int moveCount = 0;

			while (!game.isFinished()) {
				//game.printBoard();
				//cout << "getting moves "<< endl;
				vector<string>* moves = game.getLegalMoves(new vector<string>());
				//cout << "got moves " << moves.size()<< endl;
				int actionNum = rand() % moves->size();
				if (moveCount == 0)
					firstAction = (*moves)[actionNum];
				//cout << "rollout " << game.getState()<< endl;
				game.executeMove((*moves)[actionNum]);
				moveCount++;
				//cout << "executed"<< endl;
			}
			pair<float, float> outcome = game.outcome();
			//cout << "finish rollout " << game.getState()<< endl;

			for (int x = 0; x < moveCount; x++) {
				game.undoMove();
			}
			//cout << moveCount << " " << outcome.first << " " << game.getTurn() << endl;
			return make_pair(firstAction, outcome);
		}

		static float uct(float c, int parentVisits, vector<float> child) {
			//cout << child[0] << " " << child[1] << " " << parentVisits << endl;
			if (child[0] == 0)
				return NEGINF;
			float exploration = c * sqrt(log(parentVisits) / child[0]);
			float qValue = child[1] / child[0];
			return qValue + exploration;
		}

	public:
		MCTS() : game(5,1) {
			cout << "Starting" << endl;
		}

		string getRecommendedMove(string state){
			int maxVisits = -1;
			string bestAction = "";

			for (auto action : actions[state]) {
				int visits = stateAction[state + "_" + action][0];
				
				if (maxVisits == -1 || visits > maxVisits) {
					maxVisits = visits;
					bestAction = action;
				}
			}
			return bestAction;
		}

		pair<int, vector<vector<float>>> getSearchStatistics(string state) {
			vector<vector<float>> statistics;
			cout << stateVisits[state] << endl;
			for (auto action : actions[state]) {
				statistics.push_back(stateAction[state + "_" + action]);
				cout << statistics.back()[0] << " " << statistics.back()[1] << endl;
			}
			return make_pair(stateVisits[state], statistics);
		}

		void setExpParam(float inpExpParam) {
			expParam = inpExpParam;
		}

		void setGame(Hex inpGame){
			game = inpGame;
		}

		void search(int searchNum) {
			//TODO: store and load should not be needed
			//game.storeState();
			
			for (int x = 0; x < searchNum; x++) {
				singleSearch();
				//game.loadState();
			}
		}
};

void multithread(){
	MCTS treeSearch;
	Hex game(4, 1);
	Hexagonal game2OfHex(4);
	game.setHexagonal(&game2OfHex);
	treeSearch.setExpParam(1.0);
	treeSearch.setGame(game);
	treeSearch.search(100000);
	treeSearch.getSearchStatistics("");

}

int main(){
	// TODO: 
	// fix some bug somewhere:(
	// speed up code: use pointers for vectors
	int size = 1;
	thread threads[size];
	auto start = chrono::high_resolution_clock::now();
	for (int x = 0; x < size; x++){
		threads[x] = thread(multithread);
	}
	for (int x = 0; x < size; x++){
		threads[x].join();
	}
	auto stop = chrono::high_resolution_clock::now();
	cout << chrono::duration_cast<chrono::microseconds>(stop - start).count() << endl;

	system("pause");
}
