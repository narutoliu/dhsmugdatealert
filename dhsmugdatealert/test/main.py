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


mainpage="""<!DOCTYPE html>
<head><title>test date alert</title>
<meta name="viewport" content="width=device-width, height=device-height, user-scalable=no"> 
    

<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
<style type="text/css">
body {background-color:white;}
</style>
<META HTTP-EQUIV="content-type" CONTENT="text/html; charset=utf-8">
</head>
<body>

<center><img style="width: 200px; height: 200px; margin-top: 5px;" alt="dhs logo" src="static/logo.jpg"></center>
<center><p style="color: red;"><b>DHS test date alert</b></p></center>
<label for="name"><center><form method="post" action="/analysis">
	enter your name:</center><center><input type="text" id="name" name="name"><center><i>eg:liu.fengyuan</i></center>
	<br>
	<center><input type="submit" value="submit" ></center>
</form>
<center><p style="color: green;">TODAY IS!!!</p><b><script type="text/javascript">
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
<div id="footer" style="background-color:blue;clear:both;text-align:center;">
<b style="color: white;">&copy feng yuan</b>
</div>
"""

head="""<!DOCTYPE html>
<head><title>test date alert</title>
<meta name="viewport" content="width=device-width, height=device-height, user-scalable=no"> 

<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
<script type="text/javascript">
$(document).ready(function(){
  $("button").click(function(){
    $("td").css({"font-size":"200%"});
  });
});
</script>
<style type="text/css">
body {background-color:white;}
</style>
<META HTTP-EQUIV="content-type" CONTENT="text/html; charset=utf-8">
</head>
<body>
<center><img style="width: 200px; height: 200px; margin-top: 5px;" alt="dhs logo" src="static/logo.jpg"></center>
<h1>anonymous</h1>
<button>Click me to enlarge</button>
</body>
"""

home="""<center><FORM>
<INPUT TYPE="BUTTON" VALUE="Home Page" ONCLICK="window.location.href='/'"> 
</FORM></center>
"""
footer="""<div id="footer" style="background-color:blue;clear:both;text-align:center;">
<b style="color: white;">&copy feng yuan</b>
</div>"""
errormsg="""
<!DOCTYPE html><head><title>test date alert</title>
<meta name="viewport" content="width=device-width, height=device-height, user-scalable=no"> 
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
<style type="text/css">
body {background-color:white;}
</style>
<META HTTP-EQUIV="content-type" CONTENT="text/html; charset=utf-8">
</head>
<body>

<center><img style="width: 200px; height: 200px; margin-top: 5px;" alt="dhs logo" src="static/logo.jpg"></center>
<center><p style="color: red;"><b>DHS test date alert</b></p></center>
<label for="name"><center><form method="post" action="/analysis">
	enter your name:</center><center><input type="text" id="name" name="name" value=%(name)s><center><i>eg:liu.fengyuan</i></center>
	<br>
	<center><input type="submit" value="submit" ></center>
</form>
<center><div style="color:red">%(error)s</div></center>
<center><p style="color: green;">TODAY IS!!!</p><b><script type="text/javascript">
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
<div id="footer" style="background-color:blue;clear:both;text-align:center;">
<b style="color: white;">&copy feng yuan</b>
</div>
"""
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(mainpage)
    

class Analysis(webapp2.RequestHandler):
    def write_error(self,error="",name=""):
        self.response.out.write(errormsg % {"error":error,"name":name})
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
            self.response.out.write(head.replace("anonymous","welcome "+str(name)))
            self.response.out.write(home)
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
            self.response.out.write(footer)
        else:
            self.write_error("this person is not from DHS senior high",name)
        
        

app = webapp2.WSGIApplication([('/', MainHandler),('/analysis',Analysis)],
                              debug=True)
