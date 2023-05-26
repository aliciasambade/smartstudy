function changeIcon() {
    var icon = document.getElementById("likeIcon");
    var button = document.getElementById("likeButton");
    if (icon.classList.contains("fa-regular")) {
        icon.classList.remove("fa-regular");
        icon.classList.add("fa-solid");
        icon.style.color = "#ff0000";
        button.setAttribute("aria-pressed", "true");
    } else {
        icon.classList.remove("fa-solid");
        icon.classList.add("fa-regular");
        icon.style.color = "#000000";
        button.setAttribute("aria-pressed", "false");
    }
}
function redirectToPost(postId) {
    var url = '/view_post/' + postId;
    window.location.href = url;
}
function redirectToSignIn() {
  window.location.href = "/sign_in";
}
function redirectToLogIn() {
  window.location.href = "/login";
}
function loadPreview(event) {
    var input = event.target;
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var preview = document.getElementById('square');
            preview.style.backgroundImage = "url('" + e.target.result + "')";
            preview.style.backgroundSize = "cover";
            preview.querySelector('p').style.display = "none";
        }
      reader.readAsDataURL(input.files[0]);
    }
}

// Esperar a que el documento HTML se cargue completamente
document.addEventListener("DOMContentLoaded", function() {
  // Obtener referencias a los campos de entrada y al botón de envío
  var nombreInput = document.querySelector('input[name="user_name"]');
  var apellidosInput = document.querySelector('input[name="user_surname"]');
  var fechaInput = document.querySelector('input[name="user_birthday"]');
  var submitBtn = document.querySelector('#submit-btn');
  var errorMessage = document.querySelector('#error-message');

  // Agregar eventos de escucha para los campos de entrada
  nombreInput.addEventListener("input", validarNombre);
  apellidosInput.addEventListener("input", validarApellidos);
  fechaInput.addEventListener("input", validarFecha);

  // Función para habilitar o deshabilitar el botón de envío y mostrar el aviso de error
  function toggleSubmitButton() {
    var inputs = document.querySelectorAll('input[required]');
    var hasErrors = false;

    inputs.forEach(function(input) {
      if (input.classList.contains('input-error')) {
        hasErrors = true;
      }
    });

    submitBtn.disabled = hasErrors;
    errorMessage.style.display = hasErrors ? 'block' : 'none';
  }

  // Funciones de validación
  function validarNombre() {
    var nombre = this.value;
    var mensajeError = "";

    if (!/^[a-zA-Z]+$/.test(nombre)) {
      mensajeError = "El nombre solo debe contener letras";
    }

    mostrarError(this, mensajeError);
    toggleSubmitButton();
  }

  function validarApellidos() {
    var apellidos = this.value;
    var mensajeError = "";

    if (!/^[a-zA-Z\s]+$/.test(apellidos)) {
      mensajeError = "Los apellidos solo deben contener letras";
    }

    mostrarError(this, mensajeError);
    toggleSubmitButton();
  }

  function validarFecha() {
    var fecha = new Date(this.value);
    var mensajeError = "";

    if (isNaN(fecha) || fecha < new Date("2000-01-01")) {
      mensajeError = "La fecha debe ser más reciente que 01/01/2000";
    }

    mostrarError(this, mensajeError);
    toggleSubmitButton();
  }

  function mostrarError(input, mensaje) {
    var mensajeErrorElemento = input.nextElementSibling;

    if (!mensajeErrorElemento || !mensajeErrorElemento.classList.contains("mensaje-error")) {
        mensajeErrorElemento = document.createElement("div");
        mensajeErrorElemento.classList.add("mensaje-error");
        input.parentNode.insertBefore(mensajeErrorElemento, input.nextSibling);
var     submitErrorElemento = document.querySelector("#submit_error");
        submitErrorElemento.textContent = "Error: Hay campos inválidos.";
    }

    mensajeErrorElemento.textContent = mensaje;
    input.classList.toggle("input-error", mensaje !== "");
  }
});
//header
var editProfile = document.querySelector(".grid-header .edit_profile");
editProfile.addEventListener("click", function () {
document.body.classList.toggle("active");
});

