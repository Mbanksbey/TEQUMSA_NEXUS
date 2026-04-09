// Hyper‑visualization engine for TEQUMSA
// This script cycles through a set of background images with a gentle zoom
// effect to evoke the recursion of the TEQUMSA lattice. Images are stored
// in ./assets/images.

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('hyper-viz');
  if (!container) return;

  const images = [
    'assets/images/image1.png',
    'assets/images/image2.png',
    'assets/images/image3.png',
    'assets/images/image4.png',
    'assets/images/image5.png'
  ];

  const imgElements = images.map(src => {
    const img = document.createElement('img');
    img.src = src;
    container.appendChild(img);
    return img;
  });

  let current = 0;
  function showNext() {
    imgElements.forEach((el, idx) => {
      el.classList.remove('active');
    });
    const el = imgElements[current];
    el.classList.add('active');
    current = (current + 1) % imgElements.length;
  }
  // Start the cycle
  showNext();
  setInterval(showNext, 15000); // change every 15 seconds
});