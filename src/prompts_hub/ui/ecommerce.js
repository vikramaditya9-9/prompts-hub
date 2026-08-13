const productList = document.querySelector('#product-list');
const cartCount = document.querySelector('#cart-count');
const cartItems = document.querySelector('#cart-items');
const subtotalEl = document.querySelector('#subtotal');
const productStatus = document.querySelector('#product-status');
const checkoutForm = document.querySelector('#checkout-form');
const checkoutError = document.querySelector('#checkout-error');
const checkoutSuccess = document.querySelector('#checkout-success');

const cart = new Map();

async function fetchProducts() {
  try {
    const response = await fetch('/api/products');
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.error?.message || 'Unable to load products');
    }
    renderProducts(payload.products || []);
    productStatus.textContent = `${payload.products.length} products ready`;
  } catch (error) {
    productStatus.textContent = 'Catalog unavailable';
    productList.innerHTML = '<p>Unable to load the product catalog right now.</p>';
  }
}

function renderProducts(products) {
  productList.innerHTML = products.map((product) => `
    <article class="product-card">
      <div class="product-meta">
        <span>${product.category}</span>
        <span>Stock ${product.inventory}</span>
      </div>
      <h3>${product.name}</h3>
      <div class="price">$${Number(product.price).toFixed(2)}</div>
      <div class="product-actions">
        <button class="secondary" type="button" data-action="decrease" data-product-id="${product.id}">-</button>
        <span>${cart.get(product.id)?.quantity || 0}</span>
        <button class="secondary" type="button" data-action="increase" data-product-id="${product.id}">+</button>
        <button class="primary" type="button" data-action="add" data-product-id="${product.id}">Add</button>
      </div>
    </article>
  `).join('');
}

function updateCartSummary() {
  const items = Array.from(cart.values());
  cartCount.textContent = items.reduce((sum, item) => sum + item.quantity, 0);
  if (!items.length) {
    cartItems.classList.add('empty');
    cartItems.textContent = 'No items selected.';
    subtotalEl.textContent = '$0.00';
    return;
  }

  cartItems.classList.remove('empty');
  cartItems.innerHTML = items.map((item) => `
    <div class="cart-item">
      <span>${item.name} x ${item.quantity}</span>
      <strong>$${(item.price * item.quantity).toFixed(2)}</strong>
    </div>
  `).join('');
  const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  subtotalEl.textContent = `$${subtotal.toFixed(2)}`;
}

function addToCart(productId, productName, productPrice) {
  const existing = cart.get(productId) || { productId, name: productName, price: productPrice, quantity: 0 };
  existing.quantity += 1;
  cart.set(productId, existing);
  updateCartSummary();
  renderProductsFromExisting();
}

function renderProductsFromExisting() {
  const cards = [...document.querySelectorAll('.product-card')];
  cards.forEach((card) => {
    const productId = card.querySelector('[data-action="add"]').dataset.productId;
    const quantity = cart.get(productId)?.quantity || 0;
    const qtyNode = card.querySelector('span:not(.price)');
    if (qtyNode) qtyNode.textContent = quantity;
  });
}

productList.addEventListener('click', (event) => {
  const button = event.target.closest('button');
  if (!button) return;
  const productId = button.dataset.productId;
  const action = button.dataset.action;
  const card = button.closest('.product-card');
  const name = card.querySelector('h3').textContent;
  const price = Number(card.querySelector('.price').textContent.replace('$', ''));

  if (action === 'increase') {
    const existing = cart.get(productId) || { productId, name, price, quantity: 0 };
    existing.quantity += 1;
    cart.set(productId, existing);
    updateCartSummary();
    renderProductsFromExisting();
    return;
  }

  if (action === 'decrease') {
    const existing = cart.get(productId);
    if (!existing) return;
    existing.quantity = Math.max(0, existing.quantity - 1);
    if (existing.quantity === 0) {
      cart.delete(productId);
    } else {
      cart.set(productId, existing);
    }
    updateCartSummary();
    renderProductsFromExisting();
    return;
  }

  if (action === 'add') {
    addToCart(productId, name, price);
  }
});

checkoutForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  checkoutError.hidden = true;
  checkoutSuccess.hidden = true;

  if (!cart.size) {
    checkoutError.textContent = 'Add at least one product to the cart before checking out.';
    checkoutError.hidden = false;
    return;
  }

  const payload = {
    customer_id: document.querySelector('#customer_id').value.trim(),
    email: document.querySelector('#email').value.trim(),
    items: Array.from(cart.values()).map((item) => ({
      product_id: item.productId,
      quantity: item.quantity,
    })),
  };

  try {
    const response = await fetch('/api/orders/checkout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) {
      checkoutError.textContent = data.error?.message || 'Checkout failed';
      checkoutError.hidden = false;
      return;
    }

    checkoutSuccess.textContent = `Order ${data.order.id} confirmed. Email queued for ${data.order.email}.`;
    checkoutSuccess.hidden = false;
    cart.clear();
    updateCartSummary();
    fetchProducts();
    checkoutForm.reset();
  } catch (error) {
    checkoutError.textContent = 'The checkout API is currently unavailable.';
    checkoutError.hidden = false;
  }
});

fetchProducts();
updateCartSummary();
