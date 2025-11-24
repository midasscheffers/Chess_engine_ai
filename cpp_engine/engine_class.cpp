
#include<iostream>
#include<vector>
#include<unordered_map>

using namespace std;



int algebraic_to_sq(string alg_sq){
    int x = alg_sq[0] - 'a';
    int y = alg_sq[1] - '0';
    return x+8*(8-y);
}




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

    unsigned long long bitboards[12]; // 0-5 white 6-11 black k,p,n,b,r,q
    unsigned long long all_black_pieces;
    unsigned long long all_white_pieces;
    unsigned long long empty_squares;
    bool is_white_turn;
    vector<vector<bool>> casteling_rights;
    vector<int> ep_sq;
    int moves_counter;
    int halfmoves_counter;
    // vector<Move> moves_made;

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
        unsigned long long one = 1;
        bitboards[p] |= (one<<sq);
        // update all_boards
        empty_squares = ~((~empty_squares) | (one<<sq));
        if (p<6){
            all_white_pieces |= (one<<sq);
        }
        else{
            all_black_pieces |= (one<<sq);
        }
    }

    
    void remove_piece(int p, int sq){
        unsigned long long one = 1;
        bitboards[p] = ~((~bitboards[p]) | (one<<sq));
        // update the all_boards
        empty_squares |= one<<sq;
        if (p<6){
            all_white_pieces = ~((~all_white_pieces) | (one<<sq));
        }
        else{
            all_black_pieces = ~((~all_black_pieces) | (one<<sq));
        }
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
            if (curr_char != '-'){
                rights[char_to_int_rights[curr_char]] = true;
            }
        }
        casteling_rights.push_back(rights);
        // ep_sq
        if (data[3] != "-"){
            ep_sq.push_back(algebraic_to_sq(data[3]));
        }
        else{
            ep_sq.push_back(-1);
        }
        // move_counters
        char mc = data[5][0];
        int imc = mc - '0';
        char hmc = data[4][0];
        int ihmc = hmc - '0';
        moves_counter = imc;
        halfmoves_counter = ihmc;

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
        cout << "cr: ";
        for (int i =0;i<4;i++){
            cout << casteling_rights.back()[i] << ", ";
        }
        cout << "m: " << moves_counter << " hm: " << halfmoves_counter;
        cout << " ep: " << ep_sq.back() << endl; 
        
    }

    void print_bitboards(){
        for (int i =0; i<12; i++){
            cout << "Bitboard: " << i << endl;
            BitBoard().print(bitboards[i]);
        }
        cout << "All White BB:" << endl;
        BitBoard().print(all_white_pieces);
        cout << "All Black BB:" << endl;
        BitBoard().print(all_black_pieces);
        cout << "Empty squares:" << endl;
        BitBoard().print(empty_squares);
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
        if (!(m.is_castle || m.is_capture || m.is_ep)){
            int piece = piece_on_sq(m.start);
            remove_piece(piece, m.start);
            set_piece(piece, m.end);
        }
        else if (m.is_capture){
            int piece = piece_on_sq(m.start);
            int enemy_piece = piece_on_sq(m.end);
            remove_piece(piece, m.start);
            remove_piece(enemy_piece, m.end);
            set_piece(piece, m.end);
        }
        else if (m.is_ep){
            
        }
        else if (m.is_castle){
            
        }
        // castle rights logic

        // ep square logic
        if (m.is_double_pawn_move){
            int d = (m.end-m.start < 0) ? -8 : 8;
            ep_sq.push_back(m.end+d);
        }
        else{
            ep_sq.push_back(-1);
        }
    }

};



int main(){
    Board b = Board();
    // b.print_bitboards();
    b.print();
    // b.make_move(Move(0, 16));
    // b.print();
    // b.print_bitboards();
    return 0;
}