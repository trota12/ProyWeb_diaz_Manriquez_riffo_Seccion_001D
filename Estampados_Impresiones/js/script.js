//API REST

// Función para obtener productos de la API
async function fetchProducts() {
    try {
        const response = await fetch('https://fakestoreapi.com/products');
        const data = await response.json();
        displayProducts(data);
    } catch (error) {
        console.error('Error al obtener los productos:', error);
    }
}

// Función para mostrar los productos en el HTML
function displayProducts(products) {
    const container = document.getElementById('productos');
    container.innerHTML = ''; // Limpiar el contenedor

    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'producto';

        productCard.innerHTML = `
            <img src="${product.image}" alt="${product.title}">
            <h3>${product.title}</h3>
            <p class="price">$${product.price}</p>
            <p><strong>Categoría:</strong> ${product.category}</p>
            <p>${product.description.slice(0, 100)}...</p>
        `;

        container.appendChild(productCard);
    });
}

// Llamar a la función cuando cargue la página
fetchProducts();




//VALIDACIONES