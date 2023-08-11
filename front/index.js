const btn = document.getElementById("aaaaaa");

async function fetcher(url, method, body){
    let response = await fetch(url,{
        method:method,
        mode:"cors",
        credentials:"include",
        headers: {
            "Content-Type": "application/json"
        },
        redirect:"follow",
        body:JSON.stringify(body)
    });
    return response.json();
} 


btn.onclick = async ()=>{
    let response = await fetch("http://localhost:8080");//proxy to /api/
    if(response.ok){
        let results = await response.json();
        console.log(results);
        alert(JSON.stringify(results));
    }
    else{
        console.log(response.status);
        console.log(response.statusText);
    }
}
    
