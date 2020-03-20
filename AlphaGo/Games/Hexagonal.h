#define HEXAGONAL_H
#include <vector>

using namespace std;

class Hexagonal {
	private:


		vector<pair<int, int>> neighbours = {
			make_pair(-1, 0), make_pair(-1, 1), make_pair(0, -1),
		       	make_pair(0, 1), make_pair(1, -1), make_pair(1, 0)
		};
		vector<vector<int>> board;

	public:
		Hexagonal(int boardSize);

		vector<vector<int>> createBoard(int size);

		vector<vector<int>> getBoard();

		void setBoard(vector<vector<int>> inpBoard);

		vector<int> getUnoccupied();

		vector<int> getNeighbours(int pos, int value);
		
		pair<int, int> border(int position);

		int getSquare(int pos);

		int setSquare(int pos, int value);
};


