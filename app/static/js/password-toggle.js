document.querySelectorAll(".password-toggle").forEach((passwordToggle) => {
  const passwordInput = document.getElementById(passwordToggle.getAttribute("aria-controls"));
  if (!passwordInput) return;

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
});
