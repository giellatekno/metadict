# OCR cleanup
This folder contains scripts used when a dictionary has been OCR-read and you want to clean up the mistakes and format the textfile for use in the metadictionary. The first step in this process is to evaluate if the OCR is good. If it is very poor, then it could be more efficient to try to create a better model. Otherwise it can be quicker to just try to find and fix mistakes with regex. Once all the most obvious mistakes have been corrected, the verify_text.py script can be used to find mistakes that you may have missed. Once you think you have removed all mistakes, it is good to format the textfile so that each line corresponds to one dictionary entry. Then you can use the alphabetic_check.py script to see if the first word in each line is in alphabetical order. If not, it probably means one entry is split into multiple lines. 


## verify_text.py
Takes a textfile and tries to find misspelt words. Uses HFST to check if a word in a given language is recognized. The HFSTs for the languages you are checking must be compiled. By default it uses the nob and sme HFSTs, but this can be changed with the arguments `-l1` and `-l2`. If a word is not recognized by either hfst, it is added to a list. The list contains the unrecognized word, what line it is found on, and the full line in question. Finally, the list is written to a \[filname\]-mistakes.txt file. If a textfile contains many latin words, the `--latin` argument will use the latin.txt file to disregard at least most of the latin words.


## alphabetic_check.py
Takes a textfile and compares the first word of every line to see if any two lines following each other are not in alphabetical order. Prints every pair of non-alphabetical lines with the line numbers.