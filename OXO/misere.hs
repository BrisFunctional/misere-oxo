module Main (main) where

import System( getArgs )
import List
import Random

blank = '-'
symbols = ['x', 'o']

-- compute_move inp = inp
is_playing_symbol sym = or [sym == x | x <- symbols]
count_symbols board = length $ filter is_playing_symbol board
my_symbol board = symbols !! (mod (count_symbols board) 2)

blanks = findIndices (== blank)
make_board board idx sym = (take idx board) ++ [sym] ++ (drop (idx + 1) board)

-- string_to_board :: String -> [String]
-- string_to_board board_string =
--     let dim = round $ sqrt (length board_string::Int)
--     in [board_string]

winning_board board =
    let
        rowidxs = [3 * x | x <- [0..3]]
        rows = [[board !! 0, board !! 1, board !! 2],
                [board !! 3, board !! 4, board !! 5],
                [board !! 6, board !! 7, board !! 8],
                [board !! 0, board !! 3, board !! 6],
                [board !! 1, board !! 4, board !! 7],
                [board !! 2, board !! 5, board !! 8],
                [board !! 0, board !! 4, board !! 8],
                [board !! 2, board !! 4, board !! 6]]

    in any winning_list rows

rating = [3, 2, 3, 2, 4, 2, 3, 2, 3]
best_blank possible =
    let ranks = [(rating !! x, x) | x <- possible]
    in fst $ minimum ranks

-- check_winning_board =
winning_list list =
    let
        first = list !! 0
    in (all (== first) list) && (is_playing_symbol first)

next_move :: String -> String
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
  print $ next_move board
  main
