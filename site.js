// Shared behaviour: mobile menu, testimonial carousel, resources filter, contact form.
(function () {
  'use strict';

  // ---- Contact form backend -------------------------------------------------
  // Create a free form at https://formspree.io (or Basin / Web3Forms) and paste its
  // endpoint here, e.g. 'https://formspree.io/f/abcdwxyz'. Empty = fall back to a
  // pre-filled mailto: so the form still works on day one.
  var FORM_ENDPOINT = '';
  var EMAIL = 'office@megmaginnlcsw.com';

  // ---- mobile menu ----
  var top = document.getElementById('top');
  var burger = top && top.querySelector('.burger');
  if (burger) {
    burger.addEventListener('click', function () {
      var open = top.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
  }

  // ---- testimonial carousel (scroll-snap track + arrows + dots) ----
  var track = document.getElementById('track');
  if (track) {
    var slides = Array.prototype.slice.call(track.children);
    var dots = document.getElementById('qdots');
    var btns = slides.map(function (s, i) {
      var b = document.createElement('button'); b.type = 'button';
      b.setAttribute('aria-label', 'Testimonial ' + (i + 1));
      b.addEventListener('click', function () { go(i); });
      dots.appendChild(b); return b;
    });
    var cur = 0;
    function go(i) {
      cur = (i + slides.length) % slides.length;
      track.scrollTo({ left: slides[cur].offsetLeft - track.offsetLeft, behavior: 'smooth' });
    }
    function mark() {
      var x = track.scrollLeft + track.clientWidth / 2;
      slides.forEach(function (s, i) {
        var on = x >= s.offsetLeft && x < s.offsetLeft + s.offsetWidth;
        if (on) cur = i;
        if (on) btns[i].setAttribute('aria-current', 'true'); else btns[i].removeAttribute('aria-current');
      });
    }
    document.querySelector('.qnav.prev').addEventListener('click', function () { go(cur - 1); });
    document.querySelector('.qnav.next').addEventListener('click', function () { go(cur + 1); });
    track.addEventListener('scroll', function () { window.requestAnimationFrame(mark); }, { passive: true });
    mark();
  }

  // ---- resources: category filter via ?c=slug ----
  var posts = document.getElementById('posts');
  if (posts) {
    var filters = document.getElementById('filters');
    function apply(cat) {
      Array.prototype.forEach.call(posts.children, function (p) {
        p.classList.toggle('hide', !!cat && p.getAttribute('data-cat') !== cat);
      });
      Array.prototype.forEach.call(filters.querySelectorAll('a'), function (a) {
        if ((a.getAttribute('data-cat') || '') === (cat || '')) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
      });
    }
    filters.addEventListener('click', function (e) {
      var a = e.target.closest('a'); if (!a) return;
      e.preventDefault();
      var cat = a.getAttribute('data-cat') || '';
      history.replaceState(null, '', cat ? '?c=' + cat : location.pathname);
      apply(cat);
    });
    apply(new URLSearchParams(location.search).get('c') || '');
  }

  // ---- contact form ----
  var form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var f = new FormData(form);
      if (!FORM_ENDPOINT) {
        var body = 'Name: ' + f.get('name') + '\nEmail: ' + f.get('email') + '\nLocation/State: ' + f.get('location') + '\n\nI want to...\n' + f.get('message');
        location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent('Website inquiry from ' + f.get('name')) + '&body=' + encodeURIComponent(body);
        return;
      }
      var btn = form.querySelector('button[type=submit]'); btn.disabled = true; btn.textContent = 'Sending…';
      fetch(FORM_ENDPOINT, { method: 'POST', body: f, headers: { Accept: 'application/json' } })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function () {
          form.innerHTML = '<p class="ok"><strong>Thank you.</strong> Your message was sent; Meg will get back to you shortly.</p>';
        })
        .catch(function () {
          btn.disabled = false; btn.textContent = 'Send';
          alert('Sorry, the message could not be sent. Please e-mail ' + EMAIL + ' or call instead.');
        });
    });
  }
})();
