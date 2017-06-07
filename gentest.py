import sys
import math
import datetime
import json

#######################################
## MANUAL INPUT                      ##
#######################################
# Number of jobs
Njobs=int(sys.argv[1])
# ProgressTicker printing period in seconds
tickerTime=int(sys.argv[2])
# Opening input file
i=open(sys.argv[3],'r')
# Initializing cost file
c=open(sys.argv[4],'w')
# Initializing log file
f=open(sys.argv[5],'w')
# Arguments for the log file header
arguments="[-runid, run006, -logfile, /share/mike/swift/lab/pw/billing2/swiftest/run006/swift.log, fm3.swift]"
date=datetime.date(2017,6,5)
time=datetime.time(0,0,0)
ms=775 # Micro second
f.write("%s %s,%s-0500 INFO  Loader ARGUMENTS %s\n" %(date,time,ms,arguments))
#######################################
#######################################

#######################################
## CLASS JOB DEFINITION              ##
#######################################
# Contains all the attributes and actions related to a job
class job():
    def _init_(self):
        self.name='name' # Name of the job
        # Current date and time of the job
        self.year=0
        self.month=0
        self.day=0
        self.hour=0
        self.minu=0
        self.s=0
        self.ms=775

        self.status="Waiting" # Status of the job: Waiting, Running or Finished
        self.rate=0 # Cost per hour run of the job
        self.duration=0 # Job running time
        self.cost=0 # Total Job Cost
    def JOB_START(self,f): # A job can start
       # Reports the beginng of the job to the log file "f"
       # 1<=r+1<=self.runs is the current run number of the job
       date=datetime.date(self.year,self.month,self.day)
       time=datetime.time(self.hour,self.minu,self.s)
       f.write("%s %s,%s-0500 DEBUG swift JOB_START jobid=%s\n" %(date,time,self.ms,self.name))
       self.status="Running"
    def ProgressTicker(self,f): # A job can report progress
       date=datetime.date(self.year,self.month,self.day)
       time=datetime.time(self.hour,self.minu,self.s)
       # Prints the Progress Tickers to the log file "f"
       f.write("%s %s,%s-0500 INFO RuntimeStats$ProgressTicker\n" %(date,time,self.ms))
    def JOB_END(self,f): # A job can end
       date=datetime.date(self.year,self.month,self.day)
       time=datetime.time(self.hour,self.minu,self.s)
       # Reports the ending of the job to the log file "f"
       # 1<=r+1<=self.runs is the current run number of the job
       f.write("%s %s,%s-0500 DEBUG swift JOB_END jobid=%s\n" %(date,time,self.ms,self.name))
       self.status="Finished"
    def updateTime(self,time2add): # A job can update its current time
       # Updates the current date and time of the job
       timeInSec=self.hour*60*60+self.minu*60+self.s+time2add
       self.hour=int(timeInSec/(60*60))
       left=timeInSec%(60*60)
       self.minu=int(left/60)
       left=left%60
       self.s=left
       # Check if hours need to be converted to date
       while self.hour>=24:
          self.hour=self.hour-24
          # Check if months need an update
          if self.day==28:
            if self.month==2: # February
              self.month=3
              self.day=1
            else:
              self.day=self.day+1
          elif self.day==30:
            if self.month in [11,4,6,9]: # November, April, June, September
              self.month=self.month+1
              self.day=1
            else:
              self.day=self.day+1
          elif self.day==31:
            if self.month in [1,3,5,7,8,10]: # Rest of months except December
              self.month=self.month+1
              self.day=1
            else: # Happy new year!
              self.month=1
              self.day=1
              self.year=self.year+1
          else:
              self.day=self.day+1


    def saveCost(self): # A job can calculate and save its cost
       hours=int(self.duration/(60*60))
       self.cost=hours*self.rate
       left=self.duration%(60*60)
       if left>0:
          self.cost=self.cost+self.rate
############################################################
############################################################

############################################################
## INITIALIZING LIST OF JOBS FROM INPUT FILE              ##
############################################################
jobList=[job() for j in range(Njobs)]
j=0;
for line in i:
   jobList[j].__dict__= json.loads(line)
   j=j+1

############################################################
## CREATING UNSORTED LOG FILE                             ##
############################################################
for j in range(Njobs):
   jobList[j].JOB_START(f)
   Nticks=int(jobList[j].duration/tickerTime)
   leftTime=jobList[j].duration%tickerTime
   for tick in range(Nticks):
      jobList[j].updateTime(tickerTime)
      jobList[j].ProgressTicker(f)
   jobList[j].updateTime(leftTime)
   jobList[j].JOB_END(f)
   if j==(Njobs-1):
      date=datetime.date(jobList[j].year,jobList[j].month,jobList[j].day)
      time=datetime.time(jobList[j].hour,jobList[j].minu,jobList[j].s)
      f.write("%s %s,%s-0500 DEBUG swift Starting cleanups" %(date,time,jobList[j].ms))
   jobList[j].saveCost()
   json.dump(jobList[j].__dict__,c)
   c.write('\n')

