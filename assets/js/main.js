/* ============================================================
   Rossi Sho — Art Portfolio
   Gallery rendering, filtering and lightbox.
   Depends on WORKS (assets/js/works.js).
   ============================================================ */
(function () {
  "use strict";

  var SECTIONS = ["fish-game", "creatures", "illustration", "commissions"];

  /* ---------- build the grids ---------- */

  function tile(work, index) {
    var btn = document.createElement("button");
    btn.className = "tile reveal";
    btn.type = "button";
    btn.dataset.index = index;
    btn.setAttribute("aria-label", "View " + work.title);

    var tags = work.tags.map(function (t) {
      return "<li>" + t + "</li>";
    }).join("");

    btn.innerHTML =
      '<div class="tile__media">' +
        '<img src="' + work.thumb + '" alt="' + work.title.replace(/"/g, "&quot;") + '"' +
             ' loading="lazy" decoding="async" width="' + work.w + '" height="' + work.h + '">' +
        '<span class="tile__zoom" aria-hidden="true">⤢</span>' +
      "</div>" +
      '<div class="tile__body">' +
        '<h4 class="tile__title">' + work.title + "</h4>" +
        '<ul class="tile__tags">' + tags + "</ul>" +
      "</div>";

    return btn;
  }

  // Flat, in-DOM order — this is the order the lightbox steps through.
  var ordered = [];
  SECTIONS.forEach(function (section) {
    var grid = document.querySelector('[data-grid="' + section + '"]');
    if (!grid) return;
    WORKS.filter(function (w) { return w.section === section; })
         .forEach(function (w) {
           var i = ordered.push(w) - 1;
           grid.appendChild(tile(w, i));
         });
  });

  /* ---------- filtering ---------- */

  var chips = Array.prototype.slice.call(document.querySelectorAll(".chip"));
  var groups = Array.prototype.slice.call(document.querySelectorAll(".group"));

  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      var filter = chip.dataset.filter;

      chips.forEach(function (c) { c.classList.toggle("is-active", c === chip); });
      groups.forEach(function (g) {
        g.hidden = !(filter === "all" || g.dataset.group === filter);
      });

      // Re-run reveal for anything newly visible.
      document.querySelectorAll(".group:not([hidden]) .reveal:not(.is-in)")
        .forEach(function (el) { observer.observe(el); });
    });
  });

  /* ---------- reveal on scroll ---------- */

  var observer;
  if ("IntersectionObserver" in window) {
    observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        // Stagger within a row for a softer entrance.
        var delay = (Array.prototype.indexOf.call(el.parentNode.children, el) % 5) * 55;
        setTimeout(function () { el.classList.add("is-in"); }, delay);
        observer.unobserve(el);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });

    document.querySelectorAll(".reveal").forEach(function (el) { observer.observe(el); });
  } else {
    observer = { observe: function (el) { el.classList.add("is-in"); }, unobserve: function () {} };
    document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---------- lightbox ---------- */

  var lb        = document.getElementById("lightbox");
  var lbImg     = document.getElementById("lightbox-img");
  var lbTitle   = document.getElementById("lightbox-title");
  var lbText    = document.getElementById("lightbox-text");
  var lbTags    = document.getElementById("lightbox-tags");
  var lbCounter = document.getElementById("lightbox-counter");
  var current   = 0;
  var lastFocus = null;

  function visibleIndices() {
    // Only step through pieces whose group is currently shown.
    return ordered.reduce(function (acc, w, i) {
      var group = document.querySelector('.group[data-group="' + w.section + '"]');
      if (group && !group.hidden) acc.push(i);
      return acc;
    }, []);
  }

  function show(index) {
    var w = ordered[index];
    if (!w) return;
    current = index;

    lbImg.src = w.full;
    lbImg.alt = w.title;
    lbTitle.textContent = w.title;
    lbText.textContent = w.caption;
    lbTags.innerHTML = w.tags.map(function (t) { return "<li>" + t + "</li>"; }).join("");

    var vis = visibleIndices();
    lbCounter.textContent = (vis.indexOf(index) + 1) + " / " + vis.length;
  }

  function open(index) {
    lastFocus = document.activeElement;
    show(index);
    lb.hidden = false;
    document.body.classList.add("lb-open");
    lb.querySelector(".lightbox__close").focus();
  }

  function close() {
    lb.hidden = true;
    document.body.classList.remove("lb-open");
    lbImg.src = "";
    if (lastFocus) lastFocus.focus();
  }

  function step(dir) {
    var vis = visibleIndices();
    if (!vis.length) return;
    var at = vis.indexOf(current);
    show(vis[(at + dir + vis.length) % vis.length]);
  }

  document.addEventListener("click", function (e) {
    var t = e.target.closest(".tile");
    if (t) { open(parseInt(t.dataset.index, 10)); return; }

    if (e.target.closest(".lightbox__close")) return close();
    if (e.target.closest(".lightbox__nav--prev")) return step(-1);
    if (e.target.closest(".lightbox__nav--next")) return step(1);
    // Click the backdrop (but not the figure) to dismiss.
    if (e.target === lb) close();
  });

  document.addEventListener("keydown", function (e) {
    if (lb.hidden) return;
    if (e.key === "Escape")     { close(); }
    else if (e.key === "ArrowLeft")  { step(-1); }
    else if (e.key === "ArrowRight") { step(1); }
    else if (e.key === "Tab") {
      // Trap focus inside the dialog.
      var f = lb.querySelectorAll("button");
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });

  // Swipe between pieces on touch devices.
  var touchX = null;
  lb.addEventListener("touchstart", function (e) { touchX = e.changedTouches[0].clientX; }, { passive: true });
  lb.addEventListener("touchend", function (e) {
    if (touchX === null) return;
    var dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 55) step(dx < 0 ? 1 : -1);
    touchX = null;
  }, { passive: true });

  /* ---------- mobile nav ---------- */

  var toggle = document.querySelector(".nav__toggle");
  var links  = document.getElementById("nav-links");

  toggle.addEventListener("click", function () {
    var open = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!open));
    links.classList.toggle("is-open", !open);
  });

  links.addEventListener("click", function (e) {
    if (e.target.tagName !== "A") return;
    toggle.setAttribute("aria-expanded", "false");
    links.classList.remove("is-open");

    // A section link should also clear any active filter, or the target may be hidden.
    var id = e.target.getAttribute("href").slice(1);
    if (SECTIONS.indexOf(id) !== -1) {
      var chip = document.querySelector('.chip[data-filter="' + id + '"]')
              || document.querySelector('.chip[data-filter="all"]');
      if (chip && !chip.classList.contains("is-active")) chip.click();
    }
  });

  /* ---------- misc ---------- */

  document.getElementById("year").textContent = new Date().getFullYear();

  var countEl = document.querySelector("[data-count]");
  if (countEl) countEl.textContent = ordered.length;
})();
