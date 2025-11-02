let map, marker;

document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("mapModal");

  modal.addEventListener("shown.bs.modal", () => {
    if (!map) {
      map = L.map("map").setView([-2.145, -79.600], 13);

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(map);

      map.on("click", (e) => {
        const { lat, lng } = e.latlng;

        if (marker) {
          marker.setLatLng(e.latlng);
        } else {
          marker = L.marker(e.latlng).addTo(map);
        }

        // Fill form fields
        document.getElementById("id_lat").value = lat;
        document.getElementById("id_lng").value = lng;
        document.getElementById("id_location").value = `Lat: ${lat.toFixed(5)}, Lng: ${lng.toFixed(5)}`;
      });
    }

    // Fix map rendering inside modal
    setTimeout(() => map.invalidateSize(), 300);
  });
});

function initAutocomplete() {
  const input = document.getElementById('id_location');
  const latInput = document.getElementById('id_lat');
  const lngInput = document.getElementById('id_lng');

  if (!input) return;

  // Inicializa el Autocomplete de Google Places
  const autocomplete = new google.maps.places.Autocomplete(input, {
    componentRestrictions: { country: "ec" }, // puedes cambiar a tu país
    fields: ["geometry", "formatted_address"],
  });

  autocomplete.addListener("place_changed", () => {
    const place = autocomplete.getPlace();
    if (!place.geometry) return;

    // Guarda coordenadas en los campos ocultos
    const lat = place.geometry.location.lat();
    const lng = place.geometry.location.lng();
    latInput.value = lat;
    lngInput.value = lng;

    console.log("📍 Dirección:", place.formatted_address);
    console.log("Lat:", lat, "Lng:", lng);
  });
}

// Inicializar cuando cargue la página
document.addEventListener("DOMContentLoaded", initAutocomplete);
