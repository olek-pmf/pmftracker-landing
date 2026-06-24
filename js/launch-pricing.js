/* Dynamic launch pricing for the homepage #pricing section.
 * Fetches remaining launch spots from the public Supabase edge function and:
 *  - shows a "N/100 spots left" banner while spots remain;
 *  - when sold out, hides the discounted prices and shows the list price only.
 * Progressive enhancement: if the fetch fails, the static launch pricing stays as-is.
 */
(function () {
  var ENDPOINT = "https://nwgmoyedsdgivlhcgzgw.supabase.co/functions/v1/launch-spots";

  function onReady(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  onReady(function () {
    var banner = document.querySelector("[data-launch-spots]");

    fetch(ENDPOINT)
      .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
      .then(function (data) {
        if (!data || typeof data.remaining !== "number") return;
        var total = data.total || 100;
        var remaining = data.remaining;

        if (remaining > 0) {
          if (banner) {
            banner.textContent = "🔥 Launch pricing — " + remaining + " of " + total + " spots left";
            banner.style.display = "";
          }
          return;
        }

        // Sold out: surface the message and switch the cards to list price only.
        if (banner) {
          banner.textContent = "Launch pricing has ended — standard pricing now applies";
          banner.style.display = "";
        }
        // Hide the discounted amounts ($79 / $149).
        document.querySelectorAll(".plan-9, .plan-9-right").forEach(function (el) {
          el.style.display = "none";
        });
        // Promote the list prices ($99 / $199) from struck-through to the active price.
        document.querySelectorAll(".plan-, .plan---right").forEach(function (el) {
          el.style.textDecoration = "none";
          el.style.opacity = "1";
        });
      })
      .catch(function () { /* leave the static launch pricing untouched */ });
  });
})();
