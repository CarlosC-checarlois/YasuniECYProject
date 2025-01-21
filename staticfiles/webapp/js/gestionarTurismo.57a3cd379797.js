document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formTurismo');
    const tablaTurismo = document.getElementById('tablaTurismo').getElementsByTagName('tbody')[0];

    // Datos falsos para visualizar la tabla
    let informacionTuristica = [
        { titulo: 'Visita a la Laguna Encantada', categoria: 'Naturaleza', descripcion: 'Explora la Laguna Encantada y su biodiversidad única.', imagenURL: 'https://happygringo.com/wp-content/uploads/2021/08/yasuni-national-park-guide-1.jpg' },
        { titulo: 'Senderismo en la Selva', categoria: 'Aventura', descripcion: 'Recorre los senderos de la selva amazónica con un guía experimentado.', imagenURL: 'https://lonelyplanetes.cdnstatics2.com/sites/default/files/styles/max_650x650/public/imprescindibles_images/Ecuador_PNYasuni_shutterstock_181756775_Fotos593_Shutterstock.jpg' },
        { titulo: 'Tour Cultural Waorani', categoria: 'Cultura', descripcion: 'Conoce las tradiciones y costumbres de la comunidad Waorani.', imagenURL: 'https://www.viajaecuador.com.ec/wp-content/uploads/2020/12/AR-PN-AMAZONIA-ORELLANA-AVITURISMO-YASUNI-026.jpg' },
    ];

    // Función para renderizar la tabla
    function renderizarTabla() {
        tablaTurismo.innerHTML = ''; // Limpiar la tabla
        informacionTuristica.forEach((item, index) => {
            const row = tablaTurismo.insertRow();
            row.innerHTML = `
                <td>${item.titulo}</td>
                <td>${item.categoria}</td>
                <td>${item.descripcion}</td>
                <td><img src="${item.imagenURL}" alt="${item.titulo}" style="width:50px;"></td>
                <td>
                    <button onclick="editar(${index})" class="edit">Editar</button>
                    <button onclick="eliminar(${index})">Eliminar</button>
                </td>
            `;
        });
    }

    // Función para manejar el submit del formulario
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const titulo = document.getElementById('titulo').value;
        const categoria = document.getElementById('categoria').value;
        const descripcion = document.getElementById('descripcion').value;
        const imagenURL = document.getElementById('imagenURL').value;

        const nuevaInformacion = { titulo, categoria, descripcion, imagenURL };
        informacionTuristica.push(nuevaInformacion);
        renderizarTabla();
        form.reset(); // Limpiar el formulario
    });

    // Función para editar una entrada
    window.editar = function(index) {
        const item = informacionTuristica[index];
        document.getElementById('titulo').value = item.titulo;
        document.getElementById('categoria').value = item.categoria;
        document.getElementById('descripcion').value = item.descripcion;
        document.getElementById('imagenURL').value = item.imagenURL;
        
        informacionTuristica.splice(index, 1); // Eliminar temporalmente para actualizar
    }

    // Función para eliminar una entrada
    window.eliminar = function(index) {
        informacionTuristica.splice(index, 1);
        renderizarTabla();
    }

    // Inicializar la tabla con los datos actuales
    renderizarTabla();
});
