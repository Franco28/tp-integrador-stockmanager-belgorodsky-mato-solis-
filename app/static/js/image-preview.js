const imageInput = document.getElementById("product-image");
const imageUrlInput = document.getElementById("product-image-url");
const imagePreview = document.getElementById("image-preview");
const removeImageInput = document.querySelector('input[name="quitar_imagen"]');

if (imageInput && imagePreview) {
  let previewUrl;
  let urlPreviewTimer;
  const originalImageUrl = imagePreview.querySelector("img")?.src;

  const showImage = (src, alt) => {
    const image = document.createElement("img");
    image.src = src;
    image.alt = alt;
    image.addEventListener("error", () => {
      if (!imagePreview.contains(image)) return;
      const placeholder = document.createElement("span");
      placeholder.className = "image-preview-placeholder";
      placeholder.textContent = "No se pudo cargar la imagen";
      imagePreview.replaceChildren(placeholder);
    }, { once: true });
    imagePreview.replaceChildren(image);
  };

  const showOriginalOrEmpty = () => {
    if (originalImageUrl) {
      showImage(originalImageUrl, "Imagen actual del producto");
    } else {
      const placeholder = document.createElement("span");
      placeholder.className = "image-preview-placeholder";
      placeholder.textContent = "Sin imagen";
      imagePreview.replaceChildren(placeholder);
    }
  };

  imageInput.addEventListener("change", () => {
    const file = imageInput.files?.[0];
    if (!file) {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
      previewUrl = undefined;
      showOriginalOrEmpty();
      return;
    }

    if (imageUrlInput) imageUrlInput.value = "";
    if (removeImageInput) removeImageInput.checked = false;
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    previewUrl = URL.createObjectURL(file);
    showImage(previewUrl, "Vista previa de la imagen seleccionada");
  });

  imageUrlInput?.addEventListener("input", () => {
    if (imageInput.files?.length) return;
    window.clearTimeout(urlPreviewTimer);
    urlPreviewTimer = window.setTimeout(() => {
      const value = imageUrlInput.value.trim();
      if (removeImageInput) removeImageInput.checked = false;
      if (!value) {
        showOriginalOrEmpty();
        return;
      }
      try {
        const url = new URL(value);
        if (url.protocol === "https:") {
          if (previewUrl) URL.revokeObjectURL(previewUrl);
          previewUrl = undefined;
          showImage(url.href, "Vista previa de la URL ingresada");
        }
      } catch {
        // El formulario informa la URL inválida al guardar.
      }
    }, 400);
  });

  removeImageInput?.addEventListener("change", () => {
    if (removeImageInput.checked) {
      if (imageUrlInput) imageUrlInput.value = "";
      if (!imageInput.files?.length) {
        const placeholder = document.createElement("span");
        placeholder.className = "image-preview-placeholder";
        placeholder.textContent = "Sin imagen";
        imagePreview.replaceChildren(placeholder);
      }
    } else {
      showOriginalOrEmpty();
    }
  });
}
