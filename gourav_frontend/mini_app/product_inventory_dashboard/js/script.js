// Try to get products from localStorage If nothing is stored, we will use default data
let products = JSON.parse(localStorage.getItem("products")) || [
    { id: 1, name: "Pro Laptop", price: 55000, stock: 5, category: "electronics" },
    { id: 2, name: "Cotton Shirt", price: 1500, stock: 10, category: "clothing" },
    { id: 3, name: "JS Guide Book", price: 500, stock: 0, category: "books" },
    { id: 4, name: "Smart Watch", price: 2000, stock: 3, category: "accessories" },
    { id: 5, name: "Bluetooth Buds", price: 3000, stock: 12, category: "electronics" },
    { id: 6, name: "Denim Jeans", price: 2500, stock: 4, category: "clothing" },
    { id: 7, name: "Data Structures", price: 800, stock: 2, category: "books" },
    { id: 8, name: "Leather Belt", price: 1200, stock: 15, category: "accessories" },
    { id: 9, name: "Gaming Mouse", price: 4500, stock: 1, category: "electronics" },
    { id: 10, name: "Travel Backpack", price: 3500, stock: 0, category: "accessories" }
];

// Getting reference of product grid where cards will be shown

const grid = document.getElementById("productGrid");


// This function is responsible for showing products on UI
// It clears old data and re-renders updated list every time
function renderProducts(data) {
  grid.innerHTML = "";

  if (data.length === 0) {
    grid.innerHTML = "<p>No products found</p>";
    return;
  }

  data.forEach((p) => {
    const card = document.createElement("div");

    card.innerHTML = `
      <h3>${p.name}</h3>
      <p>Category: ${p.category}</p>
      <p>Price: ₹${p.price}</p>
      <p>Stock: ${p.stock}</p>
      <button onclick="deleteProduct(${p.id})">Delete</button>
    `;

    grid.appendChild(card);
  });
}

// This simulates fetching data from server (like real API)
// We are adding delay using setTimeout to mimic loading
function fetchProducts() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(products);
    }, 1500);
  });
}

// When page loads, we show loading first
// Then fetch data and render it
window.onload = async function () {
  grid.innerHTML = "<p>Loading products...</p>";

  const data = await fetchProducts();

  renderProducts(data);
  updateAnalytics();
  loadCategories();
};
// This function calculates dashboard values
// Like total products, total value and out of stock count
function updateAnalytics() {
  const total = products.length;

  // Total inventory value = price * stock for each product
  const value = products.reduce((sum, p) => sum + (p.price * p.stock), 0);

  // Count products where stock is 0
  const outOfStock = products.filter(p => p.stock === 0).length;

  document.getElementById("totalProducts").innerText = `Total Products: ${total}`;
  document.getElementById("totalValue").innerText = `Total Value: ₹${value}`;
  document.getElementById("outOfStock").innerText = `Out of Stock: ${outOfStock}`;
}

// This function handles deletion of product
// It removes product from array and updates UI + storage
function deleteProduct(id) {
  products = products.filter(p => p.id !== id);
  saveAndRender();
}

// This function saves data in localStorage
// and re-renders UI after any change
function saveAndRender() {
  localStorage.setItem("products", JSON.stringify(products));
  renderProducts(products);
  updateAnalytics();
}
// Handling form submission for adding new product
document.getElementById("productForm").addEventListener("submit", function(e) {
  e.preventDefault();

  // Getting values from input fields
  const name = document.getElementById("name").value;
  const price = +document.getElementById("price").value;
  const stock = +document.getElementById("stock").value;
  const category = document.getElementById("category").value;

  // Basic validation
  if (!name || price <= 0 || stock < 0 || !category) {
    alert("Invalid input");
    return;
  }

  // Creating new product object
  const newProduct = {
    id: Date.now(), // unique id using timestamp
    name,
    price,
    stock,
    category
  };

  // Adding new product to array
  products.push(newProduct);

  // Save and update UI
  saveAndRender();

  // Clear form after submission
  this.reset();
});

// Create a separate list for filtered/sorted data
// Original products array stays untouched

let filteredProducts = [...products];

// Getting search input
const searchInput = document.getElementById("searchInput");

// When user types, filter products
searchInput.addEventListener("input", function () {

  const query = this.value.toLowerCase();

  // Filter products based on name
  filteredProducts = products.filter(p =>
    p.name.toLowerCase().includes(query)
  );

  // Re-render UI
  renderProducts(filteredProducts);
});


const categoryFilter = document.getElementById("categoryFilter");

// Populate category dropdown dynamically
function loadCategories() {
  const categories = [...new Set(products.map(p => p.category))];

  categories.forEach(cat => {
    const option = document.createElement("option");
    option.value = cat;
    option.textContent = cat;
    categoryFilter.appendChild(option);
  });
}

// Filter by category
categoryFilter.addEventListener("change", function () {

  if (this.value === "all") {
    filteredProducts = [...products];
  } else {
    filteredProducts = products.filter(p => p.category === this.value);
  }

  renderProducts(filteredProducts);
});

const lowStockBtn = document.getElementById("lowStockBtn");

// Toggle low stock view
lowStockBtn.addEventListener("click", function () {

  filteredProducts = products.filter(p => p.stock < 5);

  renderProducts(filteredProducts);
});

