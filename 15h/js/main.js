/* Hradčany 15h — shared JS: language toggle, mobile nav, gallery lightbox */
(function () {
  // ---------- language ----------
  // Jazyk stranky urcuje <html lang>. Ceska verze je v korenu, ostatni
  // jazyky maji vlastni slozky (en/ fr/ de/ es/) generovane build-jazyky.py,
  // takze se uz nic neprepina za behu.
  var lang = (document.documentElement.lang || 'cs').slice(0, 2);

  function applyLang(l) {
    lang = l;
    document.body.classList.remove('lang-cs', 'lang-en', 'lang-fr', 'lang-de', 'lang-es');
    document.body.classList.add('lang-' + l);
    document.documentElement.lang = l;
    var tt = document.querySelector('title');
    if (tt && tt.dataset && tt.dataset[l]) document.title = tt.dataset[l];
  }

  document.addEventListener('DOMContentLoaded', function () {
    applyLang(lang);

    var t = document.querySelector('.nav-toggle');
    if (t) t.addEventListener('click', function () {
      document.querySelector('.nav-inner').classList.toggle('open');
    });

    initGallery();
    initHoverZoom();
  });

  // ---------- hover loupe on gallery cells ----------
  function initHoverZoom() {
    if (!document.querySelector('.gallery .cell')) return;
    document.addEventListener('mouseover', function (e) {
      var cell = e.target.closest ? e.target.closest('.gallery .cell') : null;
      if (!cell) return;
      var img = cell.querySelector('img');
      if (img && cell.dataset.full && img.dataset.hi !== '1') {
        img.dataset.hi = '1';
        img.src = cell.dataset.full;   // swap thumb -> full res for real detail
      }
    });
    document.addEventListener('mousemove', function (e) {
      var cell = e.target.closest ? e.target.closest('.gallery .cell') : null;
      if (!cell) return;
      var img = cell.querySelector('img');
      if (!img) return;
      var r = cell.getBoundingClientRect();
      var x = Math.max(0, Math.min(100, (e.clientX - r.left) / r.width * 100));
      var y = Math.max(0, Math.min(100, (e.clientY - r.top) / r.height * 100));
      img.style.transformOrigin = x + '% ' + y + '%';
    });
  }

  // ---------- gallery / lightbox ----------
  function initGallery() {
    var cells = Array.prototype.slice.call(document.querySelectorAll('.gallery .cell'));
    if (!cells.length) return;

    var lb = document.createElement('div');
    lb.className = 'lightbox';
    lb.innerHTML =
      '<button class="close" aria-label="close">&times;</button>' +
      '<button class="prev" aria-label="previous">&#8249;</button>' +
      '<button class="next" aria-label="next">&#8250;</button>' +
      '<img alt="">' +
      '<div class="cap"></div>';
    document.body.appendChild(lb);

    var img = lb.querySelector('img');
    var cap = lb.querySelector('.cap');
    var idx = -1;

    function show(i) {
      idx = (i + cells.length) % cells.length;
      var c = cells[idx];
      img.src = c.dataset.full;
      var tags = c.dataset.tags ? '<div class="tags">' + c.dataset.tags + '</div>' : '';
      cap.innerHTML = '<strong>' + c.dataset.cap + '</strong>' + tags;
      lb.classList.add('open');
    }
    function close() { lb.classList.remove('open'); img.src = ''; }

    cells.forEach(function (c, i) {
      c.addEventListener('click', function () { show(i); });
    });
    lb.querySelector('.close').addEventListener('click', close);
    lb.querySelector('.prev').addEventListener('click', function (e) { e.stopPropagation(); show(idx - 1); });
    lb.querySelector('.next').addEventListener('click', function (e) { e.stopPropagation(); show(idx + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(idx - 1);
      if (e.key === 'ArrowRight') show(idx + 1);
    });

    // position filter
    var filter = document.getElementById('posFilter');
    if (filter) {
      filter.addEventListener('input', function () {
        var v = filter.value.trim();
        cells.forEach(function (c) {
          c.style.display = (!v || c.dataset.pos === v || c.dataset.pos === ('0' + v) || parseInt(c.dataset.pos, 10) === parseInt(v, 10)) ? '' : 'none';
        });
      });
    }
  }
})();
