Module Name: Rule based Chunking
Name: Havish Chennamaraj (201201131) & Maripi Pradeep (201201108)


1- Requirements:
----------------
 Operating System               :       LINUX (tested on >= Fedora-19 , >= Ubuntu 10.04)

 Compiler/Interpreter/Librarie(s):      g++ / Perl / Java / Python

2- Directory Structure:
-----------------------

201201131
├── code
│   ├── bin
│   │   ├── compile.sh
│   │   ├── english.sh
│   │   ├── hindi.sh
│   │   └── installib.sh
│   ├── lib
│   └── src
│       ├── chunking_english.py
│       ├── chunking_hindi.py
│       ├── chunking.py
│       ├── English_Test_Chunking.txt
│       ├── engrules.txt
│       ├── eng.txt
│       ├── hinrules.txt
│       ├── Test
│       │   ├── English
│       │   │   └── Chunking
│       │   │       └── English_Test_Chunking.txt
│       │   └── Hindi
│       │       └── Chunking
│       │           └── Hindi_Chunking_Test.txt
│       └── Train
│           ├── English
│           │   └── Chunking
│           │       └── English_Chunking_train.txt
│           └── Hindi
│               └── Chunking
│                   └── Hindi_Chunking_Train.txt
├── README.txt
├── Report
│   └── Report.docx
└── Results
    ├── english.out
    ├── hindi.out
    └── kannada.out

16 directories, 20 files
                
                      
(FOLLOW THIS DIRECTORY STRUCTURE ONLY, recreate your own tree at last)


3- How to run
---------------
   ---> bin - (bin folder contains 3 shell scripts (.sh files). The description of the following .sh files are given below.)

        ---> sh installib.sh 
			If you are using any external libraries or libraries which are not included in the standard JAVA or Python libraries, this script installs the required 				libraries, for no such libraries, this file should be left blank (the libraries should be included in the 'lib' folder)

        ---> sh compile.sh 
			This file should contain the commands to compile your program. For Java, this script should contain 'javac program_name.java' for creating the class files, cc/			gcc for C. For Python, this script should be left blank.

        ---> sh english.sh Chunking on English test data
        	 sh hindi.sh Chunking on Hindi test data
             
			This should contain the commands to run your programs
				For Java, this should contain 'java program_name input_file' (the input_file is the file to be tagged)
				For Python, this file should contain 'python program_name.py input_file'
				Make sure this shell script only has one input argument.
				#####The output of the program should be displayed on the terminal#####
				If you are using two languages for implementing the viterbi, the corresponding .sh files should be filled to run the program, one language which is not chosen should be left blank.
   
   ---> src - 
	
	This folder contains all your programs to be run, this also contains the training model as well as the input files used for training
   
   ---> lib 
	
	This folder contains all the external libraries which your programs are using. If you are not using any custom libraries, only using standard libraries of Java and Python, 	this folder should be left blank.


4- NOTE :
--------------

	Please Make sure your code will run only throw run.sh and from anywhere in the terminal. Use relative paths for running the programs, do not use absolute paths.



