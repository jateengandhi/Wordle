# Wordle

This repository lists a program to solve Wordle using probability and elimination. Fo a detailed discussion on how this program works, kindly check out this YouTube playlist (https://tinyurl.com/37m6m62m). In a nutshell, the idea is to use most probable letters for a given attempt, and eliminate options based on the feedback.

Python script is fully automated which requires only the word attempt and Wordle's feedback. R script automatically calculates probabilities but requires manual code editing for elimination.

3 CSV files are also uploaded here. 
- d.CSV is 5 letter wordlist which exahusts nearly all possible 5 letter words in english language. This list is filtered from https://github.com/dwyl/english-words
- g.CSV is a 5 letter wordlist which is a filtered version of Google's list of popular words: https://github.com/first20hours/google-10000-english
- w.CSV is a list of past Wordle answers (through June 20, 2022).
