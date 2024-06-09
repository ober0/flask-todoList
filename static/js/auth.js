document.getElementById('reg').addEventListener('click', function () {
    let username = document.getElementById('username').value
    let password = document.getElementById('password').value

    let data = {
        username: username,
        password: password
    }

    fetch('/reg', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(result => {
            if (result.success){
                window.location.href = '/home'
            }
            else {
                const error = document.getElementById('error')
                error.innerText = 'Произошла ошибка:' + result.message
                error.style.color = 'red'
            }
        })

})