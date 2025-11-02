document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("formRegistro");
  const formContainer = document.querySelector(".register-form");

  // Crear contenedor de alerta al inicio del formulario
  const alertaDiv = document.createElement("div");
  alertaDiv.classList.add("alert", "alert-danger", "mt-2");
  alertaDiv.style.display = "none";

  // Insertar la alerta justo debajo del título
  const titulo = formContainer.querySelector("h2");
  formContainer.insertBefore(alertaDiv, titulo.nextSibling);

  function mostrarError(mensaje) {
    alertaDiv.innerText = mensaje;
    alertaDiv.style.display = "block";
    window.scrollTo({ top: formContainer.offsetTop - 50, behavior: 'smooth' });
  }

  form.addEventListener("submit", function(e) {
    alertaDiv.style.display = "none";

    const dateInput = document.getElementById("date");
    const password1 = document.getElementById("password1");
    const password2 = document.getElementById("password2");
    const email = document.getElementById("email");
    const username = document.getElementById("username");

    // 🔹 Validar fecha de nacimiento (no puede ser futura)
    const birthDate = new Date(dateInput.value);
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    if (birthDate > today) {
      e.preventDefault();
      mostrarError("⚠️ La fecha de nacimiento no puede ser posterior a hoy.");
      dateInput.focus();
      return;
    }

    // 🔹 Validar longitud mínima de contraseña
    if (password1.value.length < 8) {
      e.preventDefault();
      mostrarError("🔒 La contraseña debe tener al menos 8 caracteres.");
      password1.focus();
      return;
    }

    // 🔹 Validar coincidencia de contraseñas
    if (password1.value !== password2.value) {
      e.preventDefault();
      mostrarError("❌ Las contraseñas no coinciden.");
      password2.focus();
      return;
    }

    // 🔹 Validar formato de correo electrónico
    const emailRegex = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
    if (!emailRegex.test(email.value.trim())) {
      e.preventDefault();
      mostrarError("📧 Por favor ingrese un correo válido.");
      email.focus();
      return;
    }

    // 🔹 Validar nombre de usuario (sin espacios)
    if (/\s/.test(username.value.trim())) {
      e.preventDefault();
      mostrarError("👤 El nombre de usuario no puede contener espacios.");
      username.focus();
      return;
    }

    // 🔹 Validar campos vacíos (seguridad adicional)
    const campos = [dateInput, password1, password2, email, username];
    for (let campo of campos) {
      if (!campo.value.trim()) {
        e.preventDefault();
        mostrarError(`⚠️ El campo "${campo.name}" no puede estar vacío.`);
        campo.focus();
        return;
      }
    }
  });
});
