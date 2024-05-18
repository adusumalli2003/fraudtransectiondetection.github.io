const signInBtnLink = document.querySelector('.signInBtn-link');
const signUpBtnLink = document.querySelector('.signUpBtn-link');
const wrapper = document.querySelector('.wrapper');
signUpBtnLink.addEventListener('click', () => {
    wrapper.classList.toggle('active');
});
signInBtnLink.addEventListener('click', () => {
    wrapper.classList.toggle('active');
});
document.getElementById("login").addEventListener("submit", function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    console.log(formData)
    fetch("/login", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        console.log(data.stat)
        if (data.stat) {
            window.location.href = "/menu";
        } else {
            alert("Incorrect Username or Password")
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
document.getElementById("signup").addEventListener("submit", function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    fetch("/signup", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.stat) {
            alert("Signup successful please Login");
            window.location.href = "/";
        } else {
            alert("Signup failed")
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});