(() => {
  const grid = document.querySelector('.menu-grid');
  if (!grid) return;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let navigating = false;
  let timer;

  const reset = () => {
    clearTimeout(timer);
    navigating = false;
    grid.classList.remove('is-navigating');
    grid.querySelectorAll('.is-opening').forEach(tile => tile.classList.remove('is-opening'));
  };
  window.addEventListener('pageshow', reset);

  grid.addEventListener('click', event => {
    const tile = event.target.closest('a.menu-tile');
    if (!tile || event.defaultPrevented || event.button !== 0 ||
        event.metaKey || event.ctrlKey || event.shiftKey || event.altKey ||
        tile.hasAttribute('download') || (tile.target && tile.target !== '_self') ||
        reducedMotion.matches) return;
    const destination = new URL(tile.href, window.location.href);
    if (destination.origin !== window.location.origin) return;
    event.preventDefault();
    if (navigating) return;
    navigating = true;
    grid.classList.add('is-navigating');
    tile.classList.add('is-opening');
    // A short, bounded transition preserves normal links and keyboard activation.
    timer = window.setTimeout(() => window.location.assign(destination.href), 240);
  });
})();
