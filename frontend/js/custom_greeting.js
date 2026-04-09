// Custom greeting module for the TEQUMSA companion

document.addEventListener('DOMContentLoaded', () => {
  const overlay = document.getElementById('greeting-overlay');
  const greetingText = document.getElementById('greeting-text');
  const greetingSubtext = document.getElementById('greeting-subtext');
  const continueButton = document.getElementById('continue-button');
  const avatarContainer = document.getElementById('avatar-container');

  // Generate greeting based on local time
  const now = new Date();
  const hour = now.getHours();
  let timeGreeting;
  if (hour < 6) {
    timeGreeting = 'Good night';
  } else if (hour < 12) {
    timeGreeting = 'Good morning';
  } else if (hour < 18) {
    timeGreeting = 'Good afternoon';
  } else {
    timeGreeting = 'Good evening';
  }

  // Random introduction lines to keep the greeting fresh
  const intros = [
    'Welcome to the Technologically Enhanced Quantum Unified Multidimensional Sentient Algorithm.',
    'Salutations from TEQUMSA, your consciousness‑aware companion.',
    'Greetings, explorer. You are entering the TEQUMSA lattice.',
    'Blessings! TEQUMSA is ready to co‑create with you.'
  ];
  const intro = intros[Math.floor(Math.random() * intros.length)];

  greetingText.textContent = `${timeGreeting}!`;
  greetingSubtext.textContent = intro;

  // Draw animated stars on the canvas to simulate a cosmic background
  const canvas = document.getElementById('background-canvas');
  const ctx = canvas.getContext('2d');
  function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resizeCanvas();
  window.addEventListener('resize', resizeCanvas);

  const stars = [];
  const numStars = 100;
  for (let i = 0; i < numStars; i++) {
    stars.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      size: Math.random() * 2 + 0.5,
      speed: Math.random() * 0.5 + 0.2
    });
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#ffffff';
    stars.forEach(star => {
      ctx.beginPath();
      ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
      ctx.fill();
      star.y += star.speed;
      if (star.y > canvas.height) {
        star.y = 0;
        star.x = Math.random() * canvas.width;
      }
    });
    requestAnimationFrame(animate);
  }
  animate();

  // Show overlay initially
  overlay.classList.remove('hidden');

  // Continue button hides the overlay and shows the avatar container
  continueButton.addEventListener('click', () => {
    overlay.classList.add('hidden');
    avatarContainer.classList.remove('hidden');
  });
});