
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

//     Location(){
//         square=-1;
//     }

//     pair<int,int> xy(){
//         return make_pair(square/8, square%8);
//     }

//     int sq(){
//         return square;
//     }
    


// };



struct Move{
    int start; //start sq
    int end; // end sq

    bool is_capture = false;
    bool is_castle = false;
    bool is_promotion = false;
    bool is_double_pawn_move = false;
    bool is_ep = false;

    Move(int s, int e){
        start = s;
        end = e;
    }
};



struct BitBoard{
    unsigned long long FULL = ULLONG_MAX;
    unsigned long long LEFT_COL = 0x0101010101010101;
    unsigned long long TOP_ROW = 0x00000000000000ff;


    void print(unsigned long long bb){
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




class Board{
    public:

    // vector<Piece> pieces;

    unsigned long long bitboards[12]; // 0-5 white 6-11 black k,p,n,b,r,q
    unsigned long long all_black_pieces;
    unsigned long long all_white_pieces;
    unsigned long long empty_squares;
    bool is_white_turn;
    vector<vector<bool>> casteling_rights;
    vector<int> ep_sq;

    unordered_map<char,int> char_to_piece = {
        {'K',0}, {'P', 1}, {'N',2}, {'B', 3}, {'R', 4}, {'Q', 5},
        {'k',6}, {'p', 7}, {'n',8}, {'b', 9}, {'r', 10}, {'q', 11}
    };

    unordered_map<int,char> piece_to_char = {
        {0, 'K'}, {1, 'P'}, {2, 'N'}, {3, 'B'}, {4, 'R'}, {5, 'Q'},
        {6, 'k'}, {7, 'p'}, {8, 'n'}, {9, 'b'}, {10, 'r'}, {11, 'q'}, 
        {-1, '.'}
    };




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
        all_white_pieces = 0;
        all_black_pieces = 0;
        empty_squares = 0;
    }


    void LoadFEN(string FEN){
        // cout << "Loading FEN: " << FEN << endl;
        
        // cut string
        vector<string> data;
        for (int i=0; i<6; i++){
            int space_index = FEN.find(" ");
            string substr = FEN.substr(0, space_index);
            data.push_back(substr);
            FEN = FEN.substr(space_index+1, FEN.length());
        }
        // load pieces
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
        for(int i = 0; i<=5 ; i++){
            all_white_pieces |= bitboards[i];
        }
        for(int i = 6; i<=11 ; i++){
            all_black_pieces |= bitboards[i];
        }
        empty_squares = ~(all_black_pieces|all_white_pieces);
        // load the rest of the data
        is_white_turn = (data[1]=="w") ? true : false;
        // casteling rights
        casteling_rights.clear();
        vector<bool> rights = {false, false, false, false};
        unordered_map<char,int> char_to_int_rights = {{'K', 0}, {'Q', 1}, {'k', 2}, {'q', 3}};
        for (int c = 0; c<data[2].length(); c++){
            char curr_char = data[2][c];
            if (not curr_char == '-'){
                rights[char_to_int_rights[curr_char]] = true;
            }
        }
        casteling_rights.push_back(rights);
        // ep_sq
        // move_counters

    }

    void print(){
        for (int i=0; i<64; i++){
            int p = piece_on_sq(i);
            cout << piece_to_char[p];
            if (i%8==7){
                cout << endl;
            }
        }
        // print castle rights
    }


    int piece_on_sq(int sq){
        unsigned long long one = 1;
        unsigned long long to_check = one<<sq;
        for(int i = 0; i<=11; i++){
            if (bitboards[i] & to_check){
                return i;
            }
        }
        return -1;
    }


    void make_move(Move m){
        // check non special moves first
        if (not (m.is_castle or m.is_capture or m.is_ep)){

        }
        else if (m.is_castle){

        }
        else if (m.is_ep){

        }
        else if (m.is_capture){

        }
        // update all piece boards
        all_white_pieces = 0;
        all_black_pieces = 0;
        empty_squares = 0;
        for(int i = 0; i<=5 ; i++){
            all_white_pieces |= bitboards[i];
        }
        for(int i = 6; i<=11 ; i++){
            all_black_pieces |= bitboards[i];
        }
        empty_squares = ~(all_black_pieces|all_white_pieces);
    }

};



int main(){
    Board b = Board();
    b.print();
    cout << endl;
    return 0;
}