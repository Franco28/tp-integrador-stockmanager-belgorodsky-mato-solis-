const flashContainer = document.getElementById("flash-messages");

if (flashContainer && window.Swal) {
  const toast = window.Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 3500,
    timerProgressBar: true,
    heightAuto: false,
    didOpen: (element) => {
      element.addEventListener("mouseenter", window.Swal.stopTimer);
      element.addEventListener("mouseleave", window.Swal.resumeTimer);
    },
  });

  const iconByType = {
    ok: "success",
    error: "error",
    warning: "warning",
    info: "info",
  };

  const messages = [...flashContainer.querySelectorAll(".flash-message")];
  flashContainer.hidden = true;

  (async () => {
    for (const message of messages) {
      await toast.fire({
        icon: iconByType[message.dataset.type] || "info",
        title: message.textContent.trim(),
      });
    }
  })();
}
