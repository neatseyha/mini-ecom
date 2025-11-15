// Add to cart functionality
document.addEventListener("DOMContentLoaded", function () {
  // Add to cart buttons
  const addToCartButtons = document.querySelectorAll(".add-to-cart");
  addToCartButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const productId = parseInt(this.dataset.productId);
      addToCart(productId);
    });
  });

  // Quantity controls
  const increaseButtons = document.querySelectorAll(".qty-btn.increase");
  const decreaseButtons = document.querySelectorAll(".qty-btn.decrease");

  increaseButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const productId = parseInt(this.dataset.productId);
      const input = document.querySelector(
        `.quantity-input[data-product-id="${productId}"]`
      );
      const newQuantity = parseInt(input.value) + 1;
      updateCartQuantity(productId, newQuantity);
    });
  });

  decreaseButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const productId = parseInt(this.dataset.productId);
      const input = document.querySelector(
        `.quantity-input[data-product-id="${productId}"]`
      );
      const newQuantity = Math.max(1, parseInt(input.value) - 1);
      updateCartQuantity(productId, newQuantity);
    });
  });

  // Quantity input change
  const quantityInputs = document.querySelectorAll(".quantity-input");
  quantityInputs.forEach((input) => {
    input.addEventListener("change", function () {
      const productId = parseInt(this.dataset.productId);
      const newQuantity = Math.max(1, parseInt(this.value));
      this.value = newQuantity;
      updateCartQuantity(productId, newQuantity);
    });
  });

  // Remove from cart buttons
  const removeButtons = document.querySelectorAll(".remove-btn");
  removeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const productId = parseInt(this.dataset.productId);
      removeFromCart(productId);
    });
  });
});

function addToCart(productId) {
  fetch("/add-to-cart", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ product_id: productId }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Update cart count badge
        const cartCount = document.getElementById("cart-count");
        if (cartCount) {
          cartCount.textContent = data.cart_count;
        }

        // Show success message
        showNotification("Product added to cart!", "success");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      showNotification("Failed to add product to cart", "error");
    });
}

function updateCartQuantity(productId, quantity) {
  fetch("/update-cart", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      product_id: productId,
      quantity: quantity,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Reload page to update totals
        location.reload();
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      showNotification("Failed to update cart", "error");
    });
}

function removeFromCart(productId) {
  if (confirm("Are you sure you want to remove this item?")) {
    fetch("/remove-from-cart", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ product_id: productId }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          // Reload page
          location.reload();
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        showNotification("Failed to remove item", "error");
      });
  }
}

function showNotification(message, type) {
  const notification = document.createElement("div");
  notification.className = `notification notification-${type}`;
  notification.textContent = message;
  notification.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        padding: 15px 25px;
        background: ${type === "success" ? "#27ae60" : "#e74c3c"};
        color: white;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
    `;

  document.body.appendChild(notification);

  setTimeout(() => {
    notification.style.animation = "slideOut 0.3s ease-out";
    setTimeout(() => {
      notification.remove();
    }, 300);
  }, 3000);
}

// Add animation styles
const style = document.createElement("style");
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
