/* ============================================================================
   PMFtracker — lead capture
   Two flows, one modal:
     • "request"  — industry + email ("tell us your industry, we'll build it")
     • "magnet"   — email only, value-exchange ("email me the kit/template")

   ▶ CONFIGURE ME ◀
   Set LEAD_ENDPOINT to the URL that should receive submissions. Works with:
     - Google Apps Script web app  (doPost reads e.parameter.*)
     - Formspree / Basin form endpoint
     - Any ESP form action that accepts x-www-form-urlencoded fields
   Fields sent: email, industry, asset, source, ts
   Leave it "" to run in DEMO mode (no network call; saved to localStorage only).
   ========================================================================== */
(function () {
  "use strict";
  var LEAD_ENDPOINT = "https://hook.eu1.make.com/voppg3xcsvt7m5k9xj1hplogdbhnktlw"; // Make custom webhook

  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  // ---- modal markup (injected once) ----
  var MODAL = ''
    + '<div class="lead-modal" id="pmfLeadModal" aria-hidden="true">'
    +   '<div class="lead-modal-overlay" data-lead-close></div>'
    +   '<div class="lead-modal-card" role="dialog" aria-modal="true" aria-labelledby="pmfLeadTitle">'
    +     '<button class="lead-modal-x" type="button" data-lead-close aria-label="Close">&times;</button>'
    +     '<form class="lead-form" novalidate>'
    +       '<div class="lead-hp" aria-hidden="true"><label>Don\'t fill this in<input type="text" name="website" class="lead-hp-input" tabindex="-1" autocomplete="off"/></label></div>'
    +       '<h3 id="pmfLeadTitle" class="lead-title"></h3>'
    +       '<p class="lead-sub"></p>'
    +       '<input type="text" class="lead-industry" placeholder="Your industry (e.g. healthtech)" autocomplete="off"/>'
    +       '<input type="email" class="lead-email" placeholder="you@company.com" autocomplete="email" required/>'
    +       '<div class="lead-error" role="alert" hidden>Please enter a valid email address.</div>'
    +       '<button type="submit" class="lead-submit cta-btn"></button>'
    +       '<p class="lead-fine">No spam, ever. Unsubscribe anytime.</p>'
    +     '</form>'
    +     '<div class="lead-success" hidden>'
    +       '<div class="lead-check" aria-hidden="true">&#10003;</div>'
    +       '<h3 class="lead-success-title">You&#39;re on the list.</h3>'
    +       '<p class="lead-success-msg"></p>'
    +       '<button type="button" class="cta-btn lead-success-close" data-lead-close>Done</button>'
    +     '</div>'
    +   '</div>'
    + '</div>';

  var modal, form, title, sub, industryInput, emailInput, hpInput, errorBox, submitBtn, successBox, successMsg, lastFocus;

  function qs(sel) { return modal.querySelector(sel); }

  function openModal(mode, asset, trigger) {
    lastFocus = trigger || document.activeElement;
    modal.dataset.mode = mode;
    modal.dataset.asset = asset || "";
    // reset states
    form.hidden = false;
    successBox.hidden = true;
    errorBox.hidden = true;
    emailInput.value = "";
    industryInput.value = "";

    if (mode === "request") {
      title.textContent = "Tell us your industry";
      sub.textContent = "Leave your email and we'll send you the PMF benchmark for your industry the moment it's ready.";
      industryInput.style.display = "";
      submitBtn.textContent = "Send me the benchmark";
    } else {
      title.textContent = asset ? ("Get " + asset) : "Get the PMF Kit";
      sub.textContent = "Drop your email and we'll send it straight to your inbox.";
      industryInput.style.display = "none";
      submitBtn.textContent = "Email it to me";
    }

    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    document.documentElement.style.overflow = "hidden";
    setTimeout(function () { emailInput.focus(); }, 40);
  }

  function closeModal() {
    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    document.documentElement.style.overflow = "";
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  function submit(e) {
    e.preventDefault();
    // Honeypot: a hidden field bots auto-fill and humans never see. If it has a
    // value, silently drop the submission (fake success so bots get no signal) —
    // nothing is posted to the endpoint or saved.
    if (hpInput && hpInput.value) {
      console.info("[lead] honeypot tripped; dropping spam submission.");
      showSuccess({ industry: "", asset: modal.dataset.asset || "" });
      return;
    }
    var email = emailInput.value.trim();
    if (!EMAIL_RE.test(email)) {
      errorBox.hidden = false;
      emailInput.focus();
      return;
    }
    errorBox.hidden = true;
    submitBtn.disabled = true;
    submitBtn.textContent = "Sending…";

    var payload = {
      email: email,
      industry: industryInput.value.trim(),
      asset: modal.dataset.asset || "",
      source: location.pathname,
      mode: modal.dataset.mode || "",
      ts: new Date().toISOString()
    };

    // local backup so nothing is ever lost (also covers demo mode)
    try {
      var store = JSON.parse(localStorage.getItem("pmf_leads") || "[]");
      store.push(payload);
      localStorage.setItem("pmf_leads", JSON.stringify(store));
      localStorage.setItem("pmf_lead_email", email);
    } catch (err) {}

    function done() { showSuccess(payload); }

    if (LEAD_ENDPOINT) {
      var body = new URLSearchParams(payload).toString();
      fetch(LEAD_ENDPOINT, {
        method: "POST",
        mode: "no-cors",
        headers: { "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8" },
        body: body
      }).then(done).catch(function () {
        console.warn("[lead] endpoint POST failed; saved to localStorage backup.");
        done();
      });
    } else {
      console.info("[lead] DEMO mode (LEAD_ENDPOINT not set). Captured:", payload);
      done();
    }
  }

  function showSuccess(payload) {
    submitBtn.disabled = false;
    form.hidden = true;
    successBox.hidden = false;
    if (modal.dataset.mode === "request") {
      var ind = payload.industry ? ("the " + payload.industry + " benchmark") : "your industry benchmark";
      successMsg.textContent = "Thanks! We'll email you " + ind + " as soon as it's live.";
    } else {
      successMsg.textContent = "Check your inbox — we'll send " + (payload.asset || "it") + " over shortly.";
    }
  }

  // Auto-open (exit-intent + scroll) for pages that opt in via <body data-lead-auto="asset label">.
  // Fires once per session, never on load, and never if the visitor already submitted.
  function armAuto() {
    var asset = document.body.getAttribute("data-lead-auto");
    if (!asset) return;
    try {
      if (localStorage.getItem("pmf_lead_email")) return;       // already a lead
      if (sessionStorage.getItem("pmf_lead_auto_shown")) return; // already nudged this visit
    } catch (e) {}

    var fired = false;
    function fire() {
      if (fired || modal.classList.contains("is-open")) return;
      fired = true;
      try { sessionStorage.setItem("pmf_lead_auto_shown", "1"); } catch (e) {}
      openModal("magnet", asset, null);
      cleanup();
    }
    function onMouseOut(e) { if (e.clientY <= 0 && !e.relatedTarget) fire(); } // exit-intent (desktop)
    function onScroll() {
      var p = (window.scrollY + window.innerHeight) / document.documentElement.scrollHeight;
      if (p > 0.55) fire();
    }
    function cleanup() {
      document.removeEventListener("mouseout", onMouseOut);
      window.removeEventListener("scroll", onScroll);
    }
    document.addEventListener("mouseout", onMouseOut);
    window.addEventListener("scroll", onScroll, { passive: true });
    setTimeout(fire, 40000); // fallback for touch devices where exit-intent doesn't fire
  }

  function init() {
    var holder = document.createElement("div");
    holder.innerHTML = MODAL;
    document.body.appendChild(holder.firstChild);
    modal = document.getElementById("pmfLeadModal");
    form = qs(".lead-form");
    title = qs(".lead-title");
    sub = qs(".lead-sub");
    industryInput = qs(".lead-industry");
    emailInput = qs(".lead-email");
    hpInput = qs(".lead-hp-input");
    errorBox = qs(".lead-error");
    submitBtn = qs(".lead-submit");
    successBox = qs(".lead-success");
    successMsg = qs(".lead-success-msg");

    form.addEventListener("submit", submit);

    // triggers anywhere on the page
    document.addEventListener("click", function (e) {
      var t = e.target.closest("[data-lead-open]");
      if (t) {
        e.preventDefault();
        openModal(t.getAttribute("data-lead-open"), t.getAttribute("data-lead-asset"), t);
        return;
      }
      if (e.target.closest("[data-lead-close]")) { closeModal(); }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && modal.classList.contains("is-open")) closeModal();
    });

    armAuto();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else { init(); }
})();
