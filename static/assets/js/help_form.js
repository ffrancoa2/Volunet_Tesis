document.addEventListener('DOMContentLoaded', function() {
  const categorySelect = document.getElementById('id_category');
  const fieldsDinero = document.getElementById('fields-dinero');
  const fieldsLocation = document.getElementById('fields-location');

  const locationInput = document.getElementById('id_location');
  const latInput = document.getElementById('id_lat');
  const lngInput = document.getElementById('id_lng');

  function toggleFields() {
    const isMoney = categorySelect.value === 'dinero';

    if (fieldsDinero) fieldsDinero.style.display = isMoney ? 'block' : 'none';
    if (fieldsLocation) fieldsLocation.style.display = isMoney ? 'none' : 'block';

    // Desactivar los campos ocultos para que no bloqueen el envío
    if (isMoney) {
      if (locationInput) locationInput.disabled = true;
      if (latInput) latInput.disabled = true;
      if (lngInput) lngInput.disabled = true;
    } else {
      if (locationInput) locationInput.disabled = false;
      if (latInput) latInput.disabled = false;
      if (lngInput) lngInput.disabled = false;
    }
  }

  categorySelect.addEventListener('change', toggleFields);
  toggleFields(); // Ejecutar al cargar la página
});
