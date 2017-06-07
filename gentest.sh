#!/bin/bash

rm cost_*.txt
rm fake_*.log
rm sfake_*.log

# Number of tests
Ntests=$1
for test in $(seq 1 $Ntests)
do
   echo "Test: $test"
   # Name of the file with the json formatted input
   inputfile="input_$test.txt"
   # Number of jobs = lines in input file
   Njobs=$(wc -l < $inputfile)
   # Progress Ticker period in swift
   tickerTime=20
   # Name of the json output files with the correct cost of each job
   costfile="cost_$test.txt"
   # Name of the unsorted log file
   logfile="fake_$test.log"   
   # Python code to produce the unsorted fake.log file
   python3.4 gentest.py $Njobs $tickerTime $inputfile $costfile $logfile
   # Sorting fake.log file to produce sfake.log which is the input of the plog.py code
   n=$(wc -l < $logfile)
   head -1 $logfile > "sfake_$test.log"
   tail -$n $logfile | sort -n -t"/" -k1 -k2 -k3 -k4 -k5 -k6 >> "sfake_$test.log"
done
