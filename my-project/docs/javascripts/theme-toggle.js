(() => {
  const STORAGE_KEY = "sihan-theme";
  const root = document.documentElement;

  // Reuse the saved choice when available, otherwise follow the system theme.
  const resolveTheme = () => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === "dark" || saved === "light") {
      return saved;
    }
    return window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
  };

  const applyTheme = (theme) => {
    root.dataset.theme = theme;
    const label = theme === "light" ? "Light" : "Dark";
    document.querySelectorAll("[data-theme-label]").forEach((node) => {
      node.textContent = label;
    });
    document.querySelectorAll("[data-theme-toggle]").forEach((node) => {
      node.setAttribute("aria-pressed", theme === "light" ? "true" : "false");
      node.setAttribute("title", theme === "light" ? "Switch to dark mode" : "Switch to light mode");
    });
  };

  const bindThemeToggle = () => {
    applyTheme(resolveTheme());

    document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
      if (button.dataset.themeBound === "true") {
        return;
      }
      button.dataset.themeBound = "true";
      // Material can replace page content during navigation, so guard against double binding.
      button.addEventListener("click", () => {
        const nextTheme = root.dataset.theme === "light" ? "dark" : "light";
        localStorage.setItem(STORAGE_KEY, nextTheme);
        applyTheme(nextTheme);
      });
    });
  };

  root.dataset.theme = resolveTheme();

  if (typeof document$ !== "undefined" && document$ && typeof document$.subscribe === "function") {
    document$.subscribe(bindThemeToggle);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bindThemeToggle);
  } else {
    bindThemeToggle();
  }
})();
