const loginModal = document.getElementById('loginModal');
const registerModal = document.getElementById('registerModal');

const openLoginBtn = document.getElementById('openLoginBtn');
const closeLoginBtn = document.getElementById('closeLoginBtn');

const openRegisterBtn = document.getElementById('openRegisterBtn');
const closeRegisterBtn = document.getElementById('closeRegisterBtn');

const openRegisterFromLogin = document.getElementById('openRegisterFromLogin');

if (openLoginBtn) {
    openLoginBtn.addEventListener('click', (e) => {
        e.preventDefault();
        loginModal.style.display = 'block';
    });
}

if (closeLoginBtn) {
    closeLoginBtn.addEventListener('click', () => {
        loginModal.style.display = 'none';
    });
}

if (openRegisterBtn) {
    openRegisterBtn.addEventListener('click', (e) => {
        e.preventDefault();
        registerModal.style.display = 'block';
    });
}

if (closeRegisterBtn) {
    closeRegisterBtn.addEventListener('click', () => {
        registerModal.style.display = 'none';
    });
}

if (openRegisterFromLogin) {
    openRegisterFromLogin.addEventListener('click', (e) => {
        e.preventDefault();
        loginModal.style.display = 'none';
        registerModal.style.display = 'block';
    });
}

window.addEventListener('click', (e) => {
    if (e.target === loginModal) {
        loginModal.style.display = 'none';
    } else if (e.target === registerModal) {
        registerModal.style.display = 'none';
    }
});

window.onload = function () {
    const messages = document.querySelectorAll('.mensagens li');

    if (messages.length > 0) {
            let modalParaAbrir = 'register';
             mensagens.forEach((msg) => {
            const tipo = msg.getAttribute('data-tag');
            if (tipo === 'error') {
                modalParaAbrir = 'login';
            } else if (tipo === 'success') {
                modalParaAbrir = 'register'; 
            }
        });

        if (modalParaAbrir === 'login') {
            if (loginModal) loginModal.style.display = 'block';
        } else if (modalParaAbrir === 'register') {
            if (registerModal) registerModal.style.display = 'block';
        }
    }
}
