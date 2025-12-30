window.mermaid = window.mermaid || {};
window.addEventListener("load", () => {
  if (window.mermaid && window.mermaid.initialize) {
    window.mermaid.initialize({ startOnLoad: true });
  }
});
