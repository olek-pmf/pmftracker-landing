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

  // Bands mirror the PMFtracker app: >=40 Strong PMF Achieved, >=30 Close to PMF,
  // <30 PMF Not Achieved. (>=50 surfaced as exceptional for extra nuance.)
  function verdict(score, total) {
    if (total === 0) {
      return { label: "Enter your responses to see your score", tone: "neutral" };
    }
    if (score >= 50) {
      return { label: "Exceptional — deep must-have fit. Focus on scaling.", tone: "strong" };
    }
    if (score >= 40) {
      return { label: "Strong PMF achieved — focus on growth & scaling.", tone: "good" };
    }
    if (score >= 30) {
      return { label: "Close to PMF — you're nearly there. Keep iterating.", tone: "mid" };
    }
    return { label: "PMF not yet — focus on your very-disappointed users.", tone: "low" };
  }

  // Reliability mirrors the app's data-quality bands: high >=100, medium >=40, low <40.
  function reliability(total) {
    if (total === 0) return "";
    if (total < 40) return "Under 40 responses — directional only. Aim for 40+ before you act on it.";
    if (total < 100) return "40+ responses — solid data you can act on.";
    return "100+ responses — a high-confidence score you can show investors.";
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
