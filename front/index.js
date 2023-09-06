const loginForm = document.getElementById("loginForm")
const registerForm = document.getElementById("registerForm")
const aaaBtn = document.getElementById("aaaaaa");
let auth_token = null;//set on page load if logged in

async function fetcher(url, method, body){
    let response = await fetch(url,{
        method:method,
        mode:"cors",
        credentials:"include",
        headers: {
            "Content-Type": "application/json",
            "Anti-CSRF": `${auth_token}`//only used on protected routes
        },
        redirect:"follow",
        body:JSON.stringify(body)
    });
    return response.json();
} 

async function healthCheck() {
    let response = await fetch("/api");//proxy to /api/
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

/*async function hideForms(hiddenStates){
    switch(hiddenStates){
        case "Register":
            loginForm.hidden = true;
            registerForm.hidden = false;
            break;
        case "Login":
            loginForm.hidden = false;
            registerForm.hidden = true;
            break; 
        case "Logout":
            let logoutResp = await fetch("/api/auth/logout");
            console.log(logoutResp);
            hideForms("Login");
            break;
        default:
            loginForm.hidden = true;
            break;
    }
}*/
/*
case "Logout":
    let logoutResp = await fetch("/api/auth/logout");
    console.log(logoutResp);
    hideForms("Login");
*/ 
aaaBtn.addEventListener("click", healthCheck);
loginForm.addEventListener("submit", async function(){
    let loginResp = await fetcher("/api/auth/login", "POST", {});
    console.log(loginResp);
    //hideForms(null);
});