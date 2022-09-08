"""/**
 * @author jateengandhi
 * @email 
 * @create date 2022-03-21 21:13:45
 * @modify date 2022-06-14 07:54:15
 * @desc [description]
 */"""

# This program is a guide to solve Wordle 
# using probability and elimination

# Preliminaries
import pandas as pd
import numpy as np
import os


os.chdir('C:...wordle dir') # Keep all CSV files here

# Past wordle answers
w = pd.read_csv('w.csv')

# Google's list of popular 5-letter words
g = pd.read_csv('g.csv')

# Remove past wordle answers
g_w = g[np.invert(np.isin(g['x'], w['Answer']))]

# Split words into individual letters and store in columns
g_l = g_w['x'].str.split('', expand=True)
g_l = g_l.drop([0, 6], axis=1)

# List of all possible 5-letter words
d = pd.read_csv('d.csv')

# Remove past wordle answers
d_w = d[np.invert(np.isin(d['x'], w['Answer']))]

# Split words into individual letters and store in columns
d_l = d_w['x'].str.split('', expand=True)
d_l = d_l.drop([0, 6], axis=1)


def getP(df):
    """Assumes df is a pd dataframe of words 
    split into letters and stored in columns
    Returns positional and total probability of each letter"""
    
    # Number of rows and columns of df
    r, c = df.shape

    # Count the frequency of letters in each column
    # pandas automatically does row bind. 
    # First column is all 26 letters,
    # rest of the columns have frequency of each letter in given position 
    lP = df.apply(lambda x:x.value_counts())

    # Since not all columns will have eah letter, fill NAs with 0
    lP = lP.fillna(0)

    # Add all positional frequencies to get total frequency
    lP['total'] = lP.sum(axis=1)

    # Calculate positional probabilities of a letter for each column
    for col in df:
        lP['p'+str(col)] = lP[col].apply(lambda x:x/r)

    # Total probability
    lP['p'] = lP['total']/(r*c)

    # Sort DF in descending order of 'p' (total prob) 
    # and return top 5 rows and all probability columns
    return lP.iloc[:, -(c+1):].sort_values('p', ascending = False).head()

    # return lP # Uncomment this and comment the above line in order to get entire dataframe

# Calculate probabilities and get top 5 most likely letters
gP = getP(g_l)
dP = getP(d_l)

def chkWord(word, df='w'):
    """Assumes word is a 5-letter string, and
    df is either a 'w', 'd_w', or 'g_w'.
    Returns a bool if the word is in df's column with 5 letter words"""
    if df == 'w':
        return word in w['Answer'].values
    else:
        return word in d_w['x'].values


def eliminate(col, att, fb, df):
    """Assumes col is a list of column headers of dataframe df, 
    att (attempt) and fb (feedback) are lists 
    each with 5 or fewer letters,
    df is a pd dataframe of columns with letters.

    This function eliminates rows (word options) 
    from df based off attempt and feedback.
    Returns filtered df"""

    # Create a copy of df
    elimDF = pd.DataFrame(df)
    
    # These lists will store column numbers 
    # for green, black, and yellow feedback
    gs, bs, ys = [], [], []


    for c, f in zip(col, fb):
        if f == 'g':
            gs += [c]
        elif f == 'b':
            bs += [c]
        elif f == 'y':
            ys += [c]

    # This list will be used to eliminate words (rows) 
    # with letters which had black feedback (absent from the answer)
    bys = bs + ys

    # This dictionary will store elimination info
    # Keys will be a mix of int and str
    elim = {}

    for c, f, a in zip(col, fb, att):
        # Key will be row number (int) and val will be letter (str)
        # This will be used for keeping words (rows) with the 
        # letter (val) at the position (column) indicated by key
        if f == 'g':
            elim[c] = a
        
        # Key will be row number (int) and val a list with letters (str)
        # This will be used to remove words with letters (val) 
        # at the position (key)
        elif f == 'b':
            for n in bys:
                try:
                    elim[n] += [a]
                except KeyError:
                    elim[n] = [a]
        
        # yellow ('y') feedback indicates letter not in that 
        # position but somwhere else (non 'g' position)
        elif f == 'y':
            
            # Key will be letter (str) which is present in 
            # positions other than current attempt
            # Those positions are all columns except
            # the position in current attempt
            try:
                elim[a] += [n for n in list(set(bys) ^ set([c]))]
            except KeyError:
                elim[a] = [n for n in list(set(bys) ^ set([c]))]
            
            # Key will be int and val a list with str
            # Add letter (str) in the position (int)
            # Words (rows) will be removed, similar to 'b'
            try:
                elim[c] += [a]
            except KeyError:
                elim[c] = [a]
    
    # Next two steps are for tackling 
    # double letter attempt where one of the letters 
    # is a yellow and the other is a black feedback
    elim_str = []
    for k in elim.keys():
        if isinstance(k, str):
            elim_str += [k]
        
        
    for k in elim.keys():
        if isinstance(k, int) & isinstance(elim[k], list):
            for s in elim[k]:
                if s in elim_str and k in elim[s]:
                    elim[k].remove(s)
    
    # Elimination operation
    for k in elim.keys():

        # For keys that are column numbers
        if isinstance(k, int):

            # Only for green feedback val is a str
            # Keep rows (words)
            if isinstance(elim[k], str):
              elimDF = elimDF[np.isin(elimDF[k], elim[k])]
            
            # For blacck feedback
            # Remove rows (words)
            else:
                elimDF = elimDF[np.invert(np.isin(elimDF[k], elim[k]))]
        
        # For keys that are str and val is a list for col numbers
        # Keep rows that have key in all of the possible columns
        else:
            elimDF = elimDF[elimDF[elim[k]].
                            apply(lambda x: x == k).any(axis=1)]
    
    # Filtered dataframe
    return elimDF

# First attempt
att = ['a', 'r', 'o', 's', 'e']
#  Wordle's feedback for the first attempt
fb = ['b', 'b', 'b', 'b', 'b']

cols = [1, 2, 3, 4, 5]

# Shorten the options using feedback
cur_g = eliminate(cols, att, fb, g_l)
cur_d = eliminate(cols, att, fb, d_l)

# If shortened tables have less than 10 rows,
# Check the table and pick the option with most Google search hits

# If the tables have more than 10 rows get probability and select top 5 letters
gP = getP(cur_g)
dP = getP(cur_d)

# Second attempt
att2 = ['c', 'l', 'i', 'n', 't']
fb2 = ['b', 'b', 'y', 'y', 'g']


cur_g = eliminate(cols, att2, fb2, cur_g)
cur_d = eliminate(cols, att2, fb2, cur_d)
dP = getP(cur_d)
