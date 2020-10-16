# warply_backend_task
A microservice with a tornado API endpoint, designed using this bitmap roaring implementation
(https://github.com/Ezibenroc/PyRoaringBitMap) in python.   

My python version: Python 3.9.0b5
My tornado framework version: Tornado 6.0.4
<h2>Setup</h2>
To start the server at http://localhost:3000 run `python pyroaring_server.py` in the /warply_backend_task/ directory<br />

<h2>Required Features</h2>

1.**Session management: how many users have not logged in for a week?**<br>
endpoint: http://localhost:3000/api/noOfMissingUsers/7 <br>

Here 7 represents the amount of days we are checking for missing users <br>
JSON API Example: Get the users that have not logged in for a week <br />
 `curl --location --request GET 'http://localhost:3000/api/noOfMissingUsers/7' `  <br />
 result:  "Number of missing users in the last 7 days": 2<br />

2a.**Get all the users with a particular tag:**<br>

endpoint: http://localhost:3000/api/usersWithTag

A set of tags from ([tag1,tag2,...,tag10]) is given to a user randomly when they log in for the first time.<br >

Run these examples in a linux terminal after starting the server <br />
JSON API Example: Find out all the usernames with the tag "tag5" <br />
 `curl --location --request POST 'http://localhost:3000/api/usersWithTag' \ 
--header 'Content-Type: text/plain' \ 
--data-raw '{
    "tagA":"tag5" 
}'`
 <br />
result: [['Katie1'], ['Katie3'], ['Katie4']]<br /><br />

2b.**Get how many users have two specific tags**<br />
endpoint: http://localhost:3000/api/noOfUsersWithTags/<br />
JSON API Example: Find out how many usernames have the tags "tag1" and "tag2" <br />
`curl --location --request POST 'http://localhost:3000/api/noOfUsersWithTags/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "tagA":"tag1",
    "tagB":"tag2"
}'` <br />
results: Number of users with tag1 and tag2 is 2<br /><br />

3. **Load test for 1000 concurrent sessions**<br>
For this task I used the apache benchmarking tool, and started 1000 concurrent sessions by sending 1000 POST requests to the login page with a username.
The "-c 150" option in the command line means that the server is being sent the POST requests in batches of 150 at a time.
These are the analytical results:<br>
![Screenshot](/images/concurrency_test_results.png)

<h2>Extra features</h2><br/>

**Log In**<br/>

`curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"name":"newUser"}' \
  http://localhost:3000/api/login/`
  
  
**bitmap**<br/>
Create a bitmap <br>
`curl --location --request POST 'http://localhost:3000/api/bitmap/0' \
--header 'Content-Type: application/json' \
--header 'Cookie: user=2|1:0|10:1602772051|4:user|8:S2F0aWU1|cd6e99f693db9a754449ae198c9c1bd9a93d1eaf6174ad2c949227d70d71b90d' \
--data-raw '{
  "set":[1,2,3,4,5]
}  '
`
Get a bitmap with it's metadata <br>
`curl --location --request GET 'http://localhost:3000/api/bitmap/0' \
--header 'Content-Type: application/json' `

Update a bitmap <br>
`curl --location --request PUT 'http://localhost:3000/api/bitmap/0' \
--header 'Content-Type: application/json' \
--data-raw '{
  "set": [8,9,4]
}'`

Delete a bitmap <br>
`curl --location --request DELETE 'http://localhost:3000/api/bitmap/1' \
--header 'Content-Type: application/json' \`

Union of two bitmaps (by id) <br>
`curl --location --request POST 'http://localhost:3000/api/union/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id1":0,
    "id2":1
}'`

Intersection of two bitmaps (by id) <br>

`curl --location --request POST 'http://localhost:3000/api/intersection/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id1":0,
    "id2":1
}'`
