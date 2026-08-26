/* Pixelrock — améliorations progressives.
   Sans JavaScript, tout continue de fonctionner : le <select> natif reste
   dans le formulaire et c'est lui qui porte la valeur envoyée. */

(function () {
  "use strict";

  /* ---------------------------------------------------------------
     Listes déroulantes aux couleurs du site.
     Un <select> natif ne peut pas être stylé au-delà de son bouton :
     la liste elle-même est dessinée par le système. On la remplace donc
     par une liste ARIA, en gardant le <select> comme source de vérité.
     --------------------------------------------------------------- */

  function enhanceSelect(select) {
    if (select.multiple || select.dataset.enhanced) return;
    select.dataset.enhanced = "true";

    var options = Array.prototype.slice.call(select.options);
    var label = select.labels && select.labels[0];
    var id = select.id || "sel-" + Math.floor(performance.now() * 1000);
    var listId = id + "-list";
    var btnId = id + "-button";
    if (label && !label.id) label.id = id + "-label";

    var wrap = document.createElement("div");
    wrap.className = "cselect";

    var btn = document.createElement("button");
    btn.type = "button";
    btn.id = btnId;
    btn.className = "cselect__btn";
    btn.setAttribute("aria-haspopup", "listbox");
    btn.setAttribute("aria-expanded", "false");
    btn.setAttribute("aria-controls", listId);
    if (label) btn.setAttribute("aria-labelledby", label.id + " " + btnId);

    var text = document.createElement("span");
    text.className = "cselect__value";
    btn.appendChild(text);

    var list = document.createElement("ul");
    list.id = listId;
    list.className = "cselect__list";
    list.setAttribute("role", "listbox");
    list.hidden = true;
    if (label) list.setAttribute("aria-labelledby", label.id);

    options.forEach(function (opt, i) {
      var li = document.createElement("li");
      li.className = "cselect__option";
      li.setAttribute("role", "option");
      li.id = id + "-opt-" + i;
      li.dataset.index = String(i);
      li.textContent = opt.textContent;
      li.setAttribute("aria-selected", opt.selected ? "true" : "false");
      list.appendChild(li);
    });

    wrap.appendChild(btn);
    wrap.appendChild(list);
    select.parentNode.insertBefore(wrap, select.nextSibling);

    select.classList.add("cselect__native");
    select.setAttribute("tabindex", "-1");
    select.setAttribute("aria-hidden", "true");

    var items = Array.prototype.slice.call(list.children);
    var active = select.selectedIndex < 0 ? 0 : select.selectedIndex;
    var typed = "";
    var typedAt = 0;

    function paint() {
      text.textContent = options[select.selectedIndex] ? options[select.selectedIndex].textContent : "";
      items.forEach(function (li, i) {
        li.setAttribute("aria-selected", i === select.selectedIndex ? "true" : "false");
        li.classList.toggle("is-active", i === active);
      });
      if (!list.hidden && items[active]) {
        list.setAttribute("aria-activedescendant", items[active].id);
        var li = items[active];
        var top = li.offsetTop;
        var bottom = top + li.offsetHeight;
        if (top < list.scrollTop) list.scrollTop = top;
        else if (bottom > list.scrollTop + list.clientHeight) list.scrollTop = bottom - list.clientHeight;
      }
    }

    function open() {
      if (!list.hidden) return;
      list.hidden = false;
      btn.setAttribute("aria-expanded", "true");
      active = select.selectedIndex < 0 ? 0 : select.selectedIndex;
      paint();
      document.addEventListener("pointerdown", onOutside, true);
    }

    function close(focusButton) {
      if (list.hidden) return;
      list.hidden = true;
      btn.setAttribute("aria-expanded", "false");
      list.removeAttribute("aria-activedescendant");
      document.removeEventListener("pointerdown", onOutside, true);
      if (focusButton) btn.focus();
    }

    function choose(i) {
      if (i < 0 || i >= options.length) return;
      select.selectedIndex = i;
      active = i;
      select.dispatchEvent(new Event("change", { bubbles: true }));
      paint();
    }

    function onOutside(e) {
      if (!wrap.contains(e.target)) close(false);
    }

    function move(delta) {
      var next = active + delta;
      if (next < 0) next = 0;
      if (next > options.length - 1) next = options.length - 1;
      active = next;
      paint();
    }

    function search(ch) {
      var now = Date.now();
      typed = now - typedAt > 800 ? ch : typed + ch;
      typedAt = now;
      for (var i = 0; i < options.length; i++) {
        var j = (active + (typed.length > 1 ? 0 : 1) + i) % options.length;
        if (options[j].textContent.trim().toLowerCase().indexOf(typed) === 0) {
          active = j;
          paint();
          return;
        }
      }
    }

    btn.addEventListener("click", function () {
      list.hidden ? open() : close(true);
    });

    // tout le clavier est géré sur le bouton : la liste n'est jamais focalisée
    btn.addEventListener("keydown", function (e) {
      var isOpen = !list.hidden;

      if (e.key === "Escape") {
        if (isOpen) { e.preventDefault(); close(true); }
        return;
      }
      if (e.key === "Tab") {
        if (isOpen) close(false);
        return;
      }
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        if (isOpen) { choose(active); close(true); } else { open(); }
        return;
      }
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault();
        if (!isOpen) { open(); return; }
        move(e.key === "ArrowDown" ? 1 : -1);
        return;
      }
      if (e.key === "Home" || e.key === "End") {
        e.preventDefault();
        if (!isOpen) open();
        active = e.key === "Home" ? 0 : options.length - 1;
        paint();
        return;
      }
      if (e.key.length === 1 && !e.metaKey && !e.ctrlKey && !e.altKey) {
        if (!isOpen) open();
        search(e.key.toLowerCase());
      }
    });

    items.forEach(function (li) {
      li.addEventListener("click", function () {
        choose(parseInt(li.dataset.index, 10));
        close(true);
      });
      li.addEventListener("pointermove", function () {
        active = parseInt(li.dataset.index, 10);
        paint();
      });
    });

    if (label) {
      label.addEventListener("click", function (e) {
        e.preventDefault();
        btn.focus();
      });
    }

    select.addEventListener("change", paint);
    paint();
  }

  function init() {
    document.querySelectorAll("select").forEach(enhanceSelect);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
