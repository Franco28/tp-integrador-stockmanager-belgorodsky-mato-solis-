const imageInput = document.getElementById("product-image");
const imagePreview = document.getElementById("image-preview");

if (imageInput && imagePreview) {
  let previewUrl;

  imageInput.addEventListener("change", () => {
    const file = imageInput.files?.[0];
    if (!file) return;

    if (previewUrl) URL.revokeObjectURL(previewUrl);
    previewUrl = URL.createObjectURL(file);

    const image = document.createElement("img");
    image.src = previewUrl;
    image.alt = "Vista previa de la imagen seleccionada";
    imagePreview.replaceChildren(image);
  });
}
