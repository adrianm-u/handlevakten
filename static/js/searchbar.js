let allProducts = JSON.parse(document.getElementById("products-data").textContent);
let searchTerm = "";
let userInput = document.getElementById("search");
userInput.addEventListener("input", showProducts);

let selectForm = document.getElementById("sort");
let sortType = localStorage.getItem("sortType") || "name_asc";
selectForm.addEventListener("change", changeSortType);

/**
 The function updates the sortType variable after the user
 changes sort type criteria, and updates the page. 
 */
function changeSortType(e) {
    sortType = e.target.value;
    localStorage.setItem("sortType", e.target.value);
    showProducts()
}

/**
 * The function filters products by the searchTerm using findProducts(), and 
 * updates the article container on the page.
 */
function showProducts() {
    searchTerm = userInput.value.toLowerCase();
    let showList = getVisibleProducts();
    let articleBoxEl = document.getElementById("article-box");
    articleBoxEl.innerHTML = "";
    for (let product of showList) {
        let article = createArticleElement(product);
        articleBoxEl.append(article);
    }
}
/**
 The function finds products that match the search term and sorts them
 by following the sortType criteria.
 */
function getVisibleProducts() {
    let products = [];
    for (let i = 0; i < allProducts.length; i++) {
        productLowercase = allProducts[i].product_name.toLowerCase();
        if (productLowercase.indexOf(searchTerm) > -1) { // searches for a substring in a string, return -1 if not present
            products.push(allProducts[i]);
        }
    }

    if (sortType == "name_asc") {
        products.sort((a, b) => a.product_name.localeCompare(b.product_name));
    }
    else if (sortType == "name_desc") {
        products.sort((a, b) => b.product_name.localeCompare(a.product_name));
    }
    else if (sortType == "price_asc") {
        products.sort((a, b) => a.prices_at_store[0].price - b.prices_at_store[0].price);
    }
    else if (sortType == "price_desc") {
        products.sort((a, b) => b.prices_at_store[0].price - a.prices_at_store[0].price);
    }
    return products;
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

window.onload = function () {
    showProducts() // This ensures that preset sort is applied to products from the start (loading the page)
}



