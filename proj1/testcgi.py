#import webbrowser
from pyh import *

################################page1#################
id1=1
id2=2

page = PyH('Sentiment Analysis Results')
page.addCSS('/home/hadoop/Downloads/figures/myStylesheet1.css')
#page.addJS('myJavascript1.js', 'myJavascript2.js')
page.addJS('/home/hadoop/Downloads/figures/myJavascript1.js')
page << h1('The list of assessments', cl='center')
page << a('assessments %s' %id1, style='color:red;', href='displayfigure.html', onclick='sentid(); return false;') 
page << br()
page.printOut()
##
##
##
##
###page << a('assessments %s' %id2, style='color:red;', href='file:///home/hadoop/Downloads/displayfigure.html') 
##
##page.printOut('/home/hadoop/Downloads/figurelists.html')
##new=2
##
##url = "file:///home/hadoop/Downloads/figurelists.html"
##webbrowser.open(url,new=new)
##
##
################################page2####################
##page1 = PyH('Sentiment Analysis Results')
##page1.addCSS('/home/hadoop/Downloads/figures/myStylesheet1.css')
##page1.addJS('/home/hadoop/Downloads/figures/myJavascript2.js', '/home/hadoop/Downloads/figures/myJavascript3.js')
##page1 << h1('Figure of assessment', cl='center')
##page1 << a('score %s' %id1, style='color:red;', href='datadetails.html', onclick='sentdata(); return false;') 
##page1 << br()
##
##page1.printOut('/home/hadoop/Downloads/displayfigure.html')
##
##
##
###############################page3######################
##page2 = PyH('Sentiment Analysis Results')
##page2.addCSS('/home/hadoop/Downloads/figures/myStylesheet1.css')
##page2.addJS('/home/hadoop/Downloads/figures/myJavascript4.js')
##page2 << h1('Information of submitters', cl='center')
##page2 << br()
##
##page2.printOut('/home/hadoop/Downloads/datadetails.html')



