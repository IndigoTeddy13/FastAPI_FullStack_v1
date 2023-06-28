const btn = document.getElementById("aaaaaa");

async function fetcher(url, method, body){
    let response = await fetch(url,{
        method:method,
        mode:"cors",
        credentials:"same-origin",
        headers: {
            "Content-Type": "application/json",
        },
        redirect:"follow",
        body:JSON.stringify(body)
    });
    return response.json();
} 


btn.onclick = async ()=>{
    results = await fetcher("http://localhost:80/api/", "GET", /*{
        "myname":"Jotaro Kujo",
        "standname": "Star Platinum"
    }*/);
    await console.log(results);
    await alert(JSON.stringify(results));
}
    
