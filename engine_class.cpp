
#include<iostream>
#include<vector>
#include<unordered_map>

using namespace std;


// class Piece{
//     public:
//     // piece values
//     const int Empty = 0;
//     const int King = 1;
//     const int Pawn = 2;
//     const int Knight = 3;
//     const int Bishop = 4;
//     const int Rook = 5;
//     const int Queen = 6;

//     const int White = 8;
//     const int Black = 16;

//     int pieceType = 0;
//     int pieceColor = 0;
//     Location at;
//     Piece(int pt, int pc){
//         pieceType = pt;
//         pieceColor = pc;
//     }
//     Piece(){
//         pieceType = 0;
//         pieceColor = 0;
//         at = Location(-1);
//     }
// };



// class Location{
//     public:
//     int square;

//     Location(int sq){
//         square = sq;
//     }

//     pair<int,int> xy(){
//         return make_pair(square/8, square%8);
//     }

//     int sq(){
//         return square;
//     }
//     Location(){

//     }


// };



// class Move{
//     public:
//     Location start;
//     Location end;
//     int flag;

//     const int is_capture = 1;
//     const int is_castle = 2;
//     const int is_promotion = 4;
//     const int is_double_pawn_move = 8;
//     const int is_ep = 16;
// };



// class BitBoard{
//     unsigned long long bits = 0;
// };




class Board{
    public:

    // vector<Piece> pieces;

    unsigned long long bitboards[12]; // 0-5 white 6-11 black k,p,n,b,r,q


    Board(){
        LoadFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");
    }


    void set_piece(int p,int sq){
        // cout << "Set piece " << p << ", at " << sq << endl;
        // cout << bitboards[p];
        unsigned long long one = 1;
        bitboards[p] |= (one<<sq);
        // cout << " to " << bitboards[p] << endl;
    }

    void remove_piece(int p, int sq){
        unsigned long long one = 1;
        bitboards[p] = ~((~bitboards[p]) | (one<<sq)); 
    }


    void reset_bitboards(){
        for (int i=0;i<12;i++){
            bitboards[i] = 0;
        }
    }


    void LoadFEN(string FEN){
        cout << "Loading FEN: " << FEN << endl;
        unordered_map<char,int> char_to_piece = {
            {'K',0}, {'P', 1}, {'N',2}, {'B', 3}, {'R', 4}, {'Q', 5},
            {'k',6}, {'p', 7}, {'n',8}, {'b', 9}, {'r', 10}, {'q', 11}
        };
        // cut string
        vector<string> data;
        for (int i=0; i<6; i++){
            int space_index = FEN.find(" ");
            string substr = FEN.substr(0, space_index);
            data.push_back(substr);
            FEN = FEN.substr(space_index+1, FEN.length());
        }
        string pieces = data[0];
        reset_bitboards();
        int point = 0;
        for (int c = 0; c<pieces.length(); c++){
            char curr_char = pieces[c];
            if (isdigit(pieces[c])){
                point += (int)curr_char - 48;
            }
            else if (curr_char != '/'){
                int piece_type = char_to_piece[curr_char];
                set_piece(piece_type, point);
                point ++;
            }
        }
    }

    void print(){
        for (int i=0; i<12; i++){
            cout << "Bitboard " << i << ": " << endl;
            print_bitbboard(bitboards[i]);
        }
    }

    void print_bitbboard(unsigned long long bb){
        for (int i=0;i<64;i++){
            if (i%8==0 && i!=0){
                cout << endl;
            }
            unsigned long long one = 1;
            if(bb & one<<i){
                cout << "X";
            }
            else{
                cout << ".";
            }
        }
        cout << endl;
    }
};



int main(){
    Board b = Board();
    b.print();
    return 0;
}