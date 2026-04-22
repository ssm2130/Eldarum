(function () {
  var body = document.body;
  var root = body.getAttribute("data-root") || "";

  /**
   * Must stay in sync with data/navigation.json → topBarNav.
   * Used when navigation.json cannot be loaded (opening pages via file://, blocked fetch, or bad server path).
   */
  var FALLBACK_TOP_BAR = [
    { label: "Home", href: "index.html" },
    {
      label: "Site index",
      href: "pages/meta/sitemap.html",
      match: "meta/sitemap",
    },
    {
      label: "Lore sources",
      href: "pages/meta/lore-sources.html",
      match: "meta/lore-sources",
    },
    {
      label: "Atlas",
      href: "pages/atlas/index.html",
      match: "pages/atlas/index",
    },
    {
      label: "Asceveron",
      href: "pages/atlas/asceveron.html",
      match: "atlas/asceveron.html",
    },
    {
      label: "Planes",
      href: "pages/cosmology/planes-of-existence.html",
      match: "planes-of-existence",
    },
    {
      label: "Gods",
      href: "pages/faith/gods-of-eldarum.html",
      match: "gods-of-eldarum",
    },
    {
      label: "Pantheon",
      href: "pages/faith/pantheon.html",
      match: "faith/pantheon.html",
    },
    {
      label: "Titan Wars",
      href: "pages/faith/titan-wars.html",
      match: "titan-wars.html",
    },
    {
      label: "Timeline",
      href: "pages/history/master-timeline.html",
      match: "master-timeline",
    },
    {
      label: "Grand chronicle",
      href: "pages/history/asceveron-grand-chronicle.html",
      match: "asceveron-grand-chronicle",
    },
    {
      label: "Campaign journal",
      href: "pages/campaign/journal.html",
      match: "campaign/journal",
    },
    {
      label: "Northwake",
      href: "pages/gazetteer/northwake-hub.html",
      match: "gazetteer/",
    },
    {
      label: "Frontier",
      href: "pages/asceveron.html",
      match: "pages/asceveron.html",
    },
    { label: "People", href: "pages/npcs-notable.html", match: "npcs-notable" },
  ];

  var bcLabels = (body.getAttribute("data-bc-labels") || "")
    .split("|")
    .map(function (s) {
      return s.trim();
    })
    .filter(Boolean);
  var bcHrefs = (body.getAttribute("data-bc-hrefs") || "")
    .split("|")
    .map(function (s) {
      return s.trim();
    });

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }

  function syncHeaderStickyHeight() {
    var header = document.querySelector(".site-header");
    if (!header) return;
    document.documentElement.style.setProperty(
      "--header-stack-h",
      header.offsetHeight + "px"
    );
  }

  function fillNavUl(ul, items, curPath) {
    ul.innerHTML = "";
    items.forEach(function (item) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = root + item.href;
      a.textContent = item.label;
      if (navLinkActive(item, curPath)) {
        a.setAttribute("aria-current", "page");
      }
      li.appendChild(a);
      ul.appendChild(li);
    });
  }

  /**
   * Header: brand + search + menu toggle, then curated top link bar (joosten.us-style).
   * Destinations come from navigation.json topBarNav; sidebar lists the full shelf.
   */
  function upgradeHeaderToJoostenShell() {
    var h = document.querySelector("header.app-header");
    if (!h || h.getAttribute("data-eladarum-shell") === "joosten") return;
    h.setAttribute("data-eladarum-shell", "joosten");

    var toggle = h.querySelector("button.menu-toggle");
    var brand = h.querySelector(".app-header__brand");
    var search = h.querySelector(".header-search");

    h.classList.remove("app-header");
    h.classList.add("site-header");

    var inner = document.createElement("div");
    inner.className = "site-header__inner";

    var nav = document.createElement("nav");
    nav.id = "site-nav";
    nav.className = "site-nav";
    nav.setAttribute("aria-label", "Primary");

    var ulPrimary = document.createElement("ul");
    ulPrimary.id = "site-nav-primary";
    nav.appendChild(ulPrimary);

    if (brand) {
      brand.classList.remove("app-header__brand");
      brand.classList.add("brand");
      inner.appendChild(brand);
    }

    if (search) inner.appendChild(search);

    if (toggle) {
      toggle.classList.add("nav-toggle");
      toggle.setAttribute("aria-controls", "site-nav");
      toggle.removeAttribute("data-sidebar-toggle");
      toggle.setAttribute("aria-expanded", "false");
      inner.appendChild(toggle);
    }

    inner.appendChild(nav);

    h.innerHTML = "";
    h.appendChild(inner);

    syncHeaderStickyHeight();
    if (window.ResizeObserver && h) {
      try {
        var ro = new ResizeObserver(function () {
          syncHeaderStickyHeight();
        });
        ro.observe(h);
      } catch (e0) {}
    }
    window.addEventListener("resize", syncHeaderStickyHeight);
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(syncHeaderStickyHeight);
    }
  }

  function navLinkActive(item, curPath) {
    var lower = curPath.toLowerCase().replace(/\\/g, "/");
    if (item.match) {
      return lower.indexOf(item.match.replace(/^\//, "").toLowerCase()) !== -1;
    }
    var href = (item.href || "").replace(/\\/g, "/").toLowerCase();
    if (href === "index.html") {
      return (
        (lower.endsWith("/index.html") && lower.indexOf("/pages/") === -1) ||
        lower.endsWith("/webpage") ||
        lower.endsWith("/webpage/")
      );
    }
    return lower.endsWith(href) || lower.endsWith("/" + href);
  }

  function renderPrimaryNav(nav) {
    var ulPrimary = document.querySelector("#site-nav-primary");
    if (!ulPrimary) return;
    var items =
      nav.topBarNav && nav.topBarNav.length
        ? nav.topBarNav
        : nav.primaryNav;
    if (!items || !items.length) return;
    var curPath = window.location.pathname.replace(/\\/g, "/");
    fillNavUl(ulPrimary, items, curPath);
    syncHeaderStickyHeight();
  }

  function sidebarLinkActive(link, curPath) {
    return navLinkActive(link, curPath);
  }

  /** Section navigation — same destinations as navigation.json.sidebar; not article body text. */
  function renderSidebar(navData) {
    if (document.body.getAttribute("data-section") === "home") return;
    var aside = document.getElementById("sidebar-target");
    if (!aside || !navData.sidebar || !navData.sidebar.length) return;
    aside.innerHTML = "";
    var curPath = window.location.pathname.replace(/\\/g, "/");
    navData.sidebar.forEach(function (section) {
      var sec = document.createElement("section");
      sec.className = "sidebar-section";
      var h = document.createElement("h3");
      h.className = "sidebar__title";
      h.textContent = section.heading;
      sec.appendChild(h);
      var ul = document.createElement("ul");
      section.links.forEach(function (link) {
        var li = document.createElement("li");
        var a = document.createElement("a");
        a.href = root + link.href;
        a.textContent = link.label;
        if (sidebarLinkActive(link, curPath)) {
          a.classList.add("is-active");
          a.setAttribute("aria-current", "page");
        }
        li.appendChild(a);
        ul.appendChild(li);
      });
      sec.appendChild(ul);
      aside.appendChild(sec);
    });
  }

  /** Breadcrumb only (joosten.us omits mega topic dock / recent trail). */
  function ensureWayfindingShell() {
    var strip = document.querySelector(".breadcrumb-strip");
    if (!strip || strip.closest(".wayfinding-shell")) return;
    var shell = document.createElement("div");
    shell.className = "wayfinding-shell";
    strip.parentNode.insertBefore(shell, strip);
    shell.appendChild(strip);
  }

  function renderBreadcrumb() {
    var target = document.getElementById("breadcrumb-target");
    if (!target || !bcLabels.length) return;
    target.innerHTML = "";
    bcLabels.forEach(function (label, i) {
      if (i > 0) target.appendChild(el("span", "sep", "›"));
      var last = i === bcLabels.length - 1;
      if (last) {
        target.appendChild(el("span", "here", label));
        return;
      }
      var href = bcHrefs[i];
      var a = el("a", "", label);
      a.href = root + (href || "index.html");
      target.appendChild(a);
    });
  }

  /** Narrow viewports: Menu toggles #site-nav.is-open (full link list). */
  function wirePrimaryNavToggle() {
    var toggle =
      document.querySelector("button.nav-toggle") ||
      document.querySelector("button.menu-toggle");
    var nav = document.getElementById("site-nav");
    if (!toggle || !nav) return;
    toggle.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });

    document.addEventListener("click", function (e) {
      if (
        nav.classList.contains("is-open") &&
        !nav.contains(e.target) &&
        !toggle.contains(e.target)
      ) {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });

    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape") return;
      nav.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    });
  }

  function canonicalPagePath() {
    try {
      var p = decodeURIComponent(window.location.pathname).replace(/\\/g, "/");
      var idx = p.toLowerCase().lastIndexOf("webpage/");
      if (idx !== -1)
        return p.slice(idx + "webpage/".length).replace(/^\/+/, "");
      var m = p.match(/([^/]+\.html?)$/i);
      return m ? m[1] : "index.html";
    } catch (e1) {
      return "index.html";
    }
  }

  function initSearch() {
    var input = document.getElementById("site-search");
    var box = document.getElementById("search-results");
    if (!input || !box) return;
    var idx = [];
    fetch(root + "data/search-index.json")
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        idx = data.pages || [];
      })
      .catch(function () {
        idx = [];
      });

    function norm(s) {
      return (s || "").toLowerCase();
    }
    function score(q, item) {
      if (!q) return 0;
      var t = norm(item.title);
      var k = norm(item.keywords || "");
      if (t.indexOf(q) !== -1) return 100;
      if (k.indexOf(q) !== -1) return 60;
      var parts = q.split(/\s+/).filter(Boolean);
      var s = 0;
      parts.forEach(function (p) {
        if (t.indexOf(p) !== -1) s += 22;
        else if (k.indexOf(p) !== -1) s += 12;
      });
      return s;
    }

    function render(items) {
      box.innerHTML = "";
      items.slice(0, 30).forEach(function (item) {
        var a = document.createElement("a");
        a.href = root + item.href;
        a.textContent = item.title;
        box.appendChild(a);
      });
      box.classList.toggle("open", items.length > 0);
    }

    input.addEventListener("input", function () {
      var q = norm(input.value.trim());
      if (!q || !idx.length) {
        box.classList.remove("open");
        return;
      }
      var ranked = idx
        .map(function (item) {
          return { item: item, s: score(q, item) };
        })
        .filter(function (x) {
          return x.s > 0;
        })
        .sort(function (a, b) {
          return b.s - a.s;
        })
        .map(function (x) {
          return x.item;
        });
      render(ranked);
    });

    document.addEventListener("click", function (e) {
      if (!box.contains(e.target) && e.target !== input)
        box.classList.remove("open");
    });
  }

  /* Skip link + main id */
  var skip = document.createElement("a");
  skip.className = "skip-link";
  skip.href = "#main";
  skip.textContent = "Skip to content";
  body.insertBefore(skip, body.firstChild);
  var mainEl = document.querySelector("main.main");
  if (mainEl && !mainEl.id) mainEl.id = "main";

  upgradeHeaderToJoostenShell();
  ensureWayfindingShell();

  fetch(root + "data/navigation.json")
    .then(function (r) {
      if (!r.ok) throw new Error("navigation.json HTTP " + r.status);
      return r.json();
    })
    .then(function (nav) {
      renderPrimaryNav(nav);
      renderSidebar(nav);
      renderBreadcrumb();
      wirePrimaryNavToggle();
      initSearch();
      syncHeaderStickyHeight();
    })
    .catch(function () {
      renderPrimaryNav({ topBarNav: FALLBACK_TOP_BAR });
      renderBreadcrumb();
      wirePrimaryNavToggle();
      initSearch();
      syncHeaderStickyHeight();
    });
})();
