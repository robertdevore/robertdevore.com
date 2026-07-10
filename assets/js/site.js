(function () {
  "use strict";
  var current = location.pathname.replace(/index\.html$/, "");
  document.querySelectorAll(".site-nav a,.site-menu a").forEach(function (link) {
    if (link.pathname.replace(/index\.html$/, "") === current) link.setAttribute("aria-current", "page");
    link.addEventListener("click", function () { var menu = link.closest("details"); if (menu) menu.removeAttribute("open"); });
  });

  document.querySelectorAll(".article-content,.page-content").forEach(function (content) {
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
