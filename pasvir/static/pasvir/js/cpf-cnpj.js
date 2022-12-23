let codeLabel = document.getElementById('codeLabel');
let code = document.getElementById('code');
let codeLength = code.textContent.length;

// Check if is CPF or CNPJ
if (codeLength == 11) {
    codeLabel.innerHTML = 'CPF';
} else {
    codeLabel.innerHTML = 'CNPJ';
}

code.innerHTML = formatCnpjCpf(code.textContent);

// Correct format for CPF and CNPJ
function formatCnpjCpf(value) {
    const cnpjCpf = value.replace(/\D/g, '');

    if (cnpjCpf.length === 11) {
        return cnpjCpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/g, "\$1.\$2.\$3-\$4");
    }

    return cnpjCpf.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/g, "\$1.\$2.\$3/\$4-\$5");
}
