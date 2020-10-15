# warply_backend_task
A microservice with a tornado API endpoint, designed using this bitmap roaring implementation
(https://github.com/Ezibenroc/PyRoaringBitMap) in python.   

To login send a request to localhost/login of the form :
           
curl --header "Content-Type: application/json" 
     --request POST 
     --data '{"username":"INSERT USERNAME HERE"}
