(() => {
  const STORAGE_KEY = "sihan-bzwj-github-stars";
  const CACHE_EXPIRY_KEY = "sihan-bzwj-github-stars-expiry";
  const CACHE_DURATION = 3600000; // 1 hour in milliseconds
  const API_TIMEOUT = 5000; // 5 seconds timeout

  const renderCount = (value) => {
    document.querySelectorAll("[data-visitor-count]").forEach((node) => {
      node.textContent = String(value);
    });
  };

  const loadCount = async () => {
    // Try to use cached value first
    const cachedValue = localStorage.getItem(STORAGE_KEY);
    const cacheExpiry = localStorage.getItem(CACHE_EXPIRY_KEY);
    const now = Date.now();

    if (cachedValue && cacheExpiry && now < parseInt(cacheExpiry)) {
      renderCount(cachedValue);
      return;
    }

    // Show placeholder while loading
    if (cachedValue) {
      renderCount(cachedValue);
    } else {
      renderCount("加载中...");
    }

    try {
      // Fetch GitHub repository stars
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);

      const response = await fetch(
        "https://api.github.com/repos/sihan-bzwj/-sihan-bzwj-.github.io",
        {
          headers: { "Accept": "application/vnd.github.v3+json" },
          signal: controller.signal,
        }
      );

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`GitHub API error: ${response.status}`);
      }

      const data = await response.json();
      const starCount = data.stargazers_count;

      if (typeof starCount === "number" && starCount >= 0) {
        const text = String(starCount);
        localStorage.setItem(STORAGE_KEY, text);
        localStorage.setItem(CACHE_EXPIRY_KEY, String(now + CACHE_DURATION));
        renderCount(text);
        return;
      }
    } catch (error) {
      // Silently fail - use cached value or default
      void error;
    }

    // Fall back to cached value or show default
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
