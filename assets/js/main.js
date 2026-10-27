/* ============================================================
   Rossi Sho — Art Portfolio
   Gallery rendering, filtering, album slideshows and lightbox.
   Depends on WORKS and ALBUMS (assets/js/works.js).
   ============================================================ */
(function () {
  "use strict";

  var SECTIONS = ["fish-game", "fanart", "illustration", "commissions"];

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
                    .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  /* ----------------------------------------------------------
     Build the playlists the viewer steps through.
     - Standalone pieces live in one flat list per section.
     - Each album is its own list, so arrows stay inside the set.
     ---------------------------------------------------------- */

  var standalone = WORKS.filter(function (w) { return !w.album; });

  var albumSlides = {};   // album id -> [work, ...] in manifest order
  WORKS.forEach(function (w) {
    if (!w.album) return;
    (albumSlides[w.album] = albumSlides[w.album] || []).push(w);
  });

  // playlists["standalone"] and playlists["<albumId>"]
  var playlists = { standalone: standalone };
  Object.keys(albumSlides).forEach(function (id) { playlists[id] = albumSlides[id]; });

  /* ---------------- tiles ---------------- */

  function pieceTile(work) {
    var btn = document.createElement("button");
    btn.className = "tile reveal";
    btn.type = "button";
    btn.dataset.list = "standalone";
    btn.dataset.index = standalone.indexOf(work);
    btn.setAttribute("aria-label", "View " + work.title);

    btn.innerHTML =
      '<div class="tile__media">' +
        '<img src="' + work.thumb + '" alt="' + esc(work.title) + '"' +
             ' loading="lazy" decoding="async" width="' + work.w + '" height="' + work.h + '">' +
        '<span class="tile__zoom" aria-hidden="true">⤢</span>' +
      "</div>" +
      '<div class="tile__body">' +
        '<h5 class="tile__title">' + esc(work.title) + "</h5>" +
        '<ul class="tile__tags">' +
          work.tags.map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("") +
        "</ul>" +
      "</div>";
    return btn;
  }

  function albumTile(id, album) {
    var slides = albumSlides[id] || [];
    var cover  = WORKS.filter(function (w) { return w.slug === album.cover; })[0] || slides[0];
    if (!cover) return null;

    var btn = document.createElement("button");
    btn.className = "tile tile--album reveal";
    btn.type = "button";
    btn.dataset.list = id;
    btn.dataset.index = "0";
    btn.setAttribute("aria-label", "Open " + album.title + ", " + slides.length + " images");

    // Up to two peeking thumbnails behind the cover to signal depth.
    var peeks = slides.slice(1, 3).map(function (s, i) {
      return '<span class="tile__peek tile__peek--' + (i + 1) + '"' +
             ' style="background-image:url(' + s.thumb + ')"></span>';
    }).join("");

    btn.innerHTML =
      '<div class="tile__stack">' + peeks +
        '<div class="tile__media">' +
          '<img src="' + cover.thumb + '" alt="' + esc(album.title) + '"' +
               ' loading="lazy" decoding="async" width="' + cover.w + '" height="' + cover.h + '">' +
          '<span class="tile__count">' + slides.length + ' images</span>' +
          '<span class="tile__zoom" aria-hidden="true">⤢</span>' +
        "</div>" +
      "</div>" +
      '<div class="tile__body">' +
        '<h5 class="tile__title">' + esc(album.title) + "</h5>" +
        '<ul class="tile__tags">' +
          album.tags.map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("") +
        "</ul>" +
      "</div>";
    return btn;
  }

  /* ---------------- render ---------------- */

  SECTIONS.forEach(function (section) {
    var albumGrid = document.querySelector('[data-albums="' + section + '"]');
    if (albumGrid) {
      Object.keys(ALBUMS).forEach(function (id) {
        if (ALBUMS[id].section !== section) return;
        var t = albumTile(id, ALBUMS[id]);
        if (t) albumGrid.appendChild(t);
      });
    }

    var grid = document.querySelector('[data-grid="' + section + '"]');
    if (grid) {
      standalone.filter(function (w) { return w.section === section; })
                .forEach(function (w) { grid.appendChild(pieceTile(w)); });
    }
  });

  /* ---------------- filtering ---------------- */

  var chips  = Array.prototype.slice.call(document.querySelectorAll(".chip"));
  var groups = Array.prototype.slice.call(document.querySelectorAll(".group"));

  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      var filter = chip.dataset.filter;
      chips.forEach(function (c) { c.classList.toggle("is-active", c === chip); });
      groups.forEach(function (g) {
        g.hidden = !(filter === "all" || g.dataset.group === filter);
      });
      document.querySelectorAll(".group:not([hidden]) .reveal:not(.is-in)")
        .forEach(function (el) { observer.observe(el); });
    });
  });

  /* ---------------- reveal on scroll ---------------- */

  var observer;
  if ("IntersectionObserver" in window) {
    observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
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

  /* ---------------- lightbox ---------------- */

  var lb        = document.getElementById("lightbox");
  var lbImg     = document.getElementById("lightbox-img");
  var lbAlbum   = document.getElementById("lightbox-album");
  var lbTitle   = document.getElementById("lightbox-title");
  var lbText    = document.getElementById("lightbox-text");
  var lbTags    = document.getElementById("lightbox-tags");
  var lbDots    = document.getElementById("lightbox-dots");
  var lbCounter = document.getElementById("lightbox-counter");

  var listId    = "standalone";
  var cursor    = 0;
  var lastFocus = null;

  function activeList() {
    if (listId === "standalone") {
      // Only step through pieces whose group is currently visible.
      return standalone.filter(function (w) {
        var g = document.querySelector('.group[data-group="' + w.section + '"]');
        return g && !g.hidden;
      });
    }
    return playlists[listId] || [];
  }

  function show(index, dir) {
    var list = activeList();
    if (!list.length) return;
    cursor = (index + list.length) % list.length;
    var w = list[cursor];
    var album = listId !== "standalone" ? ALBUMS[listId] : null;

    if (dir) {
      lbImg.classList.remove("slide-l", "slide-r");
      // Force reflow so the animation re-triggers on repeated presses.
      void lbImg.offsetWidth;
      lbImg.classList.add(dir > 0 ? "slide-l" : "slide-r");
    }

    lbImg.src = w.full;
    lbImg.alt = w.title;

    if (album) {
      lbAlbum.textContent = album.title;
      lbAlbum.hidden = false;
      lbText.textContent = w.caption + " — " + album.caption;
    } else {
      lbAlbum.hidden = true;
      lbText.textContent = w.caption;
    }

    lbTitle.textContent = w.title;
    lbTags.innerHTML = (album ? album.tags : w.tags)
      .map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("");

    if (album) {
      lbDots.hidden = false;
      lbDots.innerHTML = list.map(function (s, i) {
        return '<button class="dot' + (i === cursor ? " is-on" : "") + '"' +
               ' data-dot="' + i + '" aria-label="Go to image ' + (i + 1) + '"></button>';
      }).join("");
    } else {
      lbDots.hidden = true;
      lbDots.innerHTML = "";
    }

    lbCounter.textContent = (cursor + 1) + " / " + list.length;
    lb.classList.toggle("is-album", !!album);
  }

  function open(id, index) {
    lastFocus = document.activeElement;
    listId = id;
    lb.hidden = false;
    document.body.classList.add("lb-open");
    show(index, 0);
    lb.querySelector(".lightbox__close").focus();
  }

  function close() {
    lb.hidden = true;
    document.body.classList.remove("lb-open");
    lbImg.src = "";
    if (lastFocus) lastFocus.focus();
  }

  function step(dir) { show(cursor + dir, dir); }

  document.addEventListener("click", function (e) {
    var tile = e.target.closest(".tile");
    if (tile) {
      var list = tile.dataset.list;
      var idx  = parseInt(tile.dataset.index, 10);
      if (list === "standalone") {
        // Map the manifest index onto the currently visible subset.
        var w = standalone[idx];
        listId = "standalone";
        idx = Math.max(0, activeList().indexOf(w));
      }
      open(list, idx);
      return;
    }

    var dot = e.target.closest("[data-dot]");
    if (dot) return show(parseInt(dot.dataset.dot, 10), 0);

    if (e.target.closest(".lightbox__close")) return close();
    if (e.target.closest(".lightbox__nav--prev")) return step(-1);
    if (e.target.closest(".lightbox__nav--next")) return step(1);
    if (e.target === lb || e.target.closest(".lightbox__stage") === e.target) {
      if (e.target === lb) close();
    }
  });

  document.addEventListener("keydown", function (e) {
    if (lb.hidden) return;
    if (e.key === "Escape") { close(); }
    else if (e.key === "ArrowLeft")  { step(-1); }
    else if (e.key === "ArrowRight") { step(1); }
    else if (e.key === "Tab") {
      var f = lb.querySelectorAll("button:not([disabled])");
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });

  // Swipe between slides on touch devices.
  var touchX = null;
  lb.addEventListener("touchstart", function (e) { touchX = e.changedTouches[0].clientX; }, { passive: true });
  lb.addEventListener("touchend", function (e) {
    if (touchX === null) return;
    var dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 55) step(dx < 0 ? 1 : -1);
    touchX = null;
  }, { passive: true });

  /* ---------------- mobile nav ---------------- */

  var toggle = document.querySelector(".nav__toggle");
  var links  = document.getElementById("nav-links");

  toggle.addEventListener("click", function () {
    var isOpen = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!isOpen));
    links.classList.toggle("is-open", !isOpen);
  });

  links.addEventListener("click", function (e) {
    var a = e.target.closest("a");
    if (!a) return;
    toggle.setAttribute("aria-expanded", "false");
    links.classList.remove("is-open");

    // A section link must clear any active filter, or its target may be hidden.
    var href = a.getAttribute("href") || "";
    if (href.charAt(0) !== "#") return;
    var id = href.slice(1);
    if (SECTIONS.indexOf(id) !== -1) {
      var chip = document.querySelector('.chip[data-filter="' + id + '"]')
              || document.querySelector('.chip[data-filter="all"]');
      if (chip && !chip.classList.contains("is-active")) chip.click();
    }
  });

  /* ---------------- Print support ----------------
     The Download button serves a pre-built PDF (tools/build_pdf.py), so no
     JS is needed for it. This block only keeps Ctrl+P honest: album slides
     live outside the DOM until asked for, and scroll-reveal would otherwise
     print untouched sections as blank pages.                                */

  function addAlbumSlidesForPrint() {
    Object.keys(ALBUMS).forEach(function (id) {
      var grid = document.querySelector('[data-albums="' + ALBUMS[id].section + '"]');
      if (!grid || grid.querySelector('[data-print-album="' + id + '"]')) return;

      (albumSlides[id] || []).forEach(function (s) {
        var fig = document.createElement("figure");
        fig.className = "tile print-slide";
        fig.setAttribute("data-print-album", id);
        fig.innerHTML =
          '<div class="tile__media">' +
            '<img src="' + s.thumb + '" alt="' + esc(s.title) + '" decoding="async">' +
          "</div>" +
          '<div class="tile__body">' +
            '<h5 class="tile__title">' + esc(ALBUMS[id].title.split(" - ")[0]) +
              " — " + esc(s.title) + "</h5>" +
          "</div>";
        grid.appendChild(fig);
      });
    });
  }

  // The album slides must exist in the DOM for any print route, including a
  // plain Ctrl+P. Built once the page has settled so the extra thumbnails
  // never compete with first render.
  function whenIdle(fn) {
    if ("requestIdleCallback" in window) requestIdleCallback(fn, { timeout: 3000 });
    else setTimeout(fn, 1200);
  }
  if (document.readyState === "complete") whenIdle(addAlbumSlidesForPrint);
  else window.addEventListener("load", function () { whenIdle(addAlbumSlidesForPrint); });

  // Ctrl+P / File > Print still produces the same document as the PDF.
  window.addEventListener("beforeprint", function () {
    addAlbumSlidesForPrint();
    document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("is-in"); });
    Array.prototype.forEach.call(document.images, function (im) { im.loading = "eager"; });
  });

  /* ---------------- misc ---------------- */

  document.getElementById("year").textContent = new Date().getFullYear();
})();
