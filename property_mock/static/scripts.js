let currentSlide = 0;
const slides = document.querySelectorAll('.testimonial-slider .slide');

function showSlide(index) {
    slides.forEach((slide, i) => {
        slide.classList.remove('active');
        if (i === index) {
            slide.classList.add('active');
        }
    });
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
}

// Automatically move to the next slide every 3 seconds
setInterval(nextSlide, 3000);

// Show the first slide initially
showSlide(currentSlide);
