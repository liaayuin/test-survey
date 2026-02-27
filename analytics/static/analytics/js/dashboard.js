document.addEventListener("DOMContentLoaded", function () {
  Chart.defaults.color = "#94a3b8";
  Chart.defaults.font.family = "'Sora', sans-serif";
  Chart.defaults.plugins.legend.labels.usePointStyle = true;

  fetch("/api/demographics/")
    .then((res) => res.json())
    .then((data) => {
      document.getElementById("total-val").innerText = data.total;
      document.getElementById("awareness-val").innerText =
        data.awareness_rate + "%";
      document.getElementById("engagement-val").innerText =
        data.engagement_rate + "%";

      new Chart(document.getElementById("genderChart"), {
        type: "doughnut",
        data: {
          labels: data.gender.map((x) => x.gender),
          datasets: [
            {
              data: data.gender.map((x) => x.count),
              backgroundColor: ["#00d2ff", "#9d50bb", "#3a1c71"],
              borderWidth: 0,
              borderRadius: 10,
            },
          ],
        },
        options: {
          maintainAspectRatio: false,
          cutout: "82%",
          plugins: { legend: { position: "bottom" } },
        },
      });

      new Chart(document.getElementById("educationChart"), {
        type: "bar",
        data: {
          labels: data.education.map((x) => x.education),
          datasets: [
            {
              data: data.education.map((x) => x.count),
              backgroundColor: "rgba(157, 80, 187, 0.6)",
              borderRadius: 5,
            },
          ],
        },
        options: {
          indexAxis: "y",
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
        },
      });
    });

  fetch("/api/participation/")
    .then((res) => res.json())
    .then((data) => {
      const barrierCtx = document
        .getElementById("barrierChart")
        .getContext("2d");
      const barGradient = barrierCtx.createLinearGradient(0, 0, 500, 0);
      barGradient.addColorStop(0, "#00d2ff");
      barGradient.addColorStop(1, "#3a1c71");

      new Chart(barrierCtx, {
        type: "bar",
        data: {
          labels: data.barriers.map((x) => x.option__value),
          datasets: [
            {
              data: data.barriers.map((x) => x.count),
              backgroundColor: barGradient,
              borderRadius: 8,
              barThickness: 15,
            },
          ],
        },
        options: {
          indexAxis: "y",
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            y: { ticks: { font: { size: 10 } } },
          },
        },
      });

      new Chart(document.getElementById("platformChart"), {
        type: "bar",
        data: {
          labels: data.platforms.map((x) => x.option__value),
          datasets: [
            {
              data: data.platforms.map((x) => x.count),
              backgroundColor: "#00d2ff",
              borderRadius: 10,
            },
          ],
        },
        options: {
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
        },
      });
    });

  fetch("/api/training/")
    .then((res) => res.json())
    .then((data) => {
      const trainingCtx = document
        .getElementById("trainingChart")
        .getContext("2d");
      const areaGradient = trainingCtx.createLinearGradient(0, 0, 0, 300);
      areaGradient.addColorStop(0, "rgba(157, 80, 187, 0.4)");
      areaGradient.addColorStop(1, "rgba(157, 80, 187, 0)");

      new Chart(trainingCtx, {
        type: "line",
        data: {
          labels: data.interests.map((x) => x.option__value),
          datasets: [
            {
              label: "Interest Level",
              data: data.interests.map((x) => x.count),
              borderColor: "#9d50bb",
              borderWidth: 3,
              fill: true,
              backgroundColor: areaGradient,
              tension: 0.4,
              pointBackgroundColor: "#00d2ff",
            },
          ],
        },
        options: {
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: {
              ticks: {
                maxRotation: 45,
                minRotation: 45,
                font: { size: 10 },
              },
            },
          },
        },
      });
    });

  fetch("/api/awareness/")
    .then((res) => res.json())
    .then((data) => {
      new Chart(document.getElementById("awarenessChart"), {
        type: "pie",
        data: {
          labels: data.channels.map((x) => x.option__value),
          datasets: [
            {
              data: data.channels.map((x) => x.count),
              backgroundColor: [
                "#00d2ff",
                "#9d50bb",
                "#6366f1",
                "#f43f5e",
                "#10b981",
              ],
              borderWidth: 0,
            },
          ],
        },
        options: {
          maintainAspectRatio: false,
          plugins: {
            legend: { position: "right", labels: { font: { size: 10 } } },
          },
        },
      });
    });
  fetch("/api/age-dist/")
    .then((res) => res.json())
    .then((data) => {
      new Chart(document.getElementById("ageChart"), {
        type: "bar",
        data: {
          labels: data.results.map((x) => x.age_range),
          datasets: [
            {
              label: "Respondents",
              data: data.results.map((x) => x.count),
              backgroundColor: "#9d50bb",
              borderRadius: 10,
            },
          ],
        },
        options: { maintainAspectRatio: false },
      });
    });

  fetch("/api/subcity/")
    .then((res) => res.json())
    .then((data) => {
      new Chart(document.getElementById("subcityChart"), {
        type: "polarArea",
        data: {
          labels: data.results.map((x) => x.sub_city),
          datasets: [
            {
              data: data.results.map((x) => x.count),
              backgroundColor: ["#00d2ff", "#9d50bb", "#6366f1", "#f43f5e"],
            },
          ],
        },
        options: { maintainAspectRatio: false },
      });
    });

  document
    .getElementById("download-pdf")
    .addEventListener("click", function () {
      const element = document.getElementById("report-content");

      setTimeout(() => {
        const opt = {
          filename: "Youth Network Ethiopia_Analytics_Report.pdf",
          image: { type: "jpeg", quality: 0.98 },
          html2canvas: {
            scale: 2,
            useCORS: true,
            backgroundColor: "#0b0e14",
          },
          jsPDF: {
            unit: "in",
            format: "letter",
            orientation: "portrait",
          },
          pagebreak: { mode: ["avoid-all"] },
        };

        html2pdf().set(opt).from(element).save();
      });
    });
});
