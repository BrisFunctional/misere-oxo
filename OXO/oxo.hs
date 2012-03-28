#!/usr/bin/env runhaskell

-- a Misere Tic-Tac-Toe player
-- (cc) Arwyn Roberts 2012

-- game state representation:
-- a string of 9 characters from the alphabet "-OX" where '-' means a blank cell

module Main (main) where

import Data.List
import System (getArgs)
import System.Random

blank = '-'
piece = "XO"

-- which player am I? - as an index in piece
player :: [Char] -> Int
player state = length pieces `mod` length piece
             where pieces = filter (`elem` piece) state

-- who is my opponent? - also an index
opponent :: Int -> Int
opponent me = (me + 1) `mod` length piece

-- the sets of indices that define the winning/losing lines
winLines :: [[Int]]
winLines = [[0,1,2],[3,4,5],[6,7,8], -- rows
            [0,3,6],[1,4,7],[2,5,8], -- cols
            [0,4,8],[2,4,6]]         -- diags

-- extract the 8 lines from a state of the board
exLines :: [b] -> [[b]]
exLines state = map (ex_line state) winLines
               where ex_line state = map ((!!) state)

-- test whether a list of symbols are 3 of a piece
same :: [Char] -> Bool
same xs = elem xs $ map (replicate 3) piece

-- test state to see if any player has 3 in a row
lineTest :: [Char] -> Bool
lineTest state = any same (exLines state)                     

-- find the blanks
blanks :: [Char] -> [Int]
blanks = findIndices (== blank) 

-- test whether board is full
noBlanks :: [Char] -> Bool
noBlanks = null.blanks 
                                
-- construct a move by placing a piece at idx
makeMove :: [a] -> a -> Int -> [a]
makeMove state my_piece idx = (fst split) ++ [my_piece] ++ (tail $ snd split)
                               where split = splitAt idx state

-- construct a list of all available moves
newStates :: [Char] -> Char -> [[Char]]
newStates state my_piece = map (makeMove state my_piece) $ blanks state

-- mutually recursive evaluators 
-- maxValue is trying to maximise value for player
maxValue :: Int -> [Char] -> Int
maxValue me state
  | lineTest state = 1
  | noBlanks state = 0
  | otherwise = maximum $ map (minValue you) states
                where states = newStates state (piece !! me)
                      you = opponent me
                      
-- minValue is trying to minimise value for player
minValue :: Int -> [Char] -> Int
minValue me state
  | lineTest state = -1
  | noBlanks state = 0
  | otherwise = minimum $ map (maxValue you) states 
                where states = newStates state (piece !! me)
                      you = opponent me

-- return the elements of the list xs that maximise the function eval
pickMaxs :: (Ord b, Ord a) => (b -> a) -> [b] -> [b]
pickMaxs eval xs = map snd $ last $ groupBy cmp $ sort $ zip (map eval xs) xs
                   where cmp a b = (fst a) == (fst b)

-- generate the possible moves and find the best ones
minimax :: [Char] -> [[Char]]
minimax state = pickMaxs (minValue me) moves
   where moves = newStates state (piece !! me)
         me = player state
         
-- count the number of xs found in a list
count :: Eq a => a -> [a] -> Int
count x = length.filter (== x)

-- check input and then make a move
ticTacToe :: RandomGen b => [Char] -> b -> [Char]
ticTacToe state gen 
  | length state < 9 = "Too short"
  | length state > 9 = "Too long"
  | any (`notElem` blank:piece) state = "Illegal char" 
  | count 'X' state - count 'O' state `notElem` [0,1] = "Illegal board"
  | lineTest state = "Game Over: I win!" 
  | noBlanks state = "Game Over: It's a draw!"
  | otherwise = moves !! idx -- choose a move at random from among the best available
                where moves = minimax state                
                      idx = fst $ randomR (0,length moves-1) gen

main = do
  gen <- getStdGen
  args <- getArgs
  let state = head args
  putStrLn $ ticTacToe state gen
