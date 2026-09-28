(() => {
  "use strict";

  const mount = document.getElementById("cms-menu");
  const nav = document.getElementById("cms-category-nav");
  if (!mount) return;

  const el = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined && text !== null) node.textContent = text;
    return node;
  };

  const renderProducts = (group, parent) => {
    const wrap = el("div", "product-group");
    wrap.appendChild(el("h3", "", group.title || ""));

    (group.items || []).forEach((item) => {
      const article = el("article", "product");
      const line = el("div", "product-line");
      line.appendChild(el("h4", "", item.name || ""));
      line.appendChild(el("strong", "price", item.price || ""));
      article.appendChild(line);

      if (item.description) article.appendChild(el("p", "", item.description));
      if (item.allergens) article.appendChild(el("small", "", `Allergene: ${item.allergens}`));
      wrap.appendChild(article);
    });
    parent.appendChild(wrap);
  };

  const renderFlavors = (group, parent) => {
    const wrap = el("div", "product-group");
    wrap.appendChild(el("h3", "", group.title || ""));
    const ul = el("ul", "flavors");
    (group.items || []).forEach((item) => ul.appendChild(el("li", "", item)));
    wrap.appendChild(ul);
    parent.appendChild(wrap);
  };

  const render = (data) => {
    if (nav) nav.replaceChildren();
    mount.replaceChildren();

    (data.categories || []).forEach((category, index) => {
      const id = `category-${index + 1}`;
      if (nav) {
        const link = el("a", "", category.title || `Kategorie ${index + 1}`);
        link.href = `#${id}`;
        nav.appendChild(link);
      }

      const section = el("section", "category-section");
      section.id = id;
      const headingId = `heading-${index + 1}`;
      section.setAttribute("aria-labelledby", headingId);

      const intro = el("div", "category-intro");
      const copy = el("div");
      copy.appendChild(el("span", "eyebrow", `${String(index + 1).padStart(2, "0")} / ${data.menu_label || "KARTE"}`));
      const h2 = el("h2", "", category.title || "");
      h2.id = headingId;
      copy.appendChild(h2);
      if (category.subtitle) copy.appendChild(el("p", "", category.subtitle));
      intro.appendChild(copy);

      if (category.image) {
        const img = document.createElement("img");
        img.src = category.image;
        img.width = 600;
        img.height = 400;
        img.alt = "";
        img.loading = "lazy";
        intro.appendChild(img);
      }
      section.appendChild(intro);

      const grid = el("div", "product-grid");
      if (category.scoop_price) {
        const scoop = el("p", "scoop-price");
        scoop.appendChild(el("strong", "", category.scoop_price));
        scoop.appendChild(document.createTextNode(" pro Kugel"));
        grid.appendChild(scoop);
      }

      (category.groups || []).forEach((group) => {
        if (group.type === "flavors") renderFlavors(group, grid);
        else renderProducts(group, grid);
      });

      section.appendChild(grid);
      mount.appendChild(section);
    });
  };

  fetch(mount.dataset.source, { cache: "no-store" })
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then(render)
    .catch((error) => {
      console.error("Menü konnte nicht geladen werden:", error);
      const p = el("p", "price-note", "Die Karte konnte gerade nicht geladen werden. Bitte Seite neu laden.");
      mount.replaceChildren(p);
    });
})();
