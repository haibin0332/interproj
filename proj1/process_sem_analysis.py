#!/usr/bin/env python

#	Copyright 2015 Intersective code by Haibin Zhang
#
#
# Semantic analysis of reflection for intersective.
# The core function or the analysis result is based on AlchemyAPI. 
# This function can automatically execute semantic analysis.
# In general, the function connects table assess_assessment_submission_answers of intersetive database
# Basically, assessment_question_id have to check first in order to know the type of answer.
# As mentioned, the answer text may contain some unuseful contents
# Initially, the function does not give the judagement but simply tests some samples.


from __future__ import print_function
from alchemyapi import AlchemyAPI
import semAnalysis
import plotFigure
import time
import datetime
import psycopg2
import json
import sys
#sys.path.append('/var/www/cgi-bin')
#import displayFigure
#import test


if __name__ == '__main__':

 #while True:

  print('')
  print('#####################################')
  print('#   Processing Sentiment Analysis   #')
  print('#####################################')
  print('')
   
#  output_options=raw_input('Please enter ALL to view the analysis results: ')

########################################################################################################output_options
  
 # if output_options == 'all':
    
# connect database, get all the reflection results and processing analysis
  try:
          conn=psycopg2.connect(database="intersective", user="postgres", password="010305")
  except Exception as e:
          print (e)
# use a cursor to prepare for executing the sql. 
  cur=conn.cursor()
  
  try:
            cur.execute("SELECT * From assess_answer_analysis_results")
            #cur.execute("SELECT * From results")
            
            while True: 
                   create_options=raw_input(
                  'Would you like to continue processing sentiment analysis, enter yes/no: ')
                   if create_options == 'yes':
                      #delete content in the table, and execute analysis
                      #cur.execute("TRUNCATE TABLE assess_answer_analysis_results, assess_answer_analysis_keywords")
                     
###############################the following function is for sentiment analysis##########################################
#record the execution time
                     
                      starttime = datetime.datetime.now() 
                      semAnalysis.createAnalysis()
                      endtime=datetime.datetime.now()
                      interval=(endtime-starttime).seconds
                      print (interval)                  
                      conn.close()
                     
###############################the following function is for plotting results##############################################
                      assessments={}
                      assessments=plotFigure.figure()

###############################the following function is for displaying results############################################                       
                      #displayFigure.displayfigure(assessments)
                      #test.displayfigure(assessments)
                      print ('Finish Analysing')
                      print ('')
                      break
                   elif create_options == 'no':
                      break
            
                   else:
                      print('Error input, please reenter.')
            
  except Exception as e:
    
###############################create the table, and execute analysis######################################################
                    conn.close()
                    try:
                         conn=psycopg2.connect(database="intersective", user="postgres", password="010305")
                    except Exception as e:
                         print (e)
# use a cursor to prepare for executing the sql. 
                    cur=conn.cursor()
                    
                    cur.execute("CREATE TABLE assess_answer_analysis_results\
( \
  id serial NOT NULL, \
  assessment_submission_answer_id integer NOT NULL, \
  submitter_id integer, \
  assessment_submission_id integer, \
  assessment_question_id integer, \
  sentiment character varying, \
  score numeric(15,8), \
  CONSTRAINT assess_answer_analysis_results_pkey PRIMARY KEY (id) \
) \
")
                    time.sleep(5)
                    cur.execute("CREATE TABLE assess_answer_analysis_keywords\
(\
  id serial NOT NULL,\
  assessment_submission_answer_id integer NOT NULL,\
  keyword character varying,\
  relevence numeric(10,8),\
  sentiment character varying,\
  score numeric(15,8),\
  CONSTRAINT assess_answer_analysis_keywords_pkey PRIMARY KEY (id) \
)\
")
                 
                    semAnalysis.createAnalysis()
                    assessments=plotFigure.figure()
                    
                    print ('Finish Analysing')
                    print ('')
                    
                    conn.close()

   #     break       
    
######################################################################################################// output_options
        
  #else:
 
   #      print('Error input, please reenter.')
         
