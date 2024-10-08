document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevenir el envío del formulario

    const username = document.getElementById('Usuario').value.trim();
    const password = document.getElementById('Contraseña').value.trim();

    // Validación de usuario y contraseña
    if (username === 'Usuario123' && password === '12345678') {
        alert('¡Bienvenido, ' + username + '!');

        // Redirigir utilizando la ruta Flask
        window.location.href = '/paginaActividades'; // Utiliza la ruta definida en Flask
    } else {
        document.getElementById('error').style.display = 'block'; // Mostrar mensaje de error
    }
});
