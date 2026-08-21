/* Campaign countdown — one timestamp drives all three displays
   (sale bar, hero chip, urgency band). When it expires the sale bar
   and urgency band are removed, per the handoff spec. */

(function () {
  'use strict';

  // Campaign end: 47h 23m 59s from first load, persisted so a refresh
  // continues the same countdown instead of restarting it.
  var KEY = 'decathlon.campaignEndsAt';
  var DEFAULT_MS = ((47 * 60 + 23) * 60 + 59) * 1000;

  var endsAt = Number(window.localStorage.getItem(KEY));
  if (!endsAt || endsAt < Date.now()) {
    endsAt = Date.now() + DEFAULT_MS;
    window.localStorage.setItem(KEY, String(endsAt));
  }

  var nodes = Array.prototype.slice.call(document.querySelectorAll('[data-cd]'));
  var saleBar = document.querySelector('[data-sale-bar]');
  var urgency = document.querySelector('[data-urgency]');

  function pad(n) { return n < 10 ? '0' + n : String(n); }

  function tick() {
    var left = Math.max(0, endsAt - Date.now());

    if (left === 0) {
      if (saleBar) saleBar.hidden = true;
      if (urgency) urgency.hidden = true;
      return;
    }

    var total = Math.floor(left / 1000);
    var parts = {
      hrs: pad(Math.floor(total / 3600)),
      min: pad(Math.floor(total / 60) % 60),
      sec: pad(total % 60)
    };

    nodes.forEach(function (el) {
      // data-cd="min2" / "sec2" are the second instance of the same unit
      var unit = el.getAttribute('data-cd').replace(/\d+$/, '');
      if (parts[unit] !== undefined) el.textContent = parts[unit];
    });

    window.setTimeout(tick, 1000 - (Date.now() % 1000));
  }

  tick();
})();
