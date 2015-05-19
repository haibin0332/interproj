from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import datetime
import psycopg2
import sys


def figure():
    
        while True:
            
         print_options=raw_input('Would you like to generate the Figures, enter yes/no: ')

         if  print_options == 'yes':

              try:
                      
                   conn=psycopg2.connect(database="intersective", user="postgres", password="010305")
                   
              except Exception as e:
                    print (e)
# use a cursor to prepare for executing the sql. 
              cur=conn.cursor()                 
            
              try:
#plot the figures based on sentiment or score in table assess_answer_analysis_results   
                 cur.execute("SELECT \
  assess_assessments.id, \
  assess_answer_analysis_results.sentiment, \
  assess_answer_analysis_results.score, \
  assess_answer_analysis_results.assessment_question_id, \
  assess_answer_analysis_results.assessment_submission_id, \
  assess_answer_analysis_results.submitter_id \
FROM \
  public.assess_answer_analysis_results, \
  public.assess_assessments, \
  public.assess_assessment_submissions,\
  public.assess_assessment_submission_answers \
WHERE \
  assess_answer_analysis_results.assessment_submission_answer_id = assess_assessment_submission_answers.id AND \
  assess_assessment_submissions.assessment_id = assess_assessments.id AND \
  assess_assessment_submissions.id = assess_assessment_submission_answers.assessment_submission_id \
ORDER BY \
   assess_assessments.id \
")

              except Exception as e:
                   print (e)

              rows=cur.fetchall()
              assessments={}          
 #             scores={}            ##the scores for partition
 # plot the figure, the following forms are used to store the data
 # dict[submission.id][total number for this submission][total score for this submission][sub-partitions (-1, -0.9, -0.8, etc)]
 # [index for a sub-partition][content]
 
              
              total_number_group=0 ##total number for a submission
              total_score=0        ##total score for a submission
              curr_partition_number=0  ##total number for a partition
              index=0              ##the index for each item/record
              #k=0
              for row in rows:                     
                   #print(row[0])
                  sub_partition=round (row[2], 1)
                  
                  if row[0] not in assessments:
##initialization                

                     total_number_group=1
                     
                     total_score=round (row[2], 1)

                     curr_partition_number=1

                     index=1
                     
                     assessments[row[0]]={}
                     
                     assessments[row[0]][total_number_group]={}

                     assessments[row[0]][total_number_group][total_score]={}
                     
                     assessments[row[0]][total_number_group][total_score][sub_partition]={}
                         
                     assessments[row[0]][total_number_group][total_score][sub_partition][curr_partition_number]={}

                     assessments[row[0]][total_number_group][total_score][sub_partition][curr_partition_number][index]={}

                     assessments[row[0]][total_number_group][total_score][sub_partition][curr_partition_number][index]['submitter']=row[5]

                     assessments[row[0]][total_number_group][total_score][sub_partition][curr_partition_number][index]['sentiment']=row[1]

                     assessments[row[0]][total_number_group][total_score][sub_partition][curr_partition_number][index]['score']=row[2]
                     
                     
                  else:
## update record                          

                     #total_number_group_new=assessments[row[0]].keys()[0]+1
                     temp1=assessments[row[0]].keys()[0]+1
                     #assessments[row[0]][total_number_group_new]=assessments[row[0]][total_number_group]
                     temp2=assessments[row[0]][total_number_group]
                     del assessments[row[0]][total_number_group]
                     total_number_group=temp1
                     assessments[row[0]][total_number_group]={}
                     assessments[row[0]][total_number_group]=temp2
                     temp2={} 
                     
                     #total_score_new=assessments[row[0]][total_number_group].keys()[0]+round (row[2], 1)
                     temp3=assessments[row[0]][total_number_group].keys()[0] + (round (row[2], 1))
                     temp4=assessments[row[0]][total_number_group][total_score]
                     del assessments[row[0]][total_number_group][total_score]
                     total_score=temp3
                     assessments[row[0]][total_number_group][total_score]={}
                     assessments[row[0]][total_number_group][total_score]=temp4
                     temp4={}


                     if  sub_partition not in assessments[row[0]][total_number_group][total_score].keys():

                         curr_partition_number=1
                         
                         index=1
                         
                         assessments[row[0]][total_number_group][total_score][sub_partition]={}
                         
                         assessments[row[0]][total_number_group][total_score][sub_partition][curr_partition_number]={}

                         assessments[row[0]][total_number_group][total_score][sub_partition][curr_partition_number][index]={}

                         assessments[row[0]][total_number_group][total_score][sub_partition][curr_partition_number][index]['submitter']=row[5]

                         assessments[row[0]][total_number_group][total_score][sub_partition][curr_partition_number][index]['sentiment']=row[1]

                         assessments[row[0]][total_number_group][total_score][sub_partition][curr_partition_number][index]['score']=row[2]

                         #print (assessments[row[0]][total_number_group][total_score][sub_partition])
                     
                     else:

                         #new_curr_partition_number=assessments[row[0]][total_number_group_new][total_score_new][sub_partition].keys()[0]+1

                         temp5=assessments[row[0]][total_number_group][total_score][sub_partition].keys()[0]
                         temp5_1=assessments[row[0]][total_number_group][total_score][sub_partition].keys()[0]+1
                         
                         
                         #print (assessments[row[0]][total_number_group][total_score][sub_partition])
                         #print (assessments[row[0]][total_number_group][total_score][sub_partition][temp5].keys())
                         
                         temp6=assessments[row[0]][total_number_group][total_score][sub_partition][temp5]
                        
                         #print (assessments[row[0]][total_number_group][total_score][sub_partition][curr_partition_number])

                         temp7=len(assessments[row[0]][total_number_group][total_score][sub_partition][temp5].keys())+1
                         
                         del assessments[row[0]][total_number_group][total_score][sub_partition][temp5]

                         curr_partition_number=temp5_1
                         
                         assessments[row[0]][total_number_group][total_score][sub_partition][curr_partition_number]={}
                         
                         assessments[row[0]][total_number_group][total_score][sub_partition][curr_partition_number]=temp6

                         index=temp7
                         
                         assessments[row[0]][total_number_group][total_score][sub_partition][curr_partition_number][index]={}

                         assessments[row[0]][total_number_group][total_score][sub_partition][curr_partition_number][index]['submitter']=row[5]

                         assessments[row[0]][total_number_group][total_score][sub_partition][curr_partition_number][index]['sentiment']=row[1]

                         assessments[row[0]][total_number_group][total_score][sub_partition][curr_partition_number][index]['score']=row[2]

                         temp6={}

                         #print (assessments[row[0]][total_number_group][total_score])
              #print ('here')
              
              for i in assessments:
                      
                         assessments_id=i 
                         total_number_group=assessments[assessments_id].keys()[0]
                         total_score=assessments[assessments_id][total_number_group].keys()[0]
                         average=round ((total_score/total_number_group), 2)
                         
                         temp_sub_partitions=sorted(assessments[assessments_id][total_number_group][total_score].keys())

                         temp_curr_partition_number=[]

                         for j in temp_sub_partitions:
                         
                                add_curr_partition_number=assessments[assessments_id][total_number_group][total_score][j].keys()[0]

                                temp_curr_partition_number.append(add_curr_partition_number)

######################################################### the following part is just for plotting the figures##################################                                

                         x_axis = tuple(temp_sub_partitions)
                         y_axis = tuple(temp_curr_partition_number)

                         average_x = average
                         #average_y = total_number_group
                         ylim=1.5*max(y_axis)
                         ylim1=1.2*max(y_axis)
                         
                         fig, ax = plt.subplots()  
 
                         bar_width = 0.05
                         
  
                         opacity = 1 
                         rects1 = plt.bar(x_axis, y_axis, bar_width,alpha=opacity, color='b',label='partitions')  
                         #rects2 = plt.bar(average_x, average_y, bar_width, alpha=opacity,color='r',label='average')

                         plt.axvline(average_x, linewidth=4, color='black',linestyle="--")

                         plt.annotate('average',xy=(average_x, ylim1), xytext=(average_x, ylim1))
  
                         plt.xlabel('Scores')  
                         plt.ylabel('Number of Reflection')  
                         plt.title('Scores Distribution of assessment %s' % assessments_id)  
 
                         plt.ylim(0,ylim) 
                         plt.xlim(-1,1)
                         plt.legend()  
  
                         plt.tight_layout()  
                         #plt.show()
                         
                         plt.savefig('/home/hadoop/Downloads/figures/%s.jpg' % assessments_id)
 
                         #pass   #if pass, the function will not return any results 
########################################################################################################                                                

              return assessments
              break
            
         elif print_options == 'no':            
               break    
         else:
               print('Error input, please reenter.')
