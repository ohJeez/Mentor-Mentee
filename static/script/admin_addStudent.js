
document.querySelectorAll('input[type="text"], input[type="email"], input[type="date"]').forEach(input => {
    input.addEventListener('focus', function() {
        this.setAttribute('placeholder', this.getAttribute('data-label') || '');
    });
    
    input.addEventListener('blur', function() {
        if (!this.value) {
            this.setAttribute('placeholder', '');
        }
    });
});

document.querySelector('.photo-upload-area').addEventListener('click', function() {
    document.querySelector('.photo-input').click();
});
