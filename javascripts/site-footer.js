(() => {
  const API_TIMEOUT = 5000; // 5 seconds timeout
  const CACHE_KEY = "sihan-bzwj-visitor-last-fetch";

  const renderCount = (value) => {
    document.querySelectorAll("[data-visitor-count]").forEach((node) => {
      node.textContent = String(value);
    });
  };

  const loadCount = async () => {
    try {
      // Create abort controller for timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);

      // Determine API URL based on current location
      const baseUrl = window.location.origin;
      const apiUrl = `${baseUrl}/api/visitor-count`;

      const response = await fetch(apiUrl, {
        method: "GET",
        cache: "no-store",
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const payload = await response.json();
      const count = payload.count;

      if (typeof count === "number" && count > 0) {
        const countStr = String(count);
        renderCount(countStr);
        localStorage.setItem(CACHE_KEY, countStr);
        return;
      }
    } catch (error) {
      // Network error or timeout - silently fail
      void error;
    }

    // Fall back to previously cached value if available
    const cached = localStorage.getItem(CACHE_KEY);
    if (cached) {
      renderCount(cached);
    } else {
      renderCount("--");
    }
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
