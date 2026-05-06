let offset = 20;
const buttonEl = document.getElementById("loadMoreProducts");
buttonEl.addEventListener("click", requestNextBatch);

async function requestNextBatch() {
    const response = await fetch(`/api/products?offset=${offset}`);
    const products = await response.json();
    appendProducts(products);
    offset += 20;
}

function appendProducts(products) {
    const articleBox = document.getElementById("article-box");
    for (product of products) {
        const article = createArticleElement(product);
        articleBox.appendChild(article);
    }

}

function createArticleElement(product) {
    let article = document.createElement("article");

    let a = document.createElement("a");
    a.href = `/product_page?id=${product.product_id}`;

    let img = document.createElement("img");
    img.src = `${product.image_url}`;

    let h3 = document.createElement("h3");
    h3.innerText = `${product.product_name}`;

    let p = document.createElement("p");
    let priceText = product.prices_at_store
        .map(p => `${p.price} kr hos ${p.store_name}`) // loops over each item and converts it into a string
        .join(", "); // combines all strings into a line separated by commas
    p.innerHTML = priceText;

    a.appendChild(img);
    a.appendChild(h3);
    a.appendChild(p);
    article.appendChild(a);

    return article;
}