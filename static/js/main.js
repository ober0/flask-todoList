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
                let taskCountList = document.querySelectorAll('.close')
                let tclLength = taskCountList.length
                if (tclLength == 0){
                    window.location.reload()
                }
                let taskCount = taskCountList[tclLength-1].getAttribute('for')


                let taskCountList2 = document.querySelectorAll('.task')
                let tclLength2 = taskCountList2.length
                if (tclLength2 == 0){
                    window.location.reload()
                }
                let taskCount2 = taskCountList2[tclLength2-1].getAttribute('for')



                const parent = document.getElementById('myUL')

                const child = document.createElement('li')
                child.innerText = text
                child.classList.add('task')
                child.setAttribute('for', parseInt(taskCount2)+1)

                var span = document.createElement("SPAN");
                var txt = document.createTextNode("\u00D7");
                span.className = "close";
                span.appendChild(txt);

                span.setAttribute('for', parseInt(taskCount)+1)
                child.appendChild(span);

                parent.appendChild(child)
            }
            else{
                alert('Ошибка:' + result.error)
            }

        })
}


