// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Typewriter effect for the hero section title
const heroTitle = document.querySelector('.hero h2');
const text = heroTitle.textContent;
heroTitle.textContent = '';

let index = 0;
function typeWriter() {
    if (index < text.length) {
        heroTitle.textContent += text.charAt(index);
        index++;
        setTimeout(typeWriter, 50); // Adjust speed here
    }
}

typeWriter();

// Pulsating effect for the hero section
const heroSection = document.querySelector('.hero');
setInterval(() => {
    heroSection.style.boxShadow = '0 0 20px rgba(255, 215, 0, 0.8)';
    setTimeout(() => {
        heroSection.style.boxShadow = '0 8px 15px rgba(0, 0, 0, 0.2)';
    }, 500);
}, 2000);

// Button hover effect with ripple
const button = document.querySelector('.button');
button.addEventListener('click', (e) => {
    const ripple = document.createElement('span');
    ripple.classList.add('ripple');
    button.appendChild(ripple);

    const rect = button.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    ripple.style.left = `${x}px`;
    ripple.style.top = `${y}px`;

    setTimeout(() => {
        ripple.remove();
    }, 500);
});

// Add glowing particles effect to the hero section
function createParticle() {
    const particle = document.createElement('div');
    particle.classList.add('particle');
    particle.style.left = `${Math.random() * 100}%`;
    particle.style.top = `${Math.random() * 100}%`;
    particle.style.animationDuration = `${Math.random() * 3 + 2}s`;
    document.querySelector('.hero').appendChild(particle);

    setTimeout(() => {
        particle.remove();
    }, 5000);
}

setInterval(createParticle, 200);

// Synchronize glowing outline animations
const header = document.querySelector('header');
const footer = document.querySelector('footer');
const hero = document.querySelector('.hero');

function synchronizeGlowingOutline() {
    header.style.animation = 'glowingOutline 3s infinite alternate';
    footer.style.animation = 'glowingOutline 3s infinite alternate';
    hero.style.animation = 'glowingOutline 3s infinite alternate';
}

// Start synchronized glowing outline
setTimeout(synchronizeGlowingOutline, 1000); // Delay to ensure smooth start