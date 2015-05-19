#!/usr/bin/env python

print 'Content-type: text/html\r\n\r\n'

import cgitb; cgitb.enable()

import psycopg2

conn=psycopg2.connect(database="intersective", user="postgres", password="010305")
                   
cur=conn.cursor()


sql ="select distinct assess_assessments.id"
sql = sql+" from  public.assess_assessments, public.assess_assessment_submissions, public.assess_assessment_submission_answers, public.assess_answer_analysis_results"
sql = sql+" where assess_answer_analysis_results.assessment_submission_answer_id = assess_assessment_submission_answers.id"
sql = sql+"  and  assess_assessment_submissions.assessment_id = assess_assessments.id"
sql = sql+"  and  assess_assessment_submissions.id = assess_assessment_submission_answers.assessment_submission_id"
sql = sql+" order by assess_assessments.id;"

cur.execute(sql)

#print """<link rel="stylesheet" type="text/css" href="myStylesheet1.css" />"""   

#ids=1
rows=cur.fetchall()

print """
<html>
  <head>
    <title>The list of assessments</title>
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
    <h1>The list of assessments</h1>
"""

for row in rows:
    
   ids=row[0]
   temp=(ids, ids)
   print '<p><a style="color:red;" href="Figuredisplay.py?post=%s">assessments %s</a></p>' %temp

conn.close

print """   
  </body>
</html>  
"""



