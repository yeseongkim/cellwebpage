(function () {
  const root = document.documentElement;
  const themeBtn = document.getElementById("themeBtn");
  const themeLabel = document.getElementById("themeLabel");
  const savedTheme = localStorage.getItem("cell-project-theme") || "dark";

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    localStorage.setItem("cell-project-theme", theme);
    if (themeLabel) {
      themeLabel.textContent = theme === "dark" ? "Light" : "Dark";
    }
  }

  applyTheme(savedTheme);

  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      const nextTheme = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      applyTheme(nextTheme);
    });
  }

  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
        }
      });
    },
    { threshold: 0.12 }
  );

  document.querySelectorAll(".reveal").forEach((node) => revealObserver.observe(node));

  const navLinks = Array.from(document.querySelectorAll(".nav-link"));
  const navObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }
        navLinks.forEach((link) => link.classList.remove("active"));
        const active = document.querySelector('.nav-link[href="#' + entry.target.id + '"]');
        if (active) {
          active.classList.add("active");
        }
      });
    },
    { threshold: 0.35 }
  );

  document.querySelectorAll("section[id]").forEach((section) => navObserver.observe(section));

  document.querySelectorAll("[data-copy-target]").forEach((button) => {
    button.addEventListener("click", async function () {
      const targetId = button.getAttribute("data-copy-target");
      const target = document.getElementById(targetId);
      if (!target) {
        return;
      }
      try {
        await navigator.clipboard.writeText(target.textContent || "");
        const original = button.textContent;
        button.textContent = "Copied";
        window.setTimeout(() => {
          button.textContent = original;
        }, 1200);
      } catch (err) {
        button.textContent = "Unavailable";
      }
    });
  });
})();
