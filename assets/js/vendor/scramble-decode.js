(function (global) {
"use strict";
/*
 * scramble-decode — deterministic text scramble-decode + glitch pop effects.
 *
 * Two effects, extracted from the KUJO HyperFrames evidence reels:
 *
 *  1. Scramble decode: text resolves left-to-right out of a churn of junk
 *     glyphs, like a signal locking in.
 *  2. Glitch pop: a few discrete horizontal shove + skew frames that snap
 *     back to rest, like an analog tracking error.
 *
 * Everything is a pure function of progress (0..1) with seeded randomness,
 * so the same inputs always produce the same frame. That makes the effects
 * safe for frame-by-frame video renderers (HyperFrames), scrub-driven
 * timelines (GSAP, Web Animations), and plain old requestAnimationFrame.
 *
 * Zero dependencies. MIT license.
 */

var DEFAULT_POOL = "█▓▒░<>/\\#[]{}=+*01";

function clamp01(p) {
  p = Number(p);
  if (!isFinite(p)) return 0;
  return p < 0 ? 0 : p > 1 ? 1 : p;
}

/* Deterministic LCG. Same seed -> same sequence, every platform. */
function createRng(seed) {
  var s = (seed == null ? 42 : seed) >>> 0;
  return function () {
    s = (s * 1103515245 + 12345) % 2147483648;
    return s / 2147483648;
  };
}

function prefersReducedMotion() {
  return (
    typeof window !== "undefined" &&
    typeof window.matchMedia === "function" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches
  );
}

/* ------------------------------------------------------------------ *
 *  Pure frame functions                                               *
 * ------------------------------------------------------------------ */

/**
 * The scramble text at a given progress. Pure: same (text, progress,
 * options) always returns the same string.
 *
 * Characters left of the resolve point (and spaces) show their final
 * form; the rest churn through the glyph pool as progress advances.
 *
 * @param {string} text      final text
 * @param {number} progress  0..1
 * @param {object} [options] { pool, steps }
 * @returns {string}
 */
function scrambleFrame(text, progress, options) {
  options = options || {};
  var p = clamp01(progress);
  if (p >= 1) return text;
  var pool = options.pool || DEFAULT_POOL;
  var steps = Math.floor(p * (options.steps || 40));
  var resolved = Math.floor(p * text.length);
  var out = "";
  for (var i = 0; i < text.length; i++) {
    var ch = text[i];
    if (i < resolved || ch === " ") out += ch;
    else out += pool[(i * 31 + steps * 7) % pool.length];
  }
  return out;
}

/**
 * The glitch transform at a given progress. Pure and seeded: the pop
 * offsets are fixed by the seed, and progress picks which pop is active.
 *
 * @param {number} progress  0..1 (>= 1 is always at rest)
 * @param {object} [options] { pops, maxShift, maxSkew, seed }
 * @returns {{x: number, skewX: number}}
 */
function glitchFrame(progress, options) {
  options = options || {};
  var p = clamp01(progress);
  var pops = options.pops || 4;
  if (p >= 1) return { x: 0, skewX: 0 };
  var maxShift = options.maxShift == null ? 13 : options.maxShift;
  var maxSkew = options.maxSkew == null ? 2 : options.maxSkew;
  var rng = createRng(options.seed);
  var index = Math.min(Math.floor(p * pops), pops - 1);
  var x = 0;
  var skewX = 0;
  for (var i = 0; i <= index; i++) {
    x = Math.floor(rng() * (maxShift * 2 + 1)) - maxShift;
    skewX = rng() * (maxSkew * 2) - maxSkew;
  }
  return { x: x, skewX: skewX };
}

/* ------------------------------------------------------------------ *
 *  Timeline adapters (bring your own clock: GSAP, WAAPI, renderers)   *
 * ------------------------------------------------------------------ */

/**
 * Returns a setProgress(p) function that writes the scramble frame into
 * the element. Drive it from any timeline:
 *
 *   const seek = createScramble(el);
 *   gsap.to(state, { p: 1, ease: "none", onUpdate: () => seek(state.p) });
 *
 * @param {Element} el
 * @param {object} [options] { text, pool, steps }
 * @returns {(progress: number) => void}
 */
function createScramble(el, options) {
  options = options || {};
  var text =
    options.text != null
      ? options.text
      : el.getAttribute("data-text") || el.textContent || "";
  return function setProgress(progress) {
    el.textContent = scrambleFrame(text, progress, options);
  };
}

/**
 * Returns a setProgress(p) function that applies the glitch transform to
 * the element (translateX + skewX), restoring rest at p >= 1.
 *
 * @param {Element} el
 * @param {object} [options] { pops, maxShift, maxSkew, seed }
 * @returns {(progress: number) => void}
 */
function createGlitch(el, options) {
  return function setProgress(progress) {
    var f = glitchFrame(progress, options);
    el.style.transform =
      f.x === 0 && f.skewX === 0
        ? ""
        : "translateX(" + f.x + "px) skewX(" + f.skewX + "deg)";
  };
}

/* ------------------------------------------------------------------ *
 *  Self-driving animations (requestAnimationFrame)                    *
 * ------------------------------------------------------------------ */

function animate(setProgress, durationMs, onComplete) {
  var cancelled = false;
  var raf = 0;
  var start = null;
  function frame(now) {
    if (cancelled) return;
    if (start === null) start = now;
    var p = durationMs <= 0 ? 1 : (now - start) / durationMs;
    setProgress(p);
    if (p < 1) raf = requestAnimationFrame(frame);
    else if (onComplete) onComplete();
  }
  raf = requestAnimationFrame(frame);
  return function cancel() {
    cancelled = true;
    cancelAnimationFrame(raf);
  };
}

function runEffect(setProgress, durationMs) {
  if (prefersReducedMotion()) durationMs = 0;
  var done;
  var finished = new Promise(function (resolve) {
    done = resolve;
  });
  var cancel = animate(setProgress, durationMs, done);
  return {
    finished: finished,
    cancel: function () {
      cancel();
      setProgress(1);
      done();
    }
  };
}

/**
 * Play the scramble decode on an element right now.
 *
 * @param {Element} el
 * @param {object} [options] { text, duration = 900, pool, steps }
 * @returns {{finished: Promise<void>, cancel: () => void}}
 */
function scramble(el, options) {
  options = options || {};
  var duration = options.duration == null ? 900 : options.duration;
  return runEffect(createScramble(el, options), duration);
}

/**
 * Play the glitch pop on an element right now.
 *
 * @param {Element} el
 * @param {object} [options] { duration = 280, pops, maxShift, maxSkew, seed }
 * @returns {{finished: Promise<void>, cancel: () => void}}
 */
function glitch(el, options) {
  options = options || {};
  var duration = options.duration == null ? 280 : options.duration;
  return runEffect(createGlitch(el, options), duration);
}

/**
 * Scramble, then glitch — the full reel treatment in one call.
 *
 * @param {Element} el
 * @param {object} [options] scramble options plus { glitch: glitchOptions }
 * @returns {{finished: Promise<void>, cancel: () => void}}
 */
function decode(el, options) {
  options = options || {};
  var current = scramble(el, options);
  var cancelled = false;
  var finished = current.finished.then(function () {
    if (cancelled) return;
    current = glitch(el, options.glitch);
    return current.finished;
  });
  return {
    finished: finished,
    cancel: function () {
      cancelled = true;
      current.cancel();
    }
  };
}

/* ------------------------------------------------------------------ *
 *  Declarative auto-init                                              *
 * ------------------------------------------------------------------ */

/**
 * Animate every element matching [data-scramble] under root (default:
 * document). Reads options from data attributes:
 *
 *   data-scramble           -> target text (falls back to textContent)
 *   data-scramble-duration  -> ms
 *   data-scramble-delay     -> ms before starting
 *   data-scramble-pool      -> custom glyph pool
 *   data-scramble-glitch    -> present = add the glitch pop after decode
 *
 * @param {ParentNode} [root]
 * @returns {Array} controllers
 */
function auto(root) {
  root = root || (typeof document !== "undefined" ? document : null);
  if (!root) return [];
  var els = root.querySelectorAll("[data-scramble]");
  var controllers = [];
  Array.prototype.forEach.call(els, function (el) {
    var options = {
      text: el.getAttribute("data-scramble") || undefined,
      duration: el.hasAttribute("data-scramble-duration")
        ? Number(el.getAttribute("data-scramble-duration"))
        : undefined,
      pool: el.getAttribute("data-scramble-pool") || undefined
    };
    var run = el.hasAttribute("data-scramble-glitch") ? decode : scramble;
    var delay = Number(el.getAttribute("data-scramble-delay") || 0);
    if (delay > 0 && !prefersReducedMotion()) {
      var target = options.text != null ? options.text : el.textContent;
      el.textContent = scrambleFrame(target, 0, options);
      options.text = target;
      var controller = { cancel: function () {}, finished: null };
      controller.finished = new Promise(function (resolve) {
        var t = setTimeout(function () {
          var inner = run(el, options);
          controller.cancel = inner.cancel;
          inner.finished.then(resolve);
        }, delay);
        controller.cancel = function () {
          clearTimeout(t);
          el.textContent = target;
          resolve();
        };
      });
      controllers.push(controller);
    } else {
      controllers.push(run(el, options));
    }
  });
  return controllers;
}

var api = {
  DEFAULT_POOL: DEFAULT_POOL,
  scrambleFrame: scrambleFrame,
  glitchFrame: glitchFrame,
  createScramble: createScramble,
  createGlitch: createGlitch,
  scramble: scramble,
  glitch: glitch,
  decode: decode,
  auto: auto,
  createRng: createRng
};

global.ScrambleDecode = api;
})(typeof window !== "undefined" ? window : globalThis);
