#include <iostream>
#include <sstream>
using namespace std;
  
void extractIntegerWords(string str)
{
    stringstream ss;    
  
    /* Storing the whole string into string stream */
    ss << str;
  
    /* Running loop till the end of the stream */
    string temp;
    int found;
    while (!ss.eof()) {
  
        /* extracting word by word from stream */
        ss >> temp;
  
        /* Checking the given word is integer or not */
        if (stringstream(temp) >> found)
            cout << found << " ";
  
        /* To save from space at the end of string */
        temp = "";
    }
}
  
// Driver code
int main()
{
    string str = "OPTIMAL_VALUE: 384.678035 ";
    extractIntegerWords(str);
    return 0;
}