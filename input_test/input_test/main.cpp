#include <iostream>
#include <fstream>

using namespace std;
int main()
{
//    std::string str_dec = "2001, A Space Odyssey";
//    std::string a_str = "32";
//    std::string str_hex = "40c3";
//    std::string str_bin = "-10010110001";
//    std::string str_auto = "0x7f";
//
//    std::string::size_type sz;   // alias of size_t
//
//    int i_dec = std::stoi (str_dec,&sz);
//    int hello = std::stoi (a_str, &sz);
//    cout << hello << endl;
//    int i_hex = std::stoi (str_hex,nullptr,16);
//    int i_bin = std::stoi (str_bin,nullptr,2);
//    int i_auto = std::stoi (str_auto,nullptr,0);
//
//    std::cout << str_dec << ": " << i_dec << " and [" << str_dec.substr(sz) << "]\n";
//    std::cout << str_hex << ": " << i_hex << '\n';
//    std::cout << str_bin << ": " << i_bin << '\n';
//    std::cout << str_auto << ": " << i_auto << '\n';
//
//    return 0;
    ifstream inputFile("6.txt");
    if (!inputFile)
    {
        cout << "error opening input file\n";
        return 1;
    }
    int line_count = 0;
//    int row_count = 0;
//    int col_count = 0;
    std:: string::size_type sz;     // alias of size_t
    for( string line; getline( inputFile, line ); )
    {
        if(line_count == 0) {
            cout << line << endl;
//            row_count = std::stoi(line, &sz);
        }else if (line_count == 1) {
            cout << line << endl;
//            col_count = std::stoi(line, &sz);
        }else {
//            cout << line << endl;
            cout << "end of line " << endl;
        }
//        cout << line << endl;
        line_count ++;
    }

    inputFile.close();
    return 0;
}

