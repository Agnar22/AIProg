#include <vector>
#include <iostream>
#include <string>
#include <cmath>
#include <stdlib.h>
#include <bits/stdc++.h>

using namespace std;

class MCTS {
	private:
		
		unordered_map<string, int> stateVisits; // key = state : value = times visited
		unordered_map<string, vector<string>> actions; // key = state : values = actions
		unordered_map<string, vector<float>> stateAction; // key = state_action : values = {visits, sum q values}
		float expParam;

		pair<int, int> singleSearch(Hexagonal game) {
			if (game.isFinished())
				return game.outcome;

			string state = game.getState();

			// Tree search
			if (stateVisits.find(state) != stateVisits.end())
				return threeSearch(game, state);
			
			
			// Node expansion
			nodeExpansion(game, state);

			//Leaf evaluation
			pair<string, pair<int, int>> evaluation = rollout(game);			
			string action = evaluation.first;
			
			int outcome = (game.getTurn() == 0) ? evaluation.second.first : evaluation.second.second;
			
			//Backpropagation
			stateVisits[state] = stateVisits + 1;
			stateAction[state + "_" + action] = {1, outcome};
			return evaluation.second
		}

		pair<int, int> treeSearch(Hexagonal game, string state) {
			string move = selectAction(game, state);
			game.execute(move);
			pair<int, int> outcome = singleSearch(game);
			game.undoMove();
			int playerOutcome = (game.getTurn() == 0) ? outcome.first : outcome.second;

			stateVisits[state] = stateVisits + 1;
			string stateActionName = state + "_" + move;
			stateActions[stateActonName][0] += 1;
			stateActions[stateActonName][0] += playerOutcome;
			return outcome;
		}

		string selectAction(Hexagonal game, string state) {
			float maxVal = NULL;
			string maxAction = NULL;

			for (auto action : game.getLegalMoves()) {
				float score = MCTS.uct(expParam, stateVisits[state], state_action[state + "_" + action]);
				if (score == NULL) 
					return action;
				if (maxVal == NULL || score > maxVal) {
					maxVal = score;
					maxAction = action;
				}
			}
			return maxAction;
		}

		void nodeExpansion(Hexagonal game, string state) {
			stateVisits[state] = 0;
			vector<string> legalActions = game.getLegalMoves();
			actions[state] = legalActions;
			
			for (auto action : legalActions) {
				stateAction = vector<float> {0, 0};
			}
		}

		pair<string, pair<int, int> rollout(Hexagonal game) {
			string firstAction = NULL;
			int moveCount = 0;

			while (game.isFinished()) {
				vector<string> moves = game.getLegalMoves();
				int actionNum = rand() % moves.size();
				if (moveCount == 0)
					firstAction = moves[actionNum];
				game.executeMove(moves[actonNum]);
				moveCount++;
			}

			for (int x = 0; x < moveCount; x++) {
				game.undoMove();
			}
			return make_pair(firstAction, game.outcome());
		}

		static float uct(float c, int parentVisits, vector<float> child) {
			if (child[0] == 0)
				return NULL;
			float exploration = c * sqrt(log(parentVisits) / child[0]);
			float qValue = child[1] / child[0];
			return qValue + exploration;
		}

	public:
		MCTS(){
			cout << "Constructed mcts" << endl;
		}

		string getRecommendedMove(string state){
			int maxVisits = -1;
			string bestAction = NULL;

			for (auto action : actions[state]) {
				int visits = stateAction[state + "_" + action][0];
				
				if (maxVisits == -1 || visits > maxVisits) {
					maxVisits = visits;
					bestAction = action;
				}
			}
			return bestAction;
		}

		pair<int, vector<vector<int>> getSearchStatistics(string state) {
			vector<vector<int>> statistics;
			for (auto action : actions[state])
				statistics.push_back(stateAction[state + "_" + action];
			return make_pair(stateVisits[state], statistics);
		}

		void setExpParam(float inpExpParam) {
			expParam = expParam
		}

		void search(Hexagonal game, int searchNum) {
			game.storeState();
			
			for (int x = 0; x < searchNum; x++) {
				singleSearch(game);
				game.loadState();
			}
		}
}
