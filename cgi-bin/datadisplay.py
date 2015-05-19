#!/usr/bin/env python

print 'Content-type: text/html\r\n\r\n'

import cgitb; cgitb.enable()

import psycopg2

conn=psycopg2.connect(database="intersective", user="postgres", password="010305")
                   
cur=conn.cursor() 

import cgi
import sys

form=cgi.FieldStorage()

ids=form.getvalue('id')
tempscore=form.getvalue('post')
score=float(tempscore)
##############test sql
##select assess_assessments.id, assess_answer_analysis_results.score, core_users.name, assess_assessments.name, assess_answer_analysis_keywords.keyword, assess_answer_analysis_keywords.sentiment, assess_answer_analysis_keywords.score
##from  public.assess_assessments, public.assess_assessment_submissions, public.assess_assessment_submission_answers, public.assess_answer_analysis_results, public.assess_answer_analysis_keywords, public.core_users
##where assess_answer_analysis_results.assessment_submission_answer_id = assess_assessment_submission_answers.id
##and  assess_assessment_submissions.assessment_id = assess_assessments.id
##and  assess_answer_analysis_results.submitter_id = core_users.id
##and  assess_answer_analysis_results.assessment_submission_answer_id = assess_answer_analysis_keywords.assessment_submission_answer_id
##and  assess_assessment_submissions.id = assess_assessment_submission_answers.assessment_submission_id


sql ="select assess_assessments.id, assess_answer_analysis_results.score, core_users.name, assess_assessments.name, assess_answer_analysis_results.submitter_id"
sql = sql+" from  public.assess_assessments, public.assess_assessment_submissions, public.assess_assessment_submission_answers, public.assess_answer_analysis_results, public.core_users"
sql = sql+" where assess_answer_analysis_results.assessment_submission_answer_id = assess_assessment_submission_answers.id"
sql = sql+"  and  assess_assessment_submissions.assessment_id = assess_assessments.id"
sql = sql+"  and  assess_answer_analysis_results.submitter_id = core_users.id"
sql = sql+"  and  assess_assessment_submissions.id = assess_assessment_submission_answers.assessment_submission_id"
sql = sql+" and assess_assessments.id=%s" %ids
#sql = sql+" and assess_answer_analysis_results.score=%s;" %score

cur.execute(sql)

rows=cur.fetchall()

#print (type(score))


print """
<html>
  <head>
    <title>The list of submitters</title>
    <style type="text/css">
body {
  padding-left: 11em;
  font-family: Georgia, "Times New Roman",
        Times, serif;
  color: purple;
  background-color: #d8da3d }
ul.navbar {
  list-style-type: none;
  padding: 0;
  margin: 0;
  position: absolute;
  top: 2em;
  left: 1em;
  width: 9em }
h1 {
  font-family: Helvetica, Geneva, Arial,
        SunSans-Regular, sans-serif }
ul.navbar li {
  background: white;
  margin: 0.5em 0;
  padding: 0.3em;
  border-right: 1em solid black }
ul.navbar a {
  text-decoration: none }
a:link {
  color: blue }
a:visited {
  color: purple }
address {
  margin-top: 1em;
  padding-top: 1em;
  border-top: thin dotted }
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
th, td {
    padding: 15px;
} 
    </style>    
  </head>  
  <body>
    <h1>The list of submitters</h1>
"""
#print ' <p><a style="color:red;" href="datadisplay.py">assessment %s </a></p>' %ids
#print ' <p><a style="color:red;" href="datadisplay.py">assessment %s </a></p>' %score
for row in rows:
     partition=round (row[1], 1)
     if partition==score:
          temp=(ids, partition, row[4], row[2])
          print ' <p><a style="color:red;" href="keyworddisplay.py?id=%s&post=%s&nameid=%s">Name of submitter: %s </a></p>' % temp
          print ' <p><b>sentiment score: %s </b></p>' % row[1]
          print ' <p><b>assessment name: %s </b></p> <hr />' % row[3]
         #print '%s' %partition

conn.close
print """    
  </body>
</html>  
"""
