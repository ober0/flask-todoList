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




const tasks = document.querySelectorAll('.task')
tasks.forEach(function (task) {
    task.addEventListener('click', function () {
        let task_id = task.getAttribute('for')

        let data;
        if (task.getAttribute('status') == "True"){
            data = {
                taskId: task_id,
                status: false
            }
        }
        else {
            data = {
                taskId: task_id,
                status: true
            }
        }

        fetch('/do', {
            method: 'post',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(result => {
                if (result.success){
                    if (result.status){
                        task.classList.add('checked')
                        task.setAttribute('status', 'True')
                    }
                    else {
                        task.classList.remove('checked')
                        task.setAttribute('status', 'False')
                    }

                }
                else {
                    alert('Ошибка:' + result.message)
                }
            })
    })
})

const close = document.querySelectorAll('.close')
close.forEach(function (span) {
    span.addEventListener('click', function () {
        let taskId = span.getAttribute('for')

        fetch('/remTask', {
            method: 'post',
            headers: {
                "Content-Type":'application/json'
            },
            body: JSON.stringify({taskId: taskId})
        })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    let parents = document.querySelectorAll('.task')
                    parents.forEach(function (parent) {
                        if (parent.getAttribute('for') == taskId) {
                            parent.remove()
                        }
                    })
                }
                else {
                    alert('Ошибка' + result.message)
                }
            })
    })
})