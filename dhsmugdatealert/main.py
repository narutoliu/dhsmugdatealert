#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import csv
import sys
import jinja2
import os
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))



errormsg="""
<!DOCTYPE> <html><head><title>test date alert</title>
<meta name="viewport" content="width=device-width, height=device-height, user-scalable=no"> 
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
<META HTTP-EQUIV="content-type" CONTENT="text/html; charset=utf-8">
<link rel="stylesheet" href="/static/style.css" />
</head>
<body>

<center><img alt="dhs logo" src="static/logo.jpg"></center>
<center><p id="alert"><b>DHS test date alert</b></p></center>
<label for="name"><center><form method="post" action="/analysis">
	enter your name:</center><center><input type="text" id="name" name="name" value=%(name)s><center><i>eg:liu.fengyuan</i></center>
	<br>
	<center><input type="submit" value="submit" ></center>
</form>
<center><div id="error">%(error)s</div></center>
<center><p id="today">TODAY IS!!!</p><b><script type="text/javascript">
<!--

var m_names = new Array("January", "February", "March",
"April", "May", "June", "July", "August", "September",
"October", "November", "December");

var d = new Date();
var curr_date = d.getDate();
var curr_month = d.getMonth();
var curr_year = d.getFullYear();
document.write(curr_date + "-" + m_names[curr_month]
+ "-" + curr_year);



//-->
</script></b></center>
</div>
</body>

"""
class MainHandler(webapp2.RequestHandler):
    def get(self):
        name=self.request.get('name').lower()
        template_values = {
            'name': name,
        }
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))

class Analysis(webapp2.RequestHandler):
    def write_error(self,error="",name=""):
         self.response.out.write(errormsg% {"error":error,"name":name})
         template_values = {}
         template = jinja_environment.get_template('footer.html')
         self.response.out.write(template.render(template_values))
    def post(self):
        read=csv.reader(open("subjcombi.csv", "r"), delimiter = ",", skipinitialspace=True)
        read2=csv.reader(open("testdate.csv", "r"), delimiter = ",", skipinitialspace=True)
        
        username=[]
        
        name=self.request.get('name').lower()
        checker=False
        for row in read:
            if row[0]==name:
                username=row
                checker=True
                break
        
        
        if checker:
            greeting=("welcome "+str(name))
            template_values = {}

            template = jinja_environment.get_template('head.html')
            self.response.out.write(template.render(template_values))
            self.response.out.write("""<h1>"""+greeting+"""</h1>""")
            template2 = jinja_environment.get_template('home.html')
            self.response.out.write(template2.render(template_values))
            
            for test in read2:
                if test:
                   for i in username[5:-1]:
                       if test[0]==i:
                           subject=test[0]
                           paper=test[1]
                           date=test[2]
                           time=test[3]
                           checker=True
                           table=("""<center><table width="400" style="border:1px solid black;">
                                    <tr><td>dummyreplacer</td>
                                    </tr></table></center>""")
                           dummyreplacer=('<b style="color:blue">'+subject+"</b>"+":"+"<b>PAPER NUMBER</b>"+paper+","+"<b>DATE</b>"+date+","+"<b>TIME</b>"+time)
                           self.response.out.write(table.replace("dummyreplacer",str(dummyreplacer)))
            template_values = {}

            template = jinja_environment.get_template('footer.html')
            self.response.out.write(template.render(template_values))
        else:
            self.write_error("this person is not from DHS senior high",name)
            
        
        

app = webapp2.WSGIApplication([('/', MainHandler),('/analysis',Analysis)],
                              debug=True)
