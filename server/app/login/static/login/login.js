function toggle() {
    let toggle_button = document.getElementById('toggle-button')
    let password_input = document.getElementById('id_password')

    if (password_input.type === 'password') {
        console.log('password')
        password_input.type = 'text'
        toggle_button.innerHTML = `<iconify-icon icon="fluent:eye-off-32-filled" width="17.5" height="17.5"></iconify-icon>`
    } else {
        console.log('text')
        password_input.type = 'password'
        toggle_button.innerHTML = `<iconify-icon icon="fluent:eye-32-filled" width="17.5" height="17.5"></iconify-icon>`
    }
}

