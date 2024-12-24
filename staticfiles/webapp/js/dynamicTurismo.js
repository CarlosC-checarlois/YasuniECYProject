document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('turismo-container');

    // Datos falsos para visualizar las tarjetas
    let informacionTuristica = [
        { titulo: 'Visita a la Laguna Encantada', categoria: 'Naturaleza', descripcion: 'Explora la Laguna Encantada y su biodiversidad única.', imagenURL: 'https://happygringo.com/wp-content/uploads/2021/08/yasuni-national-park-guide-1.jpg' },
        { titulo: 'Senderismo en la Selva', categoria: 'Aventura', descripcion: 'Recorre los senderos de la selva amazónica con un guía experimentado.', imagenURL: 'https://lonelyplanetes.cdnstatics2.com/sites/default/files/styles/max_650x650/public/imprescindibles_images/Ecuador_PNYasuni_shutterstock_181756775_Fotos593_Shutterstock.jpg' },
        { titulo: 'Tour Cultural Waorani', categoria: 'Cultura', descripcion: 'Conoce las tradiciones y costumbres de la comunidad Waorani.', imagenURL: 'https://www.viajaecuador.com.ec/wp-content/uploads/2020/12/AR-PN-AMAZONIA-ORELLANA-AVITURISMO-YASUNI-026.jpg' },
        { titulo: 'Exploración Nocturna', categoria: 'Aventura', descripcion: 'Descubre la selva amazónica bajo la luz de la luna.', imagenURL: 'https://example.com/imagen4.jpg' },
        { titulo: 'Observación de Aves', categoria: 'Naturaleza', descripcion: 'Identifica más de 500 especies de aves en su hábitat natural.', imagenURL: 'https://example.com/imagen5.jpg' },
        { titulo: 'Paseo en Canoa', categoria: 'Aventura', descripcion: 'Navega por los ríos de Yasuni y admira la belleza natural.', imagenURL: 'https://example.com/imagen6.jpg' }
    ];

    // Función para renderizar las tarjetas
    function renderizarTarjetas() {
        container.innerHTML = ''; // Limpiar el contenedor
        informacionTuristica.forEach(item => {
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
