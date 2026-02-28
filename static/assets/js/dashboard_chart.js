document.addEventListener("DOMContentLoaded", () => {
  const chartDataElement = document.getElementById("chart-data");
  if (!chartDataElement) return;

  const data = JSON.parse(chartDataElement.textContent);
  const ctx = document.getElementById("activityChart");

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: "Estadísticas de Actividad",
          data: data.values,
          backgroundColor: ["#81c784", "#66bb6a", "#388e3c"],
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true },
      },
    },
  });
});
