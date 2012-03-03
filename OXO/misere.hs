-- TODO: add a way to compute the rating of the cell automatically
module Main (main) where

import List
import Random

-- TODO: use data declarations if better
type CellIdx = (Int, Int)
type Cell = (CellIdx, Symbol)
type Symbol = Char
type Board = [[Symbol]]

blank = '-'
symbols = ['x', 'o']

-- compute_move inp = inp
is_playing_symbol sym = or [sym == x | x <- symbols]
count_symbols board = length $ filter is_playing_symbol board
my_symbol board = symbols !! (mod (count_symbols board) 2)

cell :: Board -> CellIdx -> Symbol
cell board idx = board !! (fst idx) !! (snd idx)

cell_idxs dim = [(i, j) | i <- [0..(dim-1)], j <- [0..(dim-1)]]

blanks board =
  let dim = length board
  in [(i, j) | (i, j) <- cell_idxs dim, cell board (i, j) == blank]

idx_to_pos idx dim =
    (dim * (fst idx)) + (snd idx)

to_board board_string = 
    string_to_board board_string dim
    where
      dim = round $ sqrt (fromIntegral $ length board_string)
      string_to_board "" _ = []
      string_to_board board_string dim =
          take dim board_string : (string_to_board (drop dim board_string) dim)

winning_list :: [Symbol] -> Bool
winning_list list =
    let
        first = head list
    in (is_playing_symbol first) && (all (== first) list)
       
board_lines board =
    board ++ (transpose board) ++ [diag1, diag2]
    where
      max_idx = length board - 1
      diag1 = [cell board (i, i) | i <- [0..max_idx]]
      diag2 = [cell board (i, max_idx - i) | i <- [0..max_idx]]
      
winning_board :: Board -> Bool
winning_board board = any winning_list (board_lines board)

make_board board idx sym =
  (take idx board) ++ [sym] ++ (drop (idx + 1) board)
  
next_move board_st =
    let
        my_sym = my_symbol board_st
        board = to_board board_st
        possible_moves = blanks board
        next_blank = head possible_moves
        next_board = make_board board_st (idx_to_pos next_blank (length board)) my_sym
    in
      if (winning_board (to_board next_board))
       then (make_board board_st (idx_to_pos (possible_moves !! 2) (length board)) my_sym)
       else next_board

-- recursively ask for a board and output the next one
main = do
  board <- getLine
  print $ next_move board
  main
