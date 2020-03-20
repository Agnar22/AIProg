#include "Hex.cpp"

#define NEGINF -100000

class MCTS {
	private:
		
		unordered_map<string, int> stateVisits; // key = state : value = times visited
		unordered_map<string, vector<string>> actions; // key = state : values = actions
		unordered_map<string, vector<float>> stateAction; // key = state_action : values = {visits, sum q values}
		float expParam;

		pair<int, int> singleSearch(Hex game) {
			if (game.isFinished())
				return game.outcome();

			string state = game.getState();

			// Tree search
			if (stateVisits.find(state) != stateVisits.end())
				return treeSearch(game, state);
			
			
			// Node expansion
			nodeExpansion(game, state);

			//Leaf evaluation
			pair<string, pair<float, float>> evaluation = rollout(game);			
			string action = evaluation.first;
			
			float outcome = (game.getTurn() == 0) ? evaluation.second.first : evaluation.second.second;
			
			//Backpropagation
			stateVisits[state] += 1;
			stateAction[state + "_" + action] = vector<float> {1, outcome};
			return evaluation.second;
		}

		pair<int, int> treeSearch(Hex game, string state) {
			string move = selectAction(game, state);
			game.executeMove(move);
			pair<int, int> outcome = singleSearch(game);
			game.undoMove();
			int playerOutcome = (game.getTurn() == 0) ? outcome.first : outcome.second;

			stateVisits[state] += 1;
			string stateActionName = state + "_" + move;
			stateAction[stateActionName][0] += 1;
			stateAction[stateActionName][0] += playerOutcome;
			return outcome;
		}

		string selectAction(Hex game, string state) {
			float maxVal = NEGINF;
			string maxAction = "";

			for (auto action : game.getLegalMoves()) {
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

		void nodeExpansion(Hex game, string state) {
			stateVisits[state] = 0;
			vector<string> legalActions = game.getLegalMoves();
			actions[state] = legalActions;
			
			for (auto action : legalActions) {
				string stateActionName = state + "_" + action;
				stateAction[stateActionName] = vector<float> {0, 0};
			}
		}

		pair<string, pair<float, float>> rollout(Hex game) {
			string firstAction = "";
			int moveCount = 0;

			while (game.isFinished()) {
				vector<string> moves = game.getLegalMoves();
				int actionNum = rand() % moves.size();
				if (moveCount == 0)
					firstAction = moves[actionNum];
				game.executeMove(moves[actionNum]);
				moveCount++;
			}

			for (int x = 0; x < moveCount; x++) {
				game.undoMove();
			}
			return make_pair(firstAction, game.outcome());
		}

		static float uct(float c, int parentVisits, vector<float> child) {
			if (child[0] == 0)
				return NEGINF;
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
			for (auto action : actions[state])
				statistics.push_back(stateAction[state + "_" + action]);
			return make_pair(stateVisits[state], statistics);
		}

		void setExpParam(float inpExpParam) {
			expParam = inpExpParam;
		}

		void search(Hex game, int searchNum) {
			game.storeState();
			
			for (int x = 0; x < searchNum; x++) {
				singleSearch(game);
				game.loadState();
			}
		}
};

int main(){
	MCTS treeSearch;
	Hex game(5, 1);
	treeSearch.setExpParam(1.0);
	auto start = chrono::high_resolution_clock::now();
	treeSearch.search(game, 90000);
	auto stop = chrono::high_resolution_clock::now();
	cout << chrono::duration_cast<chrono::microseconds>(stop - start).count() << endl;
}
