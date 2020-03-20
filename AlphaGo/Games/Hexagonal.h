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
		Hexagonal(int);

		Hexagonal(void);

		void createBoard(int);

		vector<vector<int>> getBoard(void);

		void setBoard(vector<vector<int>>);

		vector<int> getUnoccupied(void);

		vector<int> getNeighbours(int, int);
		
		pair<int, int> border(int);

		int getSquare(int);

		int setSquare(int, int);
};


