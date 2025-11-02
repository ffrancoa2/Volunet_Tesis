document.addEventListener("DOMContentLoaded", function () {
  const categorySelect = document.getElementById("id_category");
  const input = document.getElementById("id_location");
  const latInput = document.getElementById("id_lat");
  const lngInput = document.getElementById("id_lng");

  if (!categorySelect || !input) return;

  const suggestionBox = document.createElement("div");
  suggestionBox.classList.add("list-group", "position-absolute", "w-100", "zindex-dropdown");
  input.parentNode.appendChild(suggestionBox);

  let timeout = null;

  // Función principal: activar o desactivar autocompletado según categoría
  function toggleAutocomplete() {
    const isMoney = categorySelect.value.toLowerCase().trim() === "dinero";

    // Si es dinero, desactivamos el autocompletado
    if (isMoney) {
      input.removeEventListener("input", handleInput);
      document.removeEventListener("click", handleClickOutside);
      suggestionBox.innerHTML = "";
      return;
    }

    // Si no es dinero, activamos los listeners
    input.addEventListener("input", handleInput);
    document.addEventListener("click", handleClickOutside);
  }

  // Manejador del evento input (autocompletar)
  function handleInput() {
    clearTimeout(timeout);
    const query = this.value.trim();

    if (query.length < 3) {
      suggestionBox.innerHTML = "";
      return;
    }

    timeout = setTimeout(() => {
      fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${query}&addressdetails=1&limit=5`)
        .then((res) => res.json())
        .then((data) => {
          suggestionBox.innerHTML = "";
          data.forEach((item) => {
            const option = document.createElement("button");
            option.type = "button";
            option.classList.add("list-group-item", "list-group-item-action");
            option.textContent = item.display_name;

            option.addEventListener("click", () => {
              input.value = item.display_name;
              latInput.value = item.lat;
              lngInput.value = item.lon;
              suggestionBox.innerHTML = "";
            });

            suggestionBox.appendChild(option);
          });
        })
        .catch((err) => console.error("Error en autocompletado:", err));
    }, 400);
  }

  // Cerrar las sugerencias si se hace clic fuera
  function handleClickOutside(e) {
    if (!suggestionBox.contains(e.target) && e.target !== input) {
      suggestionBox.innerHTML = "";
    }
  }

  // Detectar cambios en la categoría
  categorySelect.addEventListener("change", toggleAutocomplete);

  // Ejecutar al cargar la página
  toggleAutocomplete();
});
