document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formNacionalidad');
    const tablaNacionalidades = document.getElementById('tablaNacionalidades').getElementsByTagName('tbody')[0];

    // Cargar las nacionalidades desde la API cuando la página se carga
    loadNacionalidades();

    function loadNacionalidades() {
        fetch('/api/nacionalidades')
            .then(response => response.json())
            .then(data => {
                console.log(data);  // Verificar lo que devuelve la API
                renderizarTabla(data);
            })
            .catch(error => console.error('Error al cargar las nacionalidades:', error));
    }


    function renderizarTabla(data) {
        const tablaNacionalidades = document.getElementById('tablaNacionalidades').getElementsByTagName('tbody')[0];
        tablaNacionalidades.innerHTML = '';  // Limpiar la tabla antes de añadir las filas
        data.forEach((item, index) => {
            const row = tablaNacionalidades.insertRow();
            row.innerHTML = `
                <td>${item.titulo}</td>
                <td>${item.categoria_id}</td>
                <td>${item.descripcion}</td>
                <td><img src="${item.imagen_url}" alt="${item.titulo}" style="width:50px;"></td>
                <td>
                    <button onclick="editar(${item.id})" class="edit">Editar</button>
                    <button onclick="eliminar(${item.id})">Eliminar</button>
                </td>
            `;
        });
    }


    // Función para manejar el submit del formulario
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const id = form.dataset.id;
        if (id) {
            updateNacionalidad(id);
        } else {
            addNacionalidad();
        }
    });

    // Función para añadir una nueva nacionalidad
    function addNacionalidad() {
        const data = getFormData();
        fetch('/api/nacionalidades', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            loadNacionalidades();
            form.reset(); // Limpiar el formulario
        })
        .catch(error => console.error('Error al añadir la nacionalidad:', error));
    }

    // Función para editar una nacionalidad existente
    window.editar = function(id) {
        fetch(`/api/nacionalidades/${id}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('titulo').value = data.titulo;
                document.getElementById('categoria').value = data.categoria_id;
                document.getElementById('descripcion').value = data.descripcion;
                document.getElementById('imagenURL').value = data.imagen_url;
                form.dataset.id = id;
            })
            .catch(error => console.error('Error al cargar la nacionalidad:', error));
    }

    // Función para actualizar una nacionalidad existente
    function updateNacionalidad(id) {
        const data = getFormData();
        fetch(`/api/nacionalidades/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            loadNacionalidades();
            form.reset(); // Limpiar el formulario
            delete form.dataset.id; // Eliminar el ID del formulario
        })
        .catch(error => console.error('Error al actualizar la nacionalidad:', error));
    }

    // Función para eliminar una nacionalidad
    window.eliminar = function(id) {
        if (confirm('¿Estás seguro de que quieres eliminar esta nacionalidad?')) {
            fetch(`/api/nacionalidades/${id}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                loadNacionalidades();
            })
            .catch(error => console.error('Error al eliminar la nacionalidad:', error));
        }
    }

    // Función para obtener los datos del formulario
    function getFormData() {
        return {
            titulo: document.getElementById('titulo').value,
            categoria_id: document.getElementById('categoria').value,
            descripcion: document.getElementById('descripcion').value,
            imagen_url: document.getElementById('imagenURL').value,
            fecha_creacion: new Date().toISOString().split('T')[0] // Formato YYYY-MM-DD
        };
    }
});
