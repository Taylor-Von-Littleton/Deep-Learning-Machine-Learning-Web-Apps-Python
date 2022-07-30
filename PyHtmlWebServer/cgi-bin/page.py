#!/usr/bin/python3
import random
import datetime

print('Content-type:text/html\n') # print the header
print('<!DOCTYPE html>') # print the html header

print('<link rel="stylesheet" type="text/css" href="../style/style.css">') # print the css file

print('<div class="content">') # print the content div
print('<h1> These are your random numbers at this date and time<br/>' + str(datetime.datetime.now())+'</h1>') # print the date and time

for i in range(10):
    print ('<p> Random #' + str(i+1) + ': ' + str(random.randrange(0,1000)) + '<p>') # print the random numbers


print('<p> <a href="/"> Home Page </a></p>') # print the link to the home page
print('</div>') # print the closing div