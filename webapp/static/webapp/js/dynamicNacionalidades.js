document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('nacionalidades-container');

    // Datos falsos ampliados para visualizar más tarjetas
    let informacionNacionalidad = [
        { titulo: 'Cultura Andina', categoria: 'Cultura', descripcion: 'La rica herencia cultural de los Andes ecuatorianos.', imagenURL: 'https://lonelyplanetes.cdnstatics2.com/sites/default/files/styles/max_650x650/public/imprescindibles_images/Ecuador_PNYasuni_shutterstock_181756775_Fotos593_Shutterstock.jpg' },
        { titulo: 'Amazonía Indígena', categoria: 'Etnia', descripcion: 'Comunidades indígenas de la Amazonía ecuatoriana.', imagenURL: 'https://via.placeholder.com/150' },
        { titulo: 'Costa Pacífica', categoria: 'Geografía', descripcion: 'La diversidad geográfica y cultural de la costa pacífica de Ecuador.', imagenURL: 'https://via.placeholder.com/150' },
        { titulo: 'Sierra Central', categoria: 'Geografía', descripcion: 'Una región montañosa rica en biodiversidad y tradición.', imagenURL: 'https://via.placeholder.com/150' },
        { titulo: 'Pueblo Shuar', categoria: 'Etnia', descripcion: 'Una comunidad indígena conocida por su resistencia y cultura en la Amazonía.', imagenURL: 'https://via.placeholder.com/150' },
        { titulo: 'Galápagos', categoria: 'Geografía', descripcion: 'Las islas Galápagos, un santuario natural único en el mundo.', imagenURL: 'https://via.placeholder.com/150' },
        { titulo: 'Afroecuatorianos', categoria: 'Etnia', descripcion: 'Herencia cultural de los descendientes de africanos en la región costera.', imagenURL: 'https://via.placeholder.com/150' },
        { titulo: 'Pueblo Kichwa', categoria: 'Etnia', descripcion: 'El grupo indígena más grande de Ecuador, con una rica tradición cultural.', imagenURL: 'https://via.placeholder.com/150' },
        { titulo: 'Oriente Ecuatoriano', categoria: 'Geografía', descripcion: 'Una región de exuberante selva tropical al este del país.', imagenURL: 'https://via.placeholder.com/150' },
        { titulo: 'Cultura Tsáchila', categoria: 'Cultura', descripcion: 'Conocidos por sus tradiciones ancestrales y su distintiva vestimenta.', imagenURL: 'https://via.placeholder.com/150' }
    ];

    // Función para renderizar las tarjetas
    function renderizarTarjetas() {
        container.innerHTML = ''; // Limpiar el contenedor
        informacionNacionalidad.forEach(item => {
            const card = document.createElement('div');
            card.classList.add('card');
            card.innerHTML = `
                <img src="${item.imagenURL}" alt="${item.titulo}" class="card-img">
                <div class="card-content">
                    <h3>${item.titulo}</h3>
                    <p>${item.descripcion}</p>
                    <button class="card-button">Ver más</button>
                </div>
            `;
            container.appendChild(card);
        });
    }

    // Inicializar las tarjetas con los datos actuales
    renderizarTarjetas();
});
