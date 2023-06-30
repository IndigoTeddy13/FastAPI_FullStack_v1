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
    let results = await fetcher("http://localhost:80/", "GET", /*{
        "myname":"Jotaro Kujo",
        "standname": "Star Platinum"
    }*/);
    console.log(results);
    alert(JSON.stringify(results));
}
    
