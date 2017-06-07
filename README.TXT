------------------------------
--  TEST GENERATOR EXAMPLE  --
------------------------------

- TASK: WHAT IT DOES
The code generates a fake log file including only the following lines:

Always:
   1. Log file header (Loader)
For each job:
   2. JOB_START
   3. Progress$Tickers
   4. JOB_END
Always:
   5. Starting cleanups

These are the only lines being read by the plog.py bill calculator.

The code also calculates the reference cost of each job by multiplying
its rate=cost/hour by its the round-up duration in hours.

- FILES NEEDED:
1. Input: The input files have the format input_*.txt. Each input file
   contains as many lines as fake jobs. Each line constist of a json structure
   representing the input to the job objects in the gentest.py script. The 
   user must fill in each of the following fields:
   - Job starting time:
     a) year
     b) month
     c) day
     d) hour
     e) minu (minute)
     f) s (second)
     g) ms (millisecond)
   - Job duration in seconds:
     h) duration
   - Job rate in credits/hour:
     i) r
   - Job cost in credits:
     j) cost=0 (Initial cost = 0)
   - Job status:
     k) status= Waiting, Running or Finished (Initial Status = Waiting)

2. gentest.py: Receives a the input corresponding to each test and writes
   the corresponding output files, i.e., the fake_i.log and cost_i.txt files.
   The script "runs" each job serially in the order that is specified in the 
   input file and independently of the job's starting time.
 
3. gentest.sh: Wrapps the gentest.py file in a loop that goes over each 
   of the input_*.txt. The script sorts the fake_i.log files by time producing
   the sfake_i.log files.

4. OUTPUT: There are 3 output files per input_i.txt.
   a) fake_i.log: The unsorted by time log file. Shows the order in which the
      gentest.py script is running the jobs and should only be used for debugging.
   b) sfake_i.log: The sorted by time log file. This file is the input to the
      plog.py script
   c) cost_i.txt: Is the updated input_i.txt file. That is, the input_i.txt contains
      the job's fields before running and the cost_i.txt file contains the same fields
      after running. Therefore, it shows the job's ending time, final cost and 
      Finished status.

- RUNNING AN EXAMPLE:
The directory contains 4 example input files:
   input_1.txt: Contains 7 jobs corresponding to 7 apps. All the jobs start at the same
                time and have different durations and rates.
   input_2.txt: Is similar to input_1.txt but runs the fmtask_1D app twice, therefore,
                it runs 8 jobs. 
   input_3.txt: Contains 12 jobs corresponding to 7 apps. 11 Jobs start at the same time.
   input_4.txt: Contains 1 job that runs from 2017/12/25 00:00:00 to 2018/01/01 01:01:01.
                The purpose of this input is to check the correct changes are being made
                to the date and time. The duration of the job is:
                7*24*60*60+60*60+60+1=608461 
   
 To run the example just type: ./gentest.sh 4
 The 4 is the total number if input_*.txt
   

 
