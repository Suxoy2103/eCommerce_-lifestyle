document.addEventListener("DOMContentLoaded", function () {
  function toggleSizeFields(row) {
    const sizeTypeField = row.querySelector('[name$="size_type"]');
    const shirtSizeField = row.querySelector('[name$="shirt_size"]');
    const pantsSizeField = row.querySelector('[name$="pants_size"]');

    if (sizeTypeField.value === "SHRT") {
      shirtSizeField.closest(".field-shirt_size").style.display = "";
      pantsSizeField.closest(".field-pants_size").style.display = "none";
    } else if (sizeTypeField.value === "PNT") {
      shirtSizeField.closest(".field-shirt_size").style.display = "none";
      pantsSizeField.closest(".field-pants_size").style.display = "";
    } else {
      shirtSizeField.closest(".field-shirt_size").style.display = "none";
      pantsSizeField.closest(".field-pants_size").style.display = "none";
    }
  }

  function initRow(row) {
    toggleSizeFields(row);
    const sizeTypeField = row.querySelector('[name$="size_type"]');
    sizeTypeField.addEventListener("change", () => toggleSizeFields(row));
  }

  // Инициализация всех строк в таблице
  const rows = document.querySelectorAll(".dynamic-productsizeset");
  rows.forEach(initRow);

  // Добавляем наблюдателя для новых строк
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => {
        if (node.nodeType === 1 && node.matches(".dynamic-productsizeset")) {
          initRow(node);
        }
      });
    });
  });

  const container = document.querySelector("#productsizeset-group");
  observer.observe(container, { childList: true });
});
