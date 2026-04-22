(function () {
  var input = document.getElementById("wiki-search");
  var box = document.getElementById("search-results");
  if (!input || !box) return;

  var idx = [];
  fetch((document.body.dataset.root || "") + "data/search-index.json")
    .then(function (r) { return r.json(); })
    .then(function (data) { idx = data.pages || []; })
    .catch(function () { idx = []; });

  function norm(s) {
    return (s || "").toLowerCase();
  }

  function score(q, item) {
    if (!q) return 0;
    var t = norm(item.title);
    var k = norm(item.keywords || "");
    if (t.indexOf(q) !== -1) return 100;
    if (k.indexOf(q) !== -1) return 50;
    var parts = q.split(/\s+/).filter(Boolean);
    var s = 0;
    parts.forEach(function (p) {
      if (t.indexOf(p) !== -1) s += 20;
      else if (k.indexOf(p) !== -1) s += 10;
    });
    return s;
  }

  function render(items) {
    box.innerHTML = "";
    items.slice(0, 24).forEach(function (item) {
      var a = document.createElement("a");
      a.href = (document.body.dataset.root || "") + item.href;
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
      .filter(function (x) { return x.s > 0; })
      .sort(function (a, b) { return b.s - a.s; })
      .map(function (x) { return x.item; });
    render(ranked);
  });

  document.addEventListener("click", function (e) {
    if (!box.contains(e.target) && e.target !== input) {
      box.classList.remove("open");
    }
  });
})();
