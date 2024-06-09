function newElement() {
    let textInput = document.getElementById('myInput')
    let text = textInput.value

    fetch('/newtask', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({text:text})
    })
        .then(response => response.json())
        .then(result => {
            if (result.success){
                const parent = document.getElementById('myUL')

                const child = document.createElement('li')
                child.innerText = text

                parent.appendChild(child)
            }
            else{
                alert('Ошибка:' + result.error)
            }

        })
}