#!/usr/bin/env python

print 'Content-type: text/html\r\n\r\n'

import cgitb; cgitb.enable()

import psycopg2

conn=psycopg2.connect(database="intersective", user="postgres", password="010305")
                   
cur=conn.cursor() 


import cgi
import sys

form=cgi.FieldStorage()

ids=form.getvalue('post')

sql ="select assess_assessments.id, assess_answer_analysis_results.score"
sql = sql+" from  public.assess_assessments, public.assess_assessment_submissions, public.assess_assessment_submission_answers, public.assess_answer_analysis_results"
sql = sql+" where assess_answer_analysis_results.assessment_submission_answer_id = assess_assessment_submission_answers.id"
sql = sql+"  and  assess_assessment_submissions.assessment_id = assess_assessments.id"
sql = sql+"  and  assess_assessment_submissions.id = assess_assessment_submission_answers.assessment_submission_id"
sql = sql+" and assess_assessments.id=%s;" %ids

cur.execute(sql)

rows=cur.fetchall()

partitions=[]

for row in rows:
    
    sub_partition=round (row[1], 1)
    if sub_partition not in partitions:         
                    partitions.append(sub_partition)


partitions.sort()
partitions.reverse()

print """
<html>
  <head>
    <title>Figure display</title>
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
    <h1>Figure</h1>
"""

data_uri = open('/home/hadoop/Downloads/figures/%s.jpg' %ids, 'rb').read().encode('base64').replace('\n', '') 
img_tag = '<img src="data:image/jpeg;base64,{0}" alt=" " height="350" width="450" />'.format(data_uri)
 
print(img_tag)

#print ' <p><a style="color:red;" href="datadisplay.py">assessment %s </a></p>' %ids

for i in partitions:
        temp=(ids, i, i)
        print ' <p><a style="color:red;" href="datadisplay.py?id=%s&post=%s">sentiment score %s </a></p>' %temp

conn.close
print """
  </body>
</html>  
"""
