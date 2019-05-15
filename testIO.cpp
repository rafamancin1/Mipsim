#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main() {
	ifstream f;
	string line;
	f.open("ex.txt");
	cout << f.tellg() << endl;
	f.seekg(4, ios::beg);
	while(getline(f, line)) {
		cout << line << endl;
		cout << f.tellg() << endl;
	}
	f.close();
	return 0;
}
