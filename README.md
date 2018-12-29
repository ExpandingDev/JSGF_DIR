# JSGF_DIR
The ```ls``` or ```dir``` command for the Java Speech Grammar Format (JSGF).  
This script will generarte a JSGF grammar file that contains a list of files and directory names of the targeted directoryu.  
Filenames and directory names are converted/processed to be more pronouncable (see pronunciation processing below).

## Pronunciation Processing
When listing filenames and directory names for use with speech recognition, many replacements must be made for better user friendliness.  
For example, the targeted direcotry contains: ```test.zip FinalDraft1.docx another_test.txt```  
When navigating the directory with voice commands, the user will not want to spell out every letter ("T E S T DOT Z I P").  
Rather it would be easier to say "test dot zip". The first type of substitution that the script makes is replacing "." with " dot ".  
The other file, ```FindalDraft1.docx`` has 3 issues that speech recognition software will have trouble with:  
1) "FinalDraft" should be pronunciated as two words ("Final Draft")
2) The ```1``` is usually not produced by speech recognition software. Instead speech recognition softweare will usually produce "one".  
3) The ```docx``` is pronounced "doc X" and not "docs"  
