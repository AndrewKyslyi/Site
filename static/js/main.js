// Main JS for Scorpy Tale

document.addEventListener('DOMContentLoaded', function() {
    // Theme Toggle Functionality
    const themeToggle = document.getElementById('theme-toggle');
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    
    // Function to set theme
    const setTheme = (theme) => {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        
        // Update toggle icon
        if (themeToggle) {
            if (theme === 'dark') {
                themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
                themeToggle.setAttribute('title', 'Switch to Light Mode');
            } else {
                themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
                themeToggle.setAttribute('title', 'Switch to Dark Mode');
            }
        }
        
        // Force reflow for immediate theme application
        document.body.style.display = 'none';
        const _ = document.body.offsetHeight; // This causes a reflow
        document.body.style.display = '';
    };
    
    // Check for saved theme preference or use OS preference
    const currentTheme = localStorage.getItem('theme');
    
    if (currentTheme) {
        setTheme(currentTheme);
    } else if (prefersDarkScheme.matches) {
        setTheme('dark');
    } else {
        setTheme('light');
    }
    
    // Toggle theme when button is clicked
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const activeTheme = document.documentElement.getAttribute('data-theme') || 'light';
            const newTheme = activeTheme === 'light' ? 'dark' : 'light';
            
            // Force immediate reapplication of theme
            setTheme(newTheme);
            
            // Add a flash animation to indicate theme change
            themeToggle.classList.add('theme-changed');
            setTimeout(() => {
                themeToggle.classList.remove('theme-changed');
            }, 500);
        });
    }

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Quantity increment/decrement in cart
    const quantityInputs = document.querySelectorAll('.quantity-input');
    
    if (quantityInputs) {
        quantityInputs.forEach(input => {
            const minusBtn = input.previousElementSibling;
            const plusBtn = input.nextElementSibling;
            
            if (minusBtn && minusBtn.classList.contains('quantity-minus')) {
                minusBtn.addEventListener('click', function() {
                    if (input.value > 1) {
                        input.value = parseInt(input.value) - 1;
                        // Trigger change event if needed for other scripts
                        input.dispatchEvent(new Event('change'));
                    }
                });
            }
            
            if (plusBtn && plusBtn.classList.contains('quantity-plus')) {
                plusBtn.addEventListener('click', function() {
                    input.value = parseInt(input.value) + 1;
                    // Trigger change event if needed for other scripts
                    input.dispatchEvent(new Event('change'));
                });
            }
        });
    }

    // Add smooth scrolling to all links
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

    // Add image preview for file inputs
    const imageInput = document.querySelector('#id_image');
    const imagePreview = document.querySelector('#image-preview');
    
    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                    imagePreview.style.display = 'block';
                }
                
                reader.readAsDataURL(this.files[0]);
            }
        });
    }

    // Add fade-in animation for cards
    const fadeElements = document.querySelectorAll('.fade-in');
    
    if (fadeElements.length > 0) {
        const fadeInObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, { threshold: 0.1 });
        
        fadeElements.forEach(element => {
            fadeInObserver.observe(element);
        });
    }
}); 