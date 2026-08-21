/**
 * StudIQ - Agenciy Framer Inspired Scroll & Micro-Interaction Engine
 * Uses lightweight IntersectionObserver with passive listeners and reduced-motion detection.
 */

(function () {
  'use strict';

  function initScrollAnimations() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      document.querySelectorAll('.reveal-on-scroll').forEach(function (el) {
        el.classList.add('is-revealed');
      });
      return;
    }

    var observerOptions = {
      root: null,
      rootMargin: '0px 0px -60px 0px',
      threshold: 0.12
    };

    var observer = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-revealed');
          obs.unobserve(entry.target);
        }
      });
    }, observerOptions);

    document.querySelectorAll('.reveal-on-scroll').forEach(function (el) {
      observer.observe(el);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initScrollAnimations);
  } else {
    initScrollAnimations();
  }

  // Support dynamic Dash page loads
  var mutationObserver = new MutationObserver(function () {
    initScrollAnimations();
  });

  if (document.body) {
    mutationObserver.observe(document.body, { childList: true, subtree: true });
  }
})();
