document.addEventListener("DOMContentLoaded", () => {
  const tabs = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");
  const openWizard = document.getElementById("openWizardBtn");
  const closeWizard = document.getElementById("closeWizardBtn");
  const wizardModal = document.getElementById("wizardModal");
  const steps = document.querySelectorAll(".wizard-step");
  const indicators = document.querySelectorAll(".step-indicator");
  const nextBtn = document.getElementById("nextStep");
  const prevBtn = document.getElementById("prevStep");
  const form = document.getElementById("helpForm");

  let currentStep = 0;
  let sending = false;

  // === Tabs control ===
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      tabContents.forEach(c => c.classList.remove("active"));
      document.getElementById(`tab-${tab.dataset.tab}`).classList.add("active");
    });
  });

  // === Modal control ===
  openWizard?.addEventListener("click", () => {
    wizardModal.style.display = "flex";
    document.body.style.overflow = "hidden";
    resetWizard();
  });

  closeWizard?.addEventListener("click", closeModal);

  function closeModal() {
    wizardModal.style.display = "none";
    document.body.style.overflow = "auto";
  }

  function resetWizard() {
    currentStep = 0;
    sending = false;
    updateSteps();
  }

  // === Navegación entre pasos ===
  nextBtn.addEventListener("click", () => {
    if (sending) return;

    if (currentStep < steps.length - 1) {
      currentStep++;
      updateSteps();
    } else {
      // ✅ Enviar solo una vez
      sending = true;
      nextBtn.disabled = true;
      nextBtn.textContent = "Enviando...";
      form.submit();
    }
  });

  prevBtn.addEventListener("click", () => {
    if (currentStep > 0) {
      currentStep--;
      updateSteps();
    }
  });

  // === Actualiza visibilidad y botones ===
  function updateSteps() {
    steps.forEach((s, i) => s.classList.toggle("active", i === currentStep));
    indicators.forEach((ind, i) => ind.classList.toggle("active", i <= currentStep));

    prevBtn.style.visibility = currentStep === 0 ? "hidden" : "visible";

    // Si es el último paso, cambiar texto y ocultar botón “Publicar” duplicado
    nextBtn.textContent = currentStep === steps.length - 1 ? "Publicar Solicitud" : "Siguiente";

    // Ocultar el botón submit directo si existe en HTML
    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) {
      submitBtn.style.display = currentStep === steps.length - 1 ? "none" : "none";
    }
  }

  updateSteps();
});



document.addEventListener("DOMContentLoaded", function () {
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get("open_modal") === "true") {
    // abre el modal automáticamente
    const wizardModal = document.getElementById("wizardModal");
    if (wizardModal) {
      wizardModal.style.display = "flex";
      document.body.style.overflow = "hidden";
    }
  }
});
