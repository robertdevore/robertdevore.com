(function () {
  "use strict";
  var current = location.pathname.replace(/index\.html$/, "");
  document.querySelectorAll(".site-nav a,.site-menu a").forEach(function (link) {
    if (link.pathname.replace(/index\.html$/, "") === current) link.setAttribute("aria-current", "page");
    link.addEventListener("click", function () { var menu = link.closest("details"); if (menu) menu.removeAttribute("open"); });
  });

  document.querySelectorAll(".listing-card-image-link").forEach(function (link) {
    var card = link.closest(".listing-card");
    var title = card ? card.querySelector(".listing-card-title") : null;
    if (title) link.setAttribute("aria-label", "Open " + title.textContent.trim());
  });

  var termTargets = {
    "ai": "/tag/ai/",
    "essays": "/tag/essays/",
    "engineering": "/tag/engineering/",
    "wordpress": "/tag/wordpress/",
    "wordpress archive": "/tag/wordpress/",
    "woocommerce": "/tag/woocommerce/"
  };
  document.querySelectorAll(".listing-card-tags .tag,.article-terms .tag").forEach(function (tag) {
    var label = tag.textContent.trim();
    var key = label.toLowerCase();
    var href = termTargets[key];
    if (!href || tag.tagName === "A") return;
    var link = document.createElement("a");
    link.className = tag.className;
    link.href = href;
    link.textContent = key === "wordpress archive" ? "WordPress" : label;
    tag.replaceWith(link);
  });

  if (window.ScrambleDecode && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var titles = document.querySelectorAll(".section-heading h2,.project-feature h2,.project-secondary h2,.project-link-bank h2,.project-link-bank__columns a,.flagship-panel h3,.home-focus .sk-card h3,.home-principles h3,.project-secondary h3,.article-related-grid .listing-card a,.clarity-grid h2,.about-map h3,.about-timeline h2,.about-proof h3");
    function runTitle(title) {
      if (title.hasAttribute("data-scramble-complete")) return;
      var headingAnchor = title.querySelector(":scope > .heading-anchor");
      if (headingAnchor) headingAnchor.remove();
      var original = (title.getAttribute("data-text") || title.textContent).trim();
      if (!original) {
        if (headingAnchor) title.append(headingAnchor);
        return;
      }
      title.setAttribute("aria-label", original);
      title.setAttribute("data-scrambling", "true");
      title.textContent = "";
      title.setAttribute("data-scramble-complete", "true");
      window.ScrambleDecode.scramble(title, {
        text: original,
        duration: 680 + Math.min(420, original.length * 12),
        pool: "█▓▒░<>/\\#[]{}=+*01"
      }).finished.then(function () {
        title.textContent = original;
        if (headingAnchor) title.append(" ", headingAnchor);
        title.removeAttribute("data-scrambling");
      });
    }
    if ("IntersectionObserver" in window) {
      var titleObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          titleObserver.unobserve(entry.target);
          runTitle(entry.target);
        });
      }, { rootMargin: "0px 0px -12% 0px", threshold: 0.25 });
      titles.forEach(function (title) { titleObserver.observe(title); });
    } else {
      titles.forEach(runTitle);
    }
  }

  document.querySelectorAll(".article-content,.page-content").forEach(function (content) {
    var walker = document.createTreeWalker(content, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        var parent = node.parentElement;
        if (!parent || /^(A|CODE|PRE|SCRIPT|STYLE|TEXTAREA)$/i.test(parent.tagName)) return NodeFilter.FILTER_REJECT;
        return /_[^_\n]+_/.test(node.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      }
    });
    var textNodes = [];
    while (walker.nextNode()) textNodes.push(walker.currentNode);
    textNodes.forEach(function (node) {
      var fragment = document.createDocumentFragment();
      var parts = node.nodeValue.split(/(_[^_\n]+_)/g);
      parts.forEach(function (part) {
        if (/^_[^_\n]+_$/.test(part)) {
          var em = document.createElement("em");
          em.textContent = part.slice(1, -1);
          fragment.append(em);
        } else if (part) {
          fragment.append(document.createTextNode(part));
        }
      });
      node.parentNode.replaceChild(fragment, node);
    });

    Array.from(content.querySelectorAll("p")).forEach(function (paragraph) {
      var fence = paragraph.textContent.trim().match(/^```([a-z0-9_-]*)$/i);
      if (!fence) return;
      var codeLines = [];
      var cursor = paragraph.nextElementSibling;
      while (cursor && cursor.tagName === "P" && cursor.textContent.trim() !== "```") {
        codeLines.push(cursor.textContent);
        cursor = cursor.nextElementSibling;
      }
      if (!cursor || cursor.tagName !== "P" || cursor.textContent.trim() !== "```") return;
      var pre = document.createElement("pre");
      var code = document.createElement("code");
      if (fence[1]) code.className = "language-" + fence[1].toLowerCase();
      code.textContent = codeLines.join("\n");
      pre.append(code);
      var current = paragraph.nextElementSibling;
      while (current && current !== cursor) {
        var next = current.nextElementSibling;
        current.remove();
        current = next;
      }
      cursor.remove();
      paragraph.replaceWith(pre);
    });

    Array.from(content.querySelectorAll("p")).forEach(function (paragraph) {
      var text = paragraph.textContent.trim();
      if (!/^(git clone https:\/\/github\.com\/robertdevore\/zero-cool-cli|cd zero-cool-cli|\.\/install\.sh|zero-cool zero-cool --profile)$/.test(text)) return;
      var pre = document.createElement("pre");
      var code = document.createElement("code");
      code.textContent = text;
      pre.append(code);
      paragraph.replaceWith(pre);
    });

    var used = {};
    var headings = Array.from(content.querySelectorAll("h2,h3"));
    var relatedHeading = content.classList.contains("article-content") ? headings.find(function (heading) {
      return /^(related writing|related reading)$/i.test(heading.textContent.trim());
    }) : null;
    if (relatedHeading) {
      relatedHeading.textContent = "Related Reading";
      relatedHeading.classList.add("article-related__title");
      var relatedList = relatedHeading.nextElementSibling;
      if (relatedList && relatedList.tagName === "UL") {
        var relatedSection = document.createElement("section");
        relatedSection.className = "article-related";
        relatedSection.setAttribute("aria-labelledby", "related-reading-title");
        relatedHeading.id = "related-reading-title";
        relatedHeading.parentNode.insertBefore(relatedSection, relatedHeading);
        relatedSection.append(relatedHeading, relatedList);
        relatedList.className = "article-related-grid";
        Array.from(relatedList.children).forEach(function (item) { item.className = "listing-card"; });
      }
    }
    var tocHeadings = headings.filter(function (heading) { return heading !== relatedHeading; });
    tocHeadings.forEach(function (heading) {
      if (heading.hasAttribute("data-no-heading-anchor")) return;
      var base = heading.textContent.toLowerCase().normalize("NFKD").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "section";
      var id = base, index = 2;
      while (used[id] || document.getElementById(id)) id = base + "-" + index++;
      used[id] = true; heading.id = id;
      var anchor = document.createElement("a"); anchor.className = "heading-anchor"; anchor.href = "#" + id; anchor.setAttribute("aria-label", "Link to " + heading.textContent); anchor.textContent = "#"; heading.append(" ", anchor);
    });
    if (content.classList.contains("article-content") && tocHeadings.length >= 3) {
      var nav = document.createElement("nav"); nav.className = "article-toc"; nav.setAttribute("aria-label", "On this page");
      var title = document.createElement("p"); title.className = "article-toc__title"; title.textContent = "On this page"; nav.append(title);
      var list = document.createElement("ol");
      tocHeadings.forEach(function (heading) { var item = document.createElement("li"), link = document.createElement("a"); if (heading.tagName === "H3") item.className = "article-toc__nested"; link.href = "#" + heading.id; link.textContent = heading.firstChild.textContent; item.append(link); list.append(item); });
      nav.append(list); content.insertBefore(nav, content.firstChild);
    }
  });

  document.querySelectorAll(".article-content pre,.page-content pre").forEach(function (pre) {
    pre.tabIndex = 0;
    var figure = document.createElement("figure"); figure.className = "sk-code-block"; pre.parentNode.insertBefore(figure, pre); figure.append(pre);
    if (!navigator.clipboard) return;
    var caption = document.createElement("figcaption"), label = document.createElement("span"), button = document.createElement("button"), status = document.createElement("span");
    label.textContent = "Code"; button.type = "button"; button.textContent = "Copy"; status.className = "sk-sr-only"; status.setAttribute("aria-live", "polite"); caption.append(label, button, status); figure.insertBefore(caption, pre);
    button.addEventListener("click", function () { navigator.clipboard.writeText(pre.textContent).then(function () { button.textContent = "Copied"; status.textContent = "Code copied to clipboard"; setTimeout(function () { button.textContent = "Copy"; }, 1800); }); });
  });

  var contactForm = document.querySelector("[data-contact-form]");
  if (contactForm) contactForm.addEventListener("submit", function (event) {
    event.preventDefault();
    var data = new FormData(contactForm);
    var subject = data.get("subject") || "Website inquiry";
    var body = [
      "Name: " + (data.get("name") || ""),
      "Email: " + (data.get("email") || ""),
      "Relevant link: " + (data.get("link") || "Not provided"),
      "",
      data.get("message") || ""
    ].join("\n");
    window.location.href = "mailto:hello@robertdevore.com?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
  });
})();
