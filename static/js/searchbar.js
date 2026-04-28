let allProducts = JSON.parse(document.getElementById("products-data").textContent);
let searchTerm = "";
let userInput = document.getElementById("search");
userInput.addEventListener("input", showProducts);

/**
 * The function filters products by the searchTerm using findProducts(), and 
 * show them on the page.
 */
function showProducts() {
    searchTerm = userInput.value.toLowerCase();
    let showList = findProducts();
    let articleBoxEl = document.getElementById("article-box");
    articleBoxEl.innerHTML = "";
    for (let product of showList) {
        let article = createArticleElement(product);
        articleBoxEl.append(article);
    }
}
/**
 Find products that match the search term.
 */
function findProducts() {
    let searchedProducts = [];
    for (let i = 0; i < allProducts.length; i++) {
        productLowercase = allProducts[i].product_name.toLowerCase();
        if (productLowercase.indexOf(searchTerm) > -1) { // searches for a substring in a string, return -1 if not present
            searchedProducts.push(allProducts[i]);
        }
    }
    return searchedProducts;
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
        .join(", "); // combines all string into a line separated by commas
    p.innerHTML = priceText;

    a.appendChild(img);
    a.appendChild(h3);
    a.appendChild(p);
    article.appendChild(a);

    return article;
}



