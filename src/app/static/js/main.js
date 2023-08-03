const btnDelete = document.querySelectorAll('.btn-delete');
if (btnDelete) {
  const btnArray = Array.from(btnDelete);
  btnArray.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      if (!confirm('¿Estás seguro/a de que quieres eliminarlo?')) {
        e.preventDefault();
      }
    });
  })
}

function validarContrasenaSegura(password) {
  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
  return regex.test(password);
}

function validarContrasenas() {
  const password = document.getElementById("passwordInput").value;
  const repeatPassword = document.getElementById("repeatPasswordInput").value;

  const passwordMessage = document.getElementById("passwordMessage");
  const repeatPasswordMessage = document.getElementById("repeatPasswordMessage");

  const submitBtn = document.getElementById("submitBtn"); // Obtiene el botón

  // Validar coincidencia de contraseñas
  if (password === repeatPassword) {
    repeatPasswordMessage.textContent = "Las contraseñas coinciden.";
    repeatPasswordMessage.className = "text-success small";
  } else {
    repeatPasswordMessage.textContent = "Las contraseñas no coinciden.";
    repeatPasswordMessage.className = "text-danger small";
  }

  // Validar contraseña segura
  if (validarContrasenaSegura(password)) {
    passwordMessage.textContent = "La contraseña es segura.";
    passwordMessage.className = "text-success small";
  } else {
    passwordMessage.textContent = "La contraseña no es segura. Debe tener al menos 8 caracteres, una letra mayúscula, una letra minúscula, un número y un carácter especial.";
    passwordMessage.className = "text-danger small textp";
  }

  // Habilitar o deshabilitar el botón según las validaciones
  if (password === repeatPassword && validarContrasenaSegura(password)) {
    submitBtn.removeAttribute("disabled"); // Habilitar el botón
  } else {
    submitBtn.setAttribute("disabled", "disabled"); // Deshabilitar el botón
  }
}

document.getElementById("passwordInput").addEventListener("input", validarContrasenas);
document.getElementById("repeatPasswordInput").addEventListener("input", validarContrasenas);



