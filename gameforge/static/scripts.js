// GameForge - Scripts Frontend

// Auto-hide messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.messages .alert');
    
    messages.forEach(message => {
        setTimeout(() => {
            message.style.transition = 'opacity 0.5s, transform 0.5s';
            message.style.opacity = '0';
            message.style.transform = 'translateX(400px)';
            
            setTimeout(() => {
                message.remove();
            }, 500);
        }, 5000);
    });
});

// Form validation
function validateCreateForm() {
    const title = document.getElementById('title')?.value;
    const genre = document.getElementById('genre')?.value;
    
    if (!title || title.trim() === '') {
        alert('Veuillez entrer un titre pour votre jeu');
        return false;
    }
    
    if (!genre) {
        alert('Veuillez sélectionner un genre');
        return false;
    }
    
    return true;
}

// Smooth scroll to top
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Add smooth scrolling to all anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Confirmation for delete actions
document.querySelectorAll('a[href*="delete"]').forEach(link => {
    link.addEventListener('click', function(e) {
        if (!link.classList.contains('confirmed')) {
            e.preventDefault();
            if (confirm('Êtes-vous sûr de vouloir supprimer cet élément ?')) {
                link.classList.add('confirmed');
                link.click();
            }
        }
    });
});

console.log('🎮 GameForge - Frontend loaded successfully!');

