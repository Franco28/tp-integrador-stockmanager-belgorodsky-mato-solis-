const passwordInput = document.getElementById("login-password");
const passwordToggle = document.querySelector(".password-toggle");

if (passwordInput && passwordToggle) {
  passwordToggle.addEventListener("click", () => {
    const mostrar = passwordInput.type === "password";
    passwordInput.type = mostrar ? "text" : "password";
    passwordToggle.setAttribute(
      "aria-label",
      mostrar ? "Ocultar contraseña" : "Mostrar contraseña",
    );
    passwordToggle.setAttribute("aria-pressed", String(mostrar));
    passwordToggle.classList.toggle("is-visible", mostrar);
  });
}
