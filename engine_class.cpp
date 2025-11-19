
#include<iostream>
#include<vector>
#include<unordered_map>

using namespace std;


class Piece{
    public:
    // piece values
    const int Empty = 0;
    const int King = 1;
    const int Pawn = 2;
    const int Knight = 3;
    const int Bishop = 4;
    const int Rook = 5;
    const int Queen = 6;

    const int White = 8;
    const int Black = 16;

    int pieceType = 0;
    int pieceColor = 0;
    Location at;
    Piece(int pt, int pc){
        pieceType = pt;
        pieceColor = pc;
    }
    Piece(){

    }
};



class Location{
    public:
    int square;

    Location(int sq){
        square = sq;
    }

    pair<int,int> xy(){
        return make_pair(square/8, square%8);
    }

    int sq(){
        return square;
    }
    Location(){

    }


};



class Move{
    public:
    Location start;
    Location end;
    int flag;

    const int is_capture = 1;
    const int is_castle = 2;
    const int is_promotion = 4;
    const int is_double_pawn_move = 8;
    const int is_ep = 16;
};



class Board{

    vector<Piece> pieces;


    Board(){

    }

    void LoadFEN(string FEN){

    }
};



int main(){
    return 0;
}