from __future__ import print_function
from alchemyapi import AlchemyAPI
import time
import psycopg2
import json
import sys

def createAnalysis():
        #print('hree')
        try:
          conn=psycopg2.connect(database="intersective", user="postgres", password="010305")
        except Exception as e:
          print (e)
# use a cursor to prepare for executing the sql. 
        cur=conn.cursor()

### select raw all ids information with reflection
        try:
              cur.execute("\
  SELECT \
  assess_assessment_submissions.submitter_id, \
  assess_assessment_questions.id, \
  assess_assessment_submissions.id \
  FROM \
  public.assess_assessment_submissions, \
  public.assess_assessments, \
  public.assess_assessment_questions \
  WHERE \
  assess_assessments.id = assess_assessment_submissions.assessment_id AND \
  assess_assessments.id = assess_assessment_questions.assessment_id AND \
  assess_assessments.assessment_type='reflection' AND \
  assess_assessment_questions.question_type = 'text'")
        except Exception as e:
               print (e)

        rows=cur.fetchall() # rows contains all the submitter_id, question.id, submission.id
        #print (rows[1])
        #print (rows[2])
        ##
#### select the unique id (assessment_submission_answer_id) for comparing whether corresponding
#### reflection has already been processed, since there are only less than 400 reflection can be
#### processed one day               
        
        try:
                cur.execute("SELECT assessment_submission_answer_id From assess_answer_analysis_results")
                temp_result_ids=cur.fetchall() ##if not in processed_result_ids, then it will continue processing
                processed_result_ids =[]
                
                cur.execute("SELECT distinct assessment_submission_answer_id From assess_answer_analysis_keywords order by assessment_submission_answer_id")
                temp_keyword_ids=cur.fetchall() ##if not in processed_keyword_ids, then it will continue processing
                processed_keyword_ids =[]
                if len (temp_result_ids): ## if processed_result_ids and processed_keyword_ids is not null
                        
                     for j in temp_result_ids:
                            add_answer_ids=j[0]   
                            processed_result_ids.append(add_answer_ids)
                            
                     for j in temp_keyword_ids:
                             
                            add_answer_ids=j[0]   
                            processed_keyword_ids.append(add_answer_ids)
                            
                else:
###reset the cursor                        
                     cur=conn.cursor()   
                     pass
                             
        except Exception as e:
                print (e)
        
        count1=0
        count2=0
        for row in rows:

            para_rows = (row[1], row[2]) #
            #print (para_rows)
        # the comments correspond to submission_id and question_id will be selected
        # note that: as the para are all varibles, the following forms are needed 
            try:                    
               cur.execute("\
  SELECT comment, id \
  FROM assess_assessment_submission_answers \
  WHERE assessment_question_id=%s AND assessment_submission_id=%s", para_rows)
            except Exception as e:
                   print (e)

#######try first as (ids) obtained may be not in answer table
#######fetchone()[1] is id, fetchone()[0] is comment                   
            try: 
                 rows1=cur.fetchone()
#######get rid of some invalid inputs
                 #print (rows1[0])
                 #print (rows1[1])

                 if rows1[1] not in processed_result_ids:

                       if len(rows1[0]) < 30:
                                   pass
                       else:
##delete space/enter/blank lines
                     #temprow=rows1[0].split()
                     #demo_text="".join(temprow)
                     #demo_text=rows1[0].strip()
##the following form works                         
                             demo_text=rows1[0].replace("\r\n", " ")
                             #print (demo_text)
                             #print ('')
                             count1=count1+1
                             print(count1)                   

                             
                             alchemyapi = AlchemyAPI()    
             #################################################################################
             #sentiment analysis, and then store the results in assess_answer_analysis_results   
                 
                             response = alchemyapi.sentiment('text', demo_text)
                     #time.sleep(2)
                             if response['status'] == 'OK':
            
                                  if 'score' in response['docSentiment']:
                                         senti_text=response['docSentiment']['type']
                                         senti_score=response['docSentiment']['score']
                                         try:
                                                 cur.execute ("INSERT INTO assess_answer_analysis_results \
                                            (assessment_submission_answer_id, submitter_id, assessment_question_id, assessment_submission_id, sentiment, score) \
                                            VALUES (%s, %s, %s, %s, %s, %s)", (rows1[1], row[0], row[1], row[2], senti_text, senti_score))


                                         except Exception as e:
                                                 print (e)
                                         conn.commit()
                                  else:
                                         senti_text=response['docSentiment']['type']
                                         try:

                                                  cur.execute ("INSERT INTO assess_answer_analysis_results \
                                            (assessment_submission_answer_id, submitter_id, assessment_question_id, assessment_submission_id, sentiment) \
                                            VALUES (%s, %s, %s, %s, %s)", (rows1[1], row[0], row[1], row[2], senti_text))

                                         except Exception as e:
                                                 print (e)
                                      
                                         conn.commit()
                             else:

                                  print('Error in sentiment analysis call: ', response['statusInfo'])
                   
                                                                           
                 else:
                        pass

                 if rows1[1] not in processed_keyword_ids:

                       if len(rows1[0]) < 30:
                                   pass
                       else:
##delete space/enter/blank lines
                     #temprow=rows1[0].split()
                     #demo_text="".join(temprow)
                     #demo_text=rows1[0].strip()
##the following form works                         
                             demo_text=rows1[0].replace("\r\n", " ")
                             #print (demo_text)
                             #print ('')
                             count2=count2+1
                             print(count2)

                             alchemyapi = AlchemyAPI()
                             
             ###############################################################################
             #keywords extraction, and then store the data in assess_answer_analysis_keywords

                             response = alchemyapi.keywords('text', demo_text, {'sentiment': 1})               
                     #time.sleep(2)
                             if response['status'] == 'OK':
                 
                                     for keyword in response['keywords']:

                                          if 'score' in keyword['sentiment']:
                         
                                                  senti_keyword=keyword['text'].encode('utf-8')
                                                  senti_relevance=keyword['relevance']
                                                  senti_text=keyword['sentiment']['type']
                                                  senti_score=keyword['sentiment']['score']

                                                  cur.execute ("INSERT INTO assess_answer_analysis_keywords \
                                                (assessment_submission_answer_id, keyword, relevence, sentiment, score) \
                                                VALUES (%s, %s, %s, %s, %s)", (rows1[1], senti_keyword, senti_relevance, senti_text, senti_score))
                                                  conn.commit()
                                   #print ('hree')
                                   
                                          else:  
                         
                                                  senti_keyword=keyword['text'].encode('utf-8') 
                                                  senti_relevance=keyword['relevance']
                                                  senti_text=keyword['sentiment']['type']
                                                  cur.execute ("INSERT INTO assess_answer_analysis_keywords \
                                                (assessment_submission_answer_id, keyword, relevence, sentiment)\
                                                VALUES (%s, %s, %s, %s)", (rows1[1], senti_keyword, senti_relevance, senti_text))
                                                  conn.commit()
                                   #print ('hree')
                                   
                             else:
                                   print('Error in keyword extaction call: ', response['statusInfo'])                                         
##                         
                 else:
                         pass    

#close database
   #     conn.close()
        
            except Exception:
                 pass
