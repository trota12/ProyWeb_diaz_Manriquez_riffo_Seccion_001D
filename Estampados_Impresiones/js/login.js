document.getElementById('togglePassword').addEventListener('click', function () {
    const passwordInput = document.getElementById('password');
    const type = passwordInput.type === 'password' ? 'text' : 'password';
    passwordInput.type = type;
    this.textContent = type === 'password' ? '👁️' : '🙈';
});

document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault();
    let isValid = true;

    // Validar correo
    const email = document.getElementById('email').value;
    const emailError = document.getElementById('emailError');
    if (!/^[\w-.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email)) {
        emailError.textContent = 'Correo inválido.';
        emailError.style.display = 'block';
        isValid = false;
    } else {
        emailError.style.display = 'none';
    }

    // Validar contraseña
    const password = document.getElementById('password').value;
    const passwordError = document.getElementById('passwordError');
    if (password.length < 6) {
        passwordError.textContent = 'La contraseña debe tener al menos 6 caracteres.';
        passwordError.style.display = 'block';
        isValid = false;
    } else {
        passwordError.style.display = 'none';
    }

    if (isValid) {
        alert('Formulario enviado con éxito');
        // Aquí puedes manejar el envío del formulario (e.g., AJAX, redireccionar, etc.)
    }
});
