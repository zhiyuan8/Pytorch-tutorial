import fetch from 'node-fetch';
fetch('http://35.232.0.181:8041/get-generated-image?username=johnsmith&project_id=10&prompt_id=0')
.then(response =>{return response.json()})
.then(response =>{
 console.log(response)
})

