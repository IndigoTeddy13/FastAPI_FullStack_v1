//Helper functions:
async function fetcher(url, method, body){
    return await fetch(url,{
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
}
async function alerter(response, securify, warnify){
    if(response.ok){//notify unless told to hide confidential data
        let content = await response.json();
        if(!securify) alert(JSON.stringify(content, null, "\t"));
        return content;
    }
    else{//warn unless told to hide warning
        let content = await response.json();
        if(!warnify) alert(`${response.status}: ${response.statusText}\n${JSON.stringify(content, null, "\t")}`);
        return null;
    }
}

//Values
let accountMakers = document.getElementById("accountMakers");
let accountManagers = document.getElementById("accountManagers");
let activateForm = document.getElementById("activateForm");
let emailActInput = document.getElementById("email_act");
let registerForm = document.getElementById("registerForm");
let loginForm = document.getElementById("loginForm");
let auth_token = null;//set on page load if logged in

//Form Hider
async function hideForms(flag){
    if(!flag) {
        accountMakers.hidden = true
        accountManagers.hidden = false
    }
    else {
        accountMakers.hidden = false
        accountManagers.hidden = true
    }
}

//Event Listeners
window.addEventListener("load", async function(){
    let loadResp = await fetcher("/api/auth/refresh-token", "POST", {})
    auth_token = await alerter(loadResp, true, true)
    //hide
    if(auth_token) await hideForms();
    else await hideForms(true);
})
activateForm.addEventListener("submit", async function(){
    let email = String(emailActInput.value);
    let actResp = await fetcher("/api/auth/activate/"+email, "POST", {});
    await alerter(actResp)
})
registerForm.addEventListener("submit", async function(){
    let regResp = await fetcher("/api/auth/register", "POST", {
        "email":document.getElementById("email_reg").value,
        "password":document.getElementById("password_reg").value,
        "passConf":document.getElementById("passConf_reg").value,
        "displayName":document.getElementById("name_reg").value,
        "activationCode":document.getElementById("activation_reg").value
    });
    auth_token = await alerter(regResp, true)
    if(auth_token){
        alert("Registered successfully!");
        //hide
        await hideForms();
    } 
});
loginForm.addEventListener("submit", async function(){
    let loginResp = await fetcher("/api/auth/login", "POST", {
        "email":document.getElementById("email_log").value,
        "password":document.getElementById("password_log").value
    });
    auth_token = await alerter(loginResp, true)
    if(auth_token) {
        alert("Logged in successfully!")
        //hide
        await hideForms();
    }
});

document.getElementById("logout").addEventListener("click", async function(){
    let logoutResp = await fetcher("/api/auth/logout", "DELETE", {})
    await alerter(logoutResp)
    //unhide
    await hideForms(true);
});
