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

function renderProducts(data) {
  grid.innerHTML = "";

  if (data.length === 0) {
    grid.innerHTML = "<p>No products found</p>";
    return;
  }

  data.forEach((p) => {
    const card = document.createElement("div");

    const stockBadge = p.stock === 0
      ? `<span class="badge out-of-stock">Out of Stock</span>`
      : p.stock < 5
        ? `<span class="badge low-stock">&#9888; Low Stock</span>`
        : "";

    card.innerHTML = `
      <h3>${p.name} ${stockBadge}</h3>
      <p>Category: ${p.category}</p>
      <p>Price: ₹${p.price}</p>
      <p>Stock: ${p.stock}</p>
      <button onclick="deleteProduct(${p.id})">Delete</button>
      <button class="edit-btn" onclick="openEditModal(${p.id})">Edit</button>
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
  createEditModal();
};

function updateAnalytics() {
  const selectedCategory = categoryFilter ? categoryFilter.value : "all";
  const query = searchInput ? searchInput.value.toLowerCase() : "";

  // Show analytics for selected category only, or all if none selected
  let data = selectedCategory === "all"
    ? [...products]
    : products.filter(p => p.category === selectedCategory);

  if (query) {
    data = data.filter(p => p.name.toLowerCase().includes(query));
  }

  if (lowStockBtn && lowStockBtn.classList.contains("active")) {
    data = data.filter(p => p.stock < 5);
  }

  const total = data.length;
  const value = data.reduce((sum, p) => sum + (p.price * p.stock), 0);
  const outOfStock = data.filter(p => p.stock === 0).length;

  document.getElementById("totalProducts").innerText = `Total Products: ${total}`;
  document.getElementById("totalValue").innerText = `Total Value: ₹${value}`;
  document.getElementById("outOfStock").innerText = `Out of Stock: ${outOfStock}`;

  // Category-wise count (how many products per category)
  const categoryCount = {};

  data.forEach(p => {
    if (categoryCount[p.category]) {
      categoryCount[p.category]++;
    } else {
      categoryCount[p.category] = 1;
    }
  });

  let categoryHTML = "";

  for (let cat in categoryCount) {
    categoryHTML += `<p>${cat}: ${categoryCount[cat]}</p>`;
  }

  document.getElementById("categoryStats").innerHTML = categoryHTML;
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
  applyFilters();
  updateAnalytics();
}

document.getElementById("productForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const name = document.getElementById("name").value;
  const price = +document.getElementById("price").value;
  const stock = +document.getElementById("stock").value;
  const category = document.getElementById("category").value;

  if (!name || price <= 0 || stock < 0 || !category) {
    alert("Invalid input");
    return;
  }

  const newProduct = {
    id: Date.now(),
    name,
    price,
    stock,
    category
  };

  products.push(newProduct);
  saveAndRender();
  this.reset();
});

// Create a separate list for filtered/sorted data
// Original products array stays untouched
let filteredProducts = [...products];

const searchInput = document.getElementById("searchInput");
const categoryFilter = document.getElementById("categoryFilter");
const lowStockBtn = document.getElementById("lowStockBtn");
const sortSelect = document.getElementById("sortSelect");

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

function applyFilters() {
  let result = [...products];

  const query = searchInput.value.toLowerCase();
  const category = categoryFilter.value;
  const sort = sortSelect.value;

  if (query) {
    result = result.filter(p => p.name.toLowerCase().includes(query));
  }

  if (category !== "all") {
    result = result.filter(p => p.category === category);
  }

  if (lowStockBtn.classList.contains("active")) {
    result = result.filter(p => p.stock < 5);
  }

  if (sort === "low") {
    result.sort((a, b) => a.price - b.price);
  } else if (sort === "high") {
    result.sort((a, b) => b.price - a.price);
  } else if (sort === "az") {
    result.sort((a, b) => a.name.localeCompare(b.name));
  } else if (sort === "za") {
    result.sort((a, b) => b.name.localeCompare(a.name));
  }

  filteredProducts = result;
  renderProducts(filteredProducts);
  updateAnalytics();
}

searchInput.addEventListener("input", applyFilters);

categoryFilter.addEventListener("change", applyFilters);

sortSelect.addEventListener("change", applyFilters);

lowStockBtn.addEventListener("click", function () {
  this.classList.toggle("active");
  applyFilters();
});

// ── Edit Feature ──────────────────────────────

let editingId = null;

function createEditModal() {
  const modal = document.createElement("div");
  modal.id = "editModal";
  modal.innerHTML = `
    <div id="editModalBox">
      <h2>Edit Product</h2>
      <label>Name</label>
      <input type="text" id="editName">
      <label>Price</label>
      <input type="number" id="editPrice">
      <label>Stock</label>
      <input type="number" id="editStock">
      <label>Category</label>
      <select id="editCategory">
        <option value="electronics">Electronics</option>
        <option value="clothing">Clothing</option>
        <option value="books">Books</option>
        <option value="accessories">Accessories</option>
      </select>
      <button id="saveEditBtn">Save</button>
      <button id="cancelEditBtn">Cancel</button>
    </div>
  `;
  document.body.appendChild(modal);

  document.getElementById("saveEditBtn").addEventListener("click", saveEdit);
  document.getElementById("cancelEditBtn").addEventListener("click", closeEditModal);
  document.getElementById("editModal").addEventListener("click", function (e) {
    if (e.target === this) closeEditModal();
  });
}

function openEditModal(id) {
  const p = products.find(p => p.id === id);
  if (!p) return;
  editingId = id;
  document.getElementById("editName").value = p.name;
  document.getElementById("editPrice").value = p.price;
  document.getElementById("editStock").value = p.stock;
  document.getElementById("editCategory").value = p.category;
  document.getElementById("editModal").style.display = "flex";
}

function closeEditModal() {
  document.getElementById("editModal").style.display = "none";
  editingId = null;
}

function saveEdit() {
  const name = document.getElementById("editName").value.trim();
  const price = +document.getElementById("editPrice").value;
  const stock = +document.getElementById("editStock").value;
  const category = document.getElementById("editCategory").value;

  if (!name || price <= 0 || stock < 0 || !category) {
    alert("Invalid input");
    return;
  }

  const index = products.findIndex(p => p.id === editingId);
  products[index] = { id: editingId, name, price, stock, category };

  closeEditModal();
  saveAndRender();
}