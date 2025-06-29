const editButton = document.getElementById('edit-button');
const cancelButton = document.getElementById('cancel-button');
const form = document.getElementById('profile-form');
const container = document.getElementById('profile-container');
const logoutButton = document.querySelector('.logout-btn');
const deleteButton = document.querySelector('.delete-btn');

editButton.addEventListener('click', () => {
    container.classList.add('is-editing');

    const formGroups = form.querySelectorAll('.form-group');
    formGroups.forEach(group => {
        const span = group.querySelector('.display-value');
        const input = group.querySelector('.edit-input');
        if (span && input) {
            if (input.type === 'date') {
                const [dia, mes, ano] = span.textContent.split('/');
                input.value = `${ano}-${mes.padStart(2, '0')}-${dia.padStart(2, '0')}`;
            } else {
                input.value = span.textContent;
            }
        }
    });

    document.getElementById('senha').value = '';
    document.getElementById('confirmar-senha').value = '';
});

cancelButton.addEventListener('click', () => {
    container.classList.remove('is-editing');
    form.reset();
});

form.addEventListener('submit', (e) => {
    const senha = document.getElementById('senha').value;
    const confirmarSenha = document.getElementById('confirmar-senha').value;

    if (senha && senha !== confirmarSenha) {
        e.preventDefault();
        alert('As senhas não conferem!');
        return;
    }   
});

//máscara para o CPF
document.addEventListener('DOMContentLoaded', function () {
    const cpfInput = document.getElementById('cpf');

    cpfInput.addEventListener('input', function () {
        let value = cpfInput.value.replace(/\D/g, '');

        if (value.length > 11) value = value.slice(0, 11);

        value = value.replace(/(\d{3})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');

        cpfInput.value = value;
    });
});

document.getElementById('logout-form').addEventListener('submit', function (e) {
    if (!confirm('Deseja realmente fazer logout?')) {
        e.preventDefault();
    }
});

document.getElementById('delete-form').addEventListener('submit', function (e) {
    if (!confirm('Tem certeza que deseja excluir sua conta? Esta ação não poderá ser desfeita.')) {
        e.preventDefault();
    }
});