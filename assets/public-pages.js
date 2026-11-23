/* Shared behaviour for BARMM Labour Market Readiness public pages. */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };

  // Mobile side panel
  var sidebar = $("#sidebar"), menuBtn = $("#menuBtn");
  if (sidebar && menuBtn) {
    menuBtn.addEventListener("click", function () {
      var open = sidebar.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", String(open));
    });
  }

  // Policies dropdown
  $$(".nav-dropdown").forEach(function (dd) {
    var btn = $(".nav-trigger", dd);
    if (!btn) return;
    btn.addEventListener("click", function () {
      var open = dd.classList.toggle("open");
      btn.setAttribute("aria-expanded", String(open));
    });
  });

  // Table of contents: highlight the section in view
  var tocLinks = $$(".toc a[href^='#']");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && map[en.target.id]) {
          tocLinks.forEach(function (a) { a.classList.remove("active"); });
          map[en.target.id].classList.add("active");
        }
      });
    }, { rootMargin: "-90px 0px -65% 0px" });
    Object.keys(map).forEach(function (id) { var s = document.getElementById(id); if (s) io.observe(s); });
  }

  // Cookie policy page: live summary of the saved choice
  var status = $("#consentStatus");
  function renderStatus() {
    if (!status || !window.BarmmConsent) return;
    var c = window.BarmmConsent.get();
    status.textContent = c
      ? "Current choice — Preferences: " + (c.preferences ? "on" : "off") + " · Analytics: " + (c.analytics ? "on" : "off") +
        " · saved " + new Date(c.ts).toLocaleDateString("en-PH", { year: "numeric", month: "long", day: "numeric" })
      : "No choice saved yet — only strictly necessary storage is active.";
  }
  renderStatus();
  document.addEventListener("barmm:consent", renderStatus);

  // Contact form (Netlify Forms, AJAX submission)
  var form = $("#contactForm");
  if (form) {
    var msg = $("#message", form), counter = $("#msgCount"), statusEl = $("#formStatus"), submit = $("#submitBtn");
    if (msg && counter) msg.addEventListener("input", function () { counter.textContent = msg.value.length; });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      statusEl.textContent = ""; statusEl.classList.remove("err");
      if (!form.checkValidity()) {
        form.reportValidity();
        statusEl.textContent = "Please complete the required fields.";
        statusEl.classList.add("err");
        return;
      }
      submit.disabled = true;
      submit.textContent = "Sending…";
      fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams(new FormData(form)).toString()
      }).then(function (res) {
        if (!res.ok) throw new Error("HTTP " + res.status);
        form.classList.add("hidden");
        $("#formSuccess").classList.remove("hidden");
        $("#formSuccess").focus();
      }).catch(function () {
        statusEl.textContent = "Your message could not be sent. Please try again or email us directly.";
        statusEl.classList.add("err");
      }).finally(function () {
        submit.disabled = false;
        submit.textContent = "Send message";
      });
    });
  }
})();
