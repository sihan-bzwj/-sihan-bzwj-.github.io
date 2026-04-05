(() => {
  const COUNTER_NAMESPACE = "sihan-bzwj-github-io";
  const COUNTER_KEY = "site";
  const STORAGE_KEY = "sihan-bzwj-visitor-count";

  const renderCount = (value) => {
    document.querySelectorAll("[data-visitor-count]").forEach((node) => {
      node.textContent = String(value);
    });
  };

  const loadCount = async () => {
    const cachedValue = localStorage.getItem(STORAGE_KEY);
    if (cachedValue) {
      renderCount(cachedValue);
      return;
    }

    try {
      const response = await fetch(
        `https://api.countapi.xyz/hit/${COUNTER_NAMESPACE}/${COUNTER_KEY}`,
        { cache: "no-store" },
      );
      const payload = await response.json();
      const value = payload.value ?? payload.count ?? payload.visits ?? "";
      if (value !== "") {
        const text = String(value);
        localStorage.setItem(STORAGE_KEY, text);
        renderCount(text);
        return;
      }
    } catch (error) {
      void error;
    }

    renderCount(cachedValue || "--");
  };

  const refresh = () => {
    if (!document.querySelector("[data-visitor-count]")) {
      return;
    }
    void loadCount();
  };

  if (typeof document$ !== "undefined" && document$ && typeof document$.subscribe === "function") {
    document$.subscribe(refresh);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", refresh);
  } else {
    refresh();
  }
})();
