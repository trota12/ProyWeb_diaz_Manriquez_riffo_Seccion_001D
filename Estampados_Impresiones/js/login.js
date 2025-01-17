const form = document.getElementById("form");
const email = document.getElementById("Email");
const password = document.getElementById("password");

// Escucha el evento de envío del formulario
form.addEventListener("submit", (e) => {
  e.preventDefault(); // Evita el envío del formulario
  validateLoginInputs();
});

// Función para validar los campos del formulario
function validateLoginInputs() {
  const emailValue = email.value.trim();
  const passwordValue = password.value.trim();

  // Validar el campo de email
  if (emailValue === "") {
    setErrorFor(email, "El email no puede estar vacío.");
  } else if (!isEmail(emailValue)) {
    setErrorFor(email, "El email no es válido.");
  } else {
    setSuccessFor(email);
  }

  // Validar el campo de contraseña
  if (passwordValue === "") {
    setErrorFor(password, "La contraseña no puede estar vacía.");
  } else {
    setSuccessFor(password);
  }

  // Verificar si ambos campos son válidos antes de proceder
  if (emailValue !== "" && isEmail(emailValue) && passwordValue !== "") {
    alert("¡Inicio de sesión exitoso!");
    // Aquí puedes usar un fetch o enviar el formulario
    // form.submit();
  }
}

// Función para mostrar error en un campo
function setErrorFor(input, message) {
  const formControl = input.parentElement;
  const small = formControl.querySelector("small");
  formControl.className = "form-control error";
  small.innerText = message;
}

// Función para mostrar éxito en un campo
function setSuccessFor(input) {
  const formControl = input.parentElement;
  formControl.className = "form-control success";
}

// Función para validar formato de email
function isEmail(email) {
  return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
    email
  );
}
function togglePassword() {
          const passwordField = document.getElementById("password");
          const toggleButton = document.querySelector(".toggle-password");
          
          if (passwordField.type === "password") {
            passwordField.type = "text";
            toggleButton.textContent = "🙈";
          } else {
            passwordField.type = "password";
            toggleButton.textContent = "👁️";
          }
        }