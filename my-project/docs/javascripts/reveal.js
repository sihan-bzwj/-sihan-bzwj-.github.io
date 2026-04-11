(() => {
  // Reveal cards and sections when they enter the viewport.
  const revealTargets = () => Array.from(document.querySelectorAll("[data-reveal]"));

  const activateReveals = () => {
    const nodes = revealTargets();
    if (!nodes.length) {
      return;
    }

    if (!("IntersectionObserver" in window)) {
      nodes.forEach((node) => node.classList.add("is-visible"));
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) {
            return;
          }
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      {
        rootMargin: "0px 0px -10% 0px",
        threshold: 0.15,
      },
    );

    nodes.forEach((node) => observer.observe(node));
  };

  if (typeof document$ !== "undefined" && document$ && typeof document$.subscribe === "function") {
    document$.subscribe(activateReveals);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", activateReveals);
  } else {
    activateReveals();
  }
})();
