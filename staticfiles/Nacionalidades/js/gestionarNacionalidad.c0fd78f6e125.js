document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formNacionalidad');
    const tablaNacionalidades = document.getElementById('tablaNacionalidades').getElementsByTagName('tbody')[0];

    // Datos falsos para visualizar la tabla
    let informacionNacionalidad = [
        { titulo: 'Cultura Andina', categoria: 'Cultura', descripcion: 'La rica herencia cultural de los Andes ecuatorianos.', imagenURL: 'https://via.placeholder.com/150' },
        { titulo: 'Amazonía Indígena', categoria: 'Etnia', descripcion: 'Comunidades indígenas de la Amazonía ecuatoriana.', imagenURL: 'https://via.placeholder.com/150' },
        { titulo: 'Costa Pacífica', categoria: 'Geografía', descripcion: 'La diversidad geográfica y cultural de la costa pacífica de Ecuador.', imagenURL: 'https://via.placeholder.com/150' },
    ];

    // Función para renderizar la tabla
    function renderizarTabla() {
        tablaNacionalidades.innerHTML = ''; // Limpiar la tabla
        informacionNacionalidad.forEach((item, index) => {
            const row = tablaNacionalidades.insertRow();
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
        informacionNacionalidad.push(nuevaInformacion);
        renderizarTabla();
        form.reset(); // Limpiar el formulario
    });

    // Función para editar una entrada
    window.editar = function(index) {
        const item = informacionNacionalidad[index];
        document.getElementById('titulo').value = item.titulo;
        document.getElementById('categoria').value = item.categoria;
        document.getElementById('descripcion').value = item.descripcion;
        document.getElementById('imagenURL').value = item.imagenURL;
        
        informacionNacionalidad.splice(index, 1); // Eliminar temporalmente para actualizar
    }

    // Función para eliminar una entrada
    window.eliminar = function(index) {
        informacionNacionalidad.splice(index, 1);
        renderizarTabla();
    }

    // Inicializar la tabla con los datos actuales
    renderizarTabla();
});
