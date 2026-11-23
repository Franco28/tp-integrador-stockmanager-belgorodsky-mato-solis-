(() => {
  const imageInput = document.getElementById("product-image");
  const imageUrlInput = document.getElementById("product-image-url");
  const imagePreview = document.getElementById("image-preview");
  const removeImageInput = document.querySelector('input[name="quitar_imagen"]');

  if (!imageInput || !imagePreview) return;

  let previewUrl;
  let urlPreviewTimer;
  const originalImageUrl = imagePreview.querySelector("img")?.src;

  const showMessage = (message) => {
    const placeholder = document.createElement("span");
    placeholder.className = "image-preview-placeholder";
    placeholder.textContent = message;
    imagePreview.replaceChildren(placeholder);
  };

  const showImage = (src, alt) => {
    const image = document.createElement("img");
    image.alt = alt;
    image.addEventListener("error", () => {
      if (imagePreview.contains(image)) showMessage("No se pudo cargar la imagen");
    }, { once: true });
    imagePreview.replaceChildren(image);
    image.src = src;
  };

  const showOriginalOrEmpty = () => {
    if (originalImageUrl) {
      showImage(originalImageUrl, "Imagen actual del producto");
    } else {
      showMessage("Sin imagen");
    }
  };

  const revokePreviewUrl = () => {
    if (!previewUrl) return;
    URL.revokeObjectURL(previewUrl);
    previewUrl = undefined;
  };

  imageInput.addEventListener("change", () => {
    const file = imageInput.files?.[0];
    window.clearTimeout(urlPreviewTimer);

    if (!file) {
      revokePreviewUrl();
      showOriginalOrEmpty();
      return;
    }

    if (imageUrlInput) imageUrlInput.value = "";
    if (removeImageInput) removeImageInput.checked = false;
    revokePreviewUrl();
    previewUrl = URL.createObjectURL(file);
    showImage(previewUrl, "Vista previa de la imagen seleccionada");
  });

  const previewImageUrl = () => {
    if (imageInput.files?.length || !imageUrlInput) return;
    const value = imageUrlInput.value.trim();
    if (removeImageInput) removeImageInput.checked = false;

    if (!value) {
      revokePreviewUrl();
      showOriginalOrEmpty();
      return;
    }

    try {
      const url = new URL(value);
      if (url.protocol !== "https:") return;
      revokePreviewUrl();
      showImage(url.href, "Vista previa de la URL ingresada");
    } catch {
      // La validación definitiva de la URL se realiza al guardar el formulario.
    }
  };

  imageUrlInput?.addEventListener("input", () => {
    window.clearTimeout(urlPreviewTimer);
    urlPreviewTimer = window.setTimeout(previewImageUrl, 250);
  });
  imageUrlInput?.addEventListener("change", previewImageUrl);

  removeImageInput?.addEventListener("change", () => {
    if (removeImageInput.checked) {
      if (imageUrlInput) imageUrlInput.value = "";
      if (!imageInput.files?.length) showMessage("Sin imagen");
    } else {
      showOriginalOrEmpty();
    }
  });
})();
