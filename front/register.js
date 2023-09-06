const registerForm = document.getElementById("registerForm")
let auth_token = null;//set on page load if logged in

async function fetcher(url, method, body){
    let response = await fetch(url,{
        method:method,
        mode:"cors",
        credentials:"include",
        headers: {
            "Content-Type": "application/json",
            "Authentication": `${auth_token}`//only used on protected routes
        },
        redirect:"follow",
        body:JSON.stringify(body)
    });
    return response.json();
} 

registerForm.addEventListener("submit", async function(){
    let loginResp = await fetcher("/api/auth/register", "POST", {});
    console.log(loginResp);
    //hideForms(null);
});