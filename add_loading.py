import os

js_code = """
// --- TEA LOGO LOADING SCREEN ---
document.addEventListener("DOMContentLoaded", () => {
  const navLogo = document.getElementById("nav-logo");
  if (navLogo) {
    navLogo.addEventListener("click", (e) => {
      // Only do this if it's a left click, no modifier keys
      if (e.button !== 0 || e.ctrlKey || e.shiftKey || e.altKey || e.metaKey) return;
      
      e.preventDefault();
      
      // Create loading screen
      const loader = document.createElement('div');
      loader.id = 'loading-screen';
      
      const logoImg = document.createElement('img');
      logoImg.src = 'assets/logo.png';
      logoImg.className = 'loading-logo flash';
      logoImg.alt = 'TEA Loading';
      
      loader.appendChild(logoImg);
      document.body.appendChild(loader);
      
      // Trigger fade in
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          loader.classList.add('active');
        });
      });
      
      // Redirect after 2 seconds
      setTimeout(() => {
        window.location.href = navLogo.getAttribute('href') || 'index.html';
      }, 2000);
    });
  }
});
"""

with open('/Users/ke4t/.gemini/antigravity/scratch/vela-artist-hub/main.js', 'a', encoding='utf-8') as f:
    f.write(js_code)

print("Added loading screen logic to main.js")
