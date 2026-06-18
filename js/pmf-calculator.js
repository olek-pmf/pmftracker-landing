/* ==========================================================================
   PMFtracker — interactive PMF score calculator
   Reusable. Drop a <div class="pmf-calc"> with the markup (see data-pmf-*)
   anywhere and this script wires it up. Supports multiple instances per page.
   No dependencies.
   ========================================================================== */
(function () {
  "use strict";

  function clampInt(v) {
    var n = parseInt(v, 10);
    if (isNaN(n) || n < 0) return 0;
    return n;
  }

  function verdict(score, total) {
    if (total === 0) {
      return { label: "Enter your responses to see your score", tone: "neutral" };
    }
    if (score >= 50) {
      return { label: "Strong fit — must-have territory", tone: "strong" };
    }
    if (score >= 40) {
      return { label: "Product-market fit — you're over the line", tone: "good" };
    }
    if (score >= 25) {
      return { label: "Not there yet — but you have a real foothold to build on", tone: "mid" };
    }
    return { label: "Early — focus on the users who'd be very disappointed", tone: "low" };
  }

  function reliability(total) {
    if (total === 0) return "";
    if (total < 30) return "Under 30 responses — read the comments, treat the % as directional only.";
    if (total < 100) return "30–100 responses — a directional signal you can act on.";
    return "100+ responses — a reliable score you can show investors.";
  }

  function initOne(root) {
    var very = root.querySelector('[data-pmf="very"]');
    var somewhat = root.querySelector('[data-pmf="somewhat"]');
    var not = root.querySelector('[data-pmf="not"]');
    var out = root.querySelector('[data-pmf="score"]');
    var verdictEl = root.querySelector('[data-pmf="verdict"]');
    var totalEl = root.querySelector('[data-pmf="total"]');
    var relEl = root.querySelector('[data-pmf="reliability"]');
    var fill = root.querySelector('[data-pmf="fill"]');

    if (!very || !somewhat || !not || !out) return;

    function update() {
      var v = clampInt(very.value);
      var s = clampInt(somewhat.value);
      var n = clampInt(not.value);
      var total = v + s + n;
      var score = total > 0 ? Math.round((v / total) * 100) : 0;

      out.textContent = score + "%";
      var vd = verdict(score, total);
      if (verdictEl) {
        verdictEl.textContent = vd.label;
        verdictEl.setAttribute("data-tone", vd.tone);
      }
      if (totalEl) {
        totalEl.textContent = total === 0
          ? "0 valid responses"
          : total + " valid response" + (total === 1 ? "" : "s");
      }
      if (relEl) relEl.textContent = reliability(total);
      if (fill) fill.style.width = Math.min(score, 100) + "%";

      root.setAttribute("data-state", total === 0 ? "empty" : vd.tone);
    }

    [very, somewhat, not].forEach(function (el) {
      el.addEventListener("input", update);
      el.addEventListener("change", update);
    });
    update();
  }

  function initAll() {
    var roots = document.querySelectorAll(".pmf-calc");
    for (var i = 0; i < roots.length; i++) initOne(roots[i]);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAll);
  } else {
    initAll();
  }
})();
