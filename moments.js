(() => {
  const track = document.querySelector('.moments-track');
  if (!track) return;
  const cards = [...track.children];
  const previous = document.querySelector('[data-moment-prev]');
  const next = document.querySelector('[data-moment-next]');
  const status = document.querySelector('.moments-status');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const update = () => {
    const index = cards.reduce((best, card, i) => Math.abs(card.offsetLeft - cards[0].offsetLeft - track.scrollLeft) < Math.abs(cards[best].offsetLeft - cards[0].offsetLeft - track.scrollLeft) ? i : best, 0);
    previous.disabled = track.scrollLeft < 2;
    next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 2;
    status.textContent = `${index + 1} / ${cards.length}`;
  };
  const move = direction => track.scrollBy({left: direction * (cards[1].offsetLeft - cards[0].offsetLeft), behavior: reducedMotion.matches ? 'instant' : 'smooth'});
  previous.addEventListener('click', () => move(-1));
  next.addEventListener('click', () => move(1));
  track.addEventListener('scroll', update, {passive: true});
  track.addEventListener('keydown', event => {
    if (event.target !== track || !['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
    event.preventDefault(); move(event.key === 'ArrowLeft' ? -1 : 1);
  });
  const videos = [...track.querySelectorAll('video')];
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if (!entry.isIntersecting) entry.target.pause();
  }), {threshold: 0.25});
  videos.forEach(video => observer.observe(video));
  document.addEventListener('visibilitychange', () => {if (document.hidden) videos.forEach(video => video.pause());});
  window.addEventListener('resize', update);
  update();
})();
