/*
 * BARMM Labour Market Readiness — Cookie Consent & Settings
 *
 * - Shows a consent pop-up after the visitor has spent 2 minutes of visible,
 *   active time on the platform (time is accumulated across pages in the same
 *   browser session, and pauses while the tab is hidden).
 * - Categories: necessary (always on), preferences, analytics.
 * - Google Analytics is loaded ONLY after analytics consent is granted.
 * - Any element with [data-cookie-settings] opens the settings view on demand.
 * - Public API: window.BarmmConsent.{get, allowed, open, save}
 */
(function () {
  "use strict";

  var STORAGE_KEY = "barmmCookieConsent";
  var VISIT_KEY = "barmmVisitMs";
  var VERSION = 1;
  var DELAY_MS = 2 * 60 * 1000; // 2 minutes
  var MAX_AGE_MS = 365 * 24 * 60 * 60 * 1000; // re-ask after 12 months
  var GA_ID = "G-2CNG7D15Q7";
  var POLICY_URL = "/public/cookie-policy.html";
  var PRIVACY_URL = "/public/privacy-policy.html";

  function read() {
    try {
      var c = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null");
      if (!c || c.v !== VERSION) return null;
      if (Date.now() - (c.ts || 0) > MAX_AGE_MS) return null;
      return c;
    } catch (e) {
      return null;
    }
  }

  function write(choice) {
    var c = {
      v: VERSION,
      ts: Date.now(),
      necessary: true,
      preferences: !!choice.preferences,
      analytics: !!choice.analytics
    };
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(c)); } catch (e) { /* storage blocked */ }
    current = c;
    apply(c);
    try { document.dispatchEvent(new CustomEvent("barmm:consent", { detail: c })); } catch (e) { /* old browser */ }
    return c;
  }

  var current = read();

  /* ---------- Analytics (opt-in only) ---------- */
  var gaLoaded = false;
  function loadAnalytics() {
    window["ga-disable-" + GA_ID] = false;
    if (gaLoaded) return;
    gaLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", GA_ID, { anonymize_ip: true });
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
    document.head.appendChild(s);
  }
  function removeAnalytics() {
    window["ga-disable-" + GA_ID] = true;
    var host = location.hostname.split(".");
    var domains = ["", location.hostname];
    if (host.length > 1) domains.push("." + host.slice(-2).join("."), "." + host.slice(-3).join("."));
    document.cookie.split(";").forEach(function (part) {
      var name = part.split("=")[0].trim();
      if (/^_ga/.test(name) || name === "_gid" || name === "_gat") {
        domains.forEach(function (d) {
          document.cookie = name + "=; Max-Age=0; path=/" + (d ? "; domain=" + d : "");
        });
      }
    });
  }
  function removePreferences() {
    try { localStorage.removeItem("barmmLastPage"); } catch (e) { /* ignore */ }
  }
  function apply(c) {
    if (c && c.analytics) loadAnalytics(); else removeAnalytics();
    if (!c || !c.preferences) removePreferences();
  }
  if (current) apply(current);

  /* ---------- UI ---------- */
  var CSS =
    ".cc-back{position:fixed;inset:0;background:#061c14a6;display:flex;align-items:center;justify-content:center;padding:18px;z-index:1000;opacity:0;transition:opacity .25s}" +
    ".cc-back.cc-show{opacity:1}.cc-back[hidden]{display:none}" +
    ".cc-modal{background:#fff;color:#1d2b25;border-radius:14px;max-width:560px;width:100%;max-height:90vh;overflow:auto;box-shadow:0 24px 60px rgba(6,28,20,.35);font-family:'Roboto Condensed',Arial,sans-serif;border-top:4px solid #c6a15b}" +
    ".cc-head{display:flex;gap:14px;align-items:flex-start;padding:22px 22px 0}" +
    ".cc-icon{flex:0 0 44px;height:44px;border-radius:50%;background:#e8f2ed;display:grid;place-items:center;font-size:22px}" +
    ".cc-eyebrow{font:600 10px Poppins,sans-serif;color:#237758;text-transform:uppercase;letter-spacing:1.2px}" +
    ".cc-title{font:700 18px Montserrat,sans-serif;color:#0b3d2e;margin:4px 0 0}" +
    ".cc-close{margin-left:auto;border:1px solid #e0e8e3;background:#fff;color:#0b3d2e;border-radius:8px;padding:6px 10px;cursor:pointer;font-size:14px}" +
    ".cc-body{padding:12px 22px 4px;font-size:15px;line-height:1.55;color:#3b4a42}" +
    ".cc-body p{margin:8px 0}.cc-body a{color:#155b45;font-weight:600}" +
    ".cc-cats{display:grid;gap:10px;margin:14px 0 6px}" +
    ".cc-cat{border:1px solid #e0e8e3;border-radius:10px;padding:12px 14px;background:#fafcfb}" +
    ".cc-cat-row{display:flex;align-items:center;justify-content:space-between;gap:12px}" +
    ".cc-cat h3{font:700 13px Poppins,sans-serif;color:#0b3d2e;margin:0}" +
    ".cc-cat p{font-size:13px;color:#69776f;margin:6px 0 0;line-height:1.45}" +
    ".cc-tag{font:600 10px Poppins,sans-serif;background:#e8f2ed;color:#155b45;padding:3px 8px;border-radius:20px;white-space:nowrap}" +
    ".cc-switch{position:relative;width:44px;height:24px;flex:0 0 44px}" +
    ".cc-switch input{opacity:0;width:100%;height:100%;margin:0;position:absolute;inset:0;cursor:pointer;z-index:1}" +
    ".cc-switch span{position:absolute;inset:0;background:#cdd9d2;border-radius:24px;transition:background .2s}" +
    ".cc-switch span:before{content:'';position:absolute;width:18px;height:18px;left:3px;top:3px;background:#fff;border-radius:50%;transition:transform .2s;box-shadow:0 1px 3px #0003}" +
    ".cc-switch input:checked+span{background:#155b45}.cc-switch input:checked+span:before{transform:translateX(20px)}" +
    ".cc-switch input:focus-visible+span{outline:2px solid #c6a15b;outline-offset:2px}" +
    ".cc-actions{display:flex;flex-wrap:wrap;gap:8px;justify-content:flex-end;padding:14px 22px 22px}" +
    ".cc-btn{border:1px solid #e0e8e3;background:#fff;color:#0b3d2e;border-radius:8px;padding:10px 14px;font:600 13px Poppins,sans-serif;cursor:pointer}" +
    ".cc-btn:hover{filter:brightness(.97)}.cc-btn:focus-visible,.cc-close:focus-visible{outline:2px solid #c6a15b;outline-offset:2px}" +
    ".cc-btn.cc-primary{background:#155b45;border-color:#155b45;color:#fff}" +
    ".cc-hidden{display:none!important}" +
    "@media(max-width:560px){.cc-back{align-items:flex-end;padding:0}.cc-modal{border-radius:14px 14px 0 0;max-height:92vh}.cc-actions .cc-btn{flex:1 1 100%}}" +
    "@media(prefers-reduced-motion:reduce){.cc-back,.cc-switch span,.cc-switch span:before{transition:none}}" +
    "@media print{.cc-back{display:none!important}}";

  var root = null, lastFocus = null;

  function el(html) {
    var d = document.createElement("div");
    d.innerHTML = html.trim();
    return d.firstChild;
  }

  function build() {
    if (root) return root;
    var style = document.createElement("style");
    style.textContent = CSS;
    document.head.appendChild(style);
    root = el(
      '<div class="cc-back" role="dialog" aria-modal="true" aria-labelledby="ccTitle" aria-describedby="ccDesc" hidden>' +
      '<div class="cc-modal">' +
      '<div class="cc-head"><div class="cc-icon" aria-hidden="true">🍪</div><div>' +
      '<div class="cc-eyebrow">Your privacy choices</div><h2 class="cc-title" id="ccTitle">Cookie Consent &amp; Settings</h2></div>' +
      '<button type="button" class="cc-close" data-cc="close" aria-label="Close cookie settings">✕</button></div>' +
      '<div class="cc-body"><div id="ccDesc">' +
      '<p>The BARMM Labour Market Readiness platform uses a small amount of browser storage so the dashboard works properly. With your permission, we would also like to remember your preferences and measure aggregate, anonymised usage to improve the platform for MTIT and its partners.</p>' +
      '<p>Non-essential storage stays off unless you switch it on. You can change your choice at any time from <b>Cookie settings</b> in the side panel. Read the <a href="' + POLICY_URL + '">Cookie Policy</a> and <a href="' + PRIVACY_URL + '">Privacy Policy</a>.</p></div>' +
      '<div class="cc-cats cc-hidden" data-cc="details">' +
      '<div class="cc-cat"><div class="cc-cat-row"><h3>Strictly necessary</h3><span class="cc-tag">Always on</span></div>' +
      '<p>Stores your consent choice, the offline app cache (service worker) and Project Register records you create on this device. These never leave your browser.</p></div>' +
      '<div class="cc-cat"><div class="cc-cat-row"><h3 id="ccPrefLbl">Preferences</h3><label class="cc-switch"><input type="checkbox" data-cc="preferences" aria-labelledby="ccPrefLbl"><span></span></label></div>' +
      '<p>Remembers the dashboard section you last viewed so you can continue where you left off.</p></div>' +
      '<div class="cc-cat"><div class="cc-cat-row"><h3 id="ccAnaLbl">Analytics</h3><label class="cc-switch"><input type="checkbox" data-cc="analytics" aria-labelledby="ccAnaLbl"><span></span></label></div>' +
      '<p>Google Analytics cookies (_ga, _ga_*) with IP anonymisation, used only to count visits and popular sections in aggregate. No advertising or cross-site profiling.</p></div>' +
      '</div></div>' +
      '<div class="cc-actions">' +
      '<button type="button" class="cc-btn" data-cc="reject">Reject non-essential</button>' +
      '<button type="button" class="cc-btn" data-cc="customise">Customise settings</button>' +
      '<button type="button" class="cc-btn cc-hidden" data-cc="save">Save my choices</button>' +
      '<button type="button" class="cc-btn cc-primary" data-cc="accept">Accept all</button>' +
      '</div></div></div>'
    );
    document.body.appendChild(root);

    root.addEventListener("click", function (e) {
      if (e.target === root) { close(); return; }
      var btn = e.target.closest("[data-cc]");
      if (!btn) return;
      var act = btn.getAttribute("data-cc");
      if (act === "close") close();
      else if (act === "accept") { write({ preferences: true, analytics: true }); close(); }
      else if (act === "reject") { write({ preferences: false, analytics: false }); close(); }
      else if (act === "customise") showDetails(true);
      else if (act === "save") {
        write({
          preferences: q('[data-cc="preferences"]').checked,
          analytics: q('[data-cc="analytics"]').checked
        });
        close();
      }
    });
    root.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { close(); return; }
      if (e.key !== "Tab") return;
      var f = [].slice.call(root.querySelectorAll("button,a[href],input")).filter(function (n) { return n.offsetParent !== null; });
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
    return root;
  }

  function q(sel) { return root.querySelector(sel); }

  function showDetails(on) {
    q('[data-cc="details"]').classList.toggle("cc-hidden", !on);
    q('[data-cc="save"]').classList.toggle("cc-hidden", !on);
    q('[data-cc="customise"]').classList.toggle("cc-hidden", on);
  }

  function open(withDetails) {
    build();
    var c = current || { preferences: false, analytics: false };
    q('[data-cc="preferences"]').checked = !!c.preferences;
    q('[data-cc="analytics"]').checked = !!c.analytics;
    showDetails(!!withDetails);
    lastFocus = document.activeElement;
    root.hidden = false;
    requestAnimationFrame(function () { root.classList.add("cc-show"); });
    var focusTarget = q(withDetails ? '[data-cc="preferences"]' : '[data-cc="accept"]');
    setTimeout(function () { focusTarget && focusTarget.focus(); }, 30);
  }

  function close() {
    if (!root || root.hidden) return;
    root.classList.remove("cc-show");
    root.hidden = true;
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  /* ---------- 2-minute timer (visible time, accumulated per session) ---------- */
  var timer = null;
  function elapsed() {
    try { return parseInt(sessionStorage.getItem(VISIT_KEY) || "0", 10) || 0; } catch (e) { return 0; }
  }
  function setElapsed(ms) {
    try { sessionStorage.setItem(VISIT_KEY, String(ms)); } catch (e) { /* ignore */ }
  }
  function startTimer() {
    if (current || timer) return;
    var acc = elapsed();
    if (acc >= DELAY_MS) { open(false); return; }
    var last = Date.now();
    timer = setInterval(function () {
      var now = Date.now();
      if (document.visibilityState === "visible") acc += Math.min(now - last, 5000);
      last = now;
      setElapsed(acc);
      if (current) { clearInterval(timer); timer = null; return; }
      if (acc >= DELAY_MS) {
        clearInterval(timer); timer = null;
        open(false);
      }
    }, 1000);
  }

  function boot() {
    document.addEventListener("click", function (e) {
      var t = e.target.closest && e.target.closest("[data-cookie-settings]");
      if (t) { e.preventDefault(); open(true); }
    });
    startTimer();
  }

  window.BarmmConsent = {
    get: function () { return current; },
    allowed: function (cat) { return cat === "necessary" || !!(current && current[cat]); },
    open: open,
    save: write
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
