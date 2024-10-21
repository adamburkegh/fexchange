h1. Text Exchange Web Service

This is a simple example web service for posting and retrieving text. 

Get text. Retrieve text using a GET from `http://server/fexchange/\<student\>/\<contentid\>` where student and contentid are chosen by you. 

Eg `$ curl    http://ec2-13-238-201-131.ap-southeast-2.compute.amazonaws.com:5000/fexchange/teststudent/plastic`


Set text. Upload text using a POST to  `http://server/fexchange/\<student\>/\<contentid\>` where student and contentid are chosen by you.

Eg `$ curl  --request POST --data 'content=Your plastic pal'  http://ec2-13-238-201-131.ap-southeast-2.compute.amazonaws.com:5000/fexchange/teststudent/plastic `
