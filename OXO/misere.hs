module Main (main) where

import System( getArgs )
import List
import Random

type CellIdx = (Int, Int)
type Symbol = Char
type Board = [[Symbol]]

blank = '-'
symbols = ['x', 'o']

-- compute_move inp = inp
is_playing_symbol sym = or [sym == x | x <- symbols]
count_symbols board = length $ filter is_playing_symbol board
my_symbol board = symbols !! (mod (count_symbols board) 2)

blanks = findIndices (== blank)
make_board board idx sym = (take idx board) ++ [sym] ++ (drop (idx + 1) board)

to_board board_string = 
    let dim = round $ sqrt (fromIntegral $ length board_string)
    in string_to_board board_string dim

string_to_board "" _ = []
string_to_board board_string dim =
    take dim board_string : (string_to_board (drop dim board_string) dim)

-- check if the line is winning
winning_list list =
    let
        first = head list
    in (is_playing_symbol first) && (all (== first) list)
       
board_lines board =
    board ++ (transpose board) ++ [diag1, diag2]
    where
      max_idx = length board - 1
      diag1 = [board !! i !! i | i <- [0..max_idx]]
      diag2 = [board !! i !! (max_idx - i) | i <- [0..max_idx]]
      
winning_board board = any winning_list (board_lines board)

rating = [3, 2, 3, 2, 4, 2, 3, 2, 3]
best_blank possible =
    let ranks = [(rating !! x, x) | x <- possible]
    in fst $ minimum ranks


next_move board =
    let
        my_sym = my_symbol board
        possible_moves = blanks board
        next_blank = possible_moves !! 0
        next_board = make_board board next_blank my_sym
    in if (winning_board next_board) then (make_board board (possible_moves !! 1) my_sym) else next_board
                                                                                               

-- recursively ask for a board and output the next one
main = do
  board <- getLine
  print $ next_move (to_board board)
  main
