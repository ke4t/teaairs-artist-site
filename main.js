/* ==========================================================================
   Tea INTERACTIVE JAVASCRIPT SYSTEM
   Features: Custom Cursor, Live Audio Synthesizer, Dynamic Video Visuals,
             Ticket Booking System, Lightbox, Dynamic Sticky Nav, Contact Form
   ========================================================================== */

// --- STATE MANAGEMENT ---
let isPlaying = false;
let currentTrackIndex = 0;
let trackProgressSeconds = 0;
let trackInterval = null;
let volume = 0.8; // Default volume (0.0 to 1.0)

// Web Audio API Synth variables
let audioCtx = null;
let masterGain = null;
let synthTimer = null;
let nextNoteTime = 0.0;
let stepIndex = 0;
let bpm = 110;

// Track Metadata
const trackList = [
  { id: "heartbreak_kid", title: "Heartbreak Kid", durationStr: "0:00", src: encodeURI("assets/HEARTBREAK_KID.mp3") }
];

// Photo Gallery Metadata
const photosList = [
  { src: "assets/photo_stairs.jpg", caption: "Tea — Outdoor Stairs Editorial" },
  { src: "assets/photo_bushes.jpg", caption: "Tea — Garden Style Outfit" },
  { src: "assets/photo_elevator.jpg", caption: "Tea — Elevator Mirror Selfie" }
];

// Video Ambient Canvas animation variables
let videoCanvasId = null;
let videoCanvasAnimFrame = null;

// --- DYNAMIC NAV SCROLL ---
const mainHeader = document.getElementById("main-header");
window.addEventListener("scroll", () => {
  if (window.scrollY > 50) {
    mainHeader.classList.add("scrolled");
  } else {
    mainHeader.classList.remove("scrolled");
  }
});

// Update nav links active class based on current page
document.addEventListener("DOMContentLoaded", () => {
  const navLinks = document.querySelectorAll(".nav-link");
  const currentPath = window.location.pathname.split("/").pop() || "index.html";
  
  navLinks.forEach(link => {
    link.classList.remove("active");
    if (link.getAttribute("href") === currentPath) {
      link.classList.add("active");
    }
  });
});

// --- MOBILE NAVIGATION ---
const mobileNavToggle = document.getElementById("mobile-nav-toggle");
const mobileDropdown = document.getElementById("mobile-dropdown");
const mobileNavLinks = document.querySelectorAll(".mobile-nav-link");

if (mobileNavToggle && mobileDropdown) {
  mobileNavToggle.addEventListener("click", () => {
    mobileNavToggle.classList.toggle("active");
    mobileDropdown.classList.toggle("active");
  });

  mobileNavLinks.forEach(link => {
    link.addEventListener("click", () => {
      mobileNavToggle.classList.remove("active");
      mobileDropdown.classList.remove("active");
    });
  });
}

// --- CUSTOM INTERTIAL CURSOR ---
const cursorRing = document.getElementById("custom-cursor");
const cursorDot = document.getElementById("custom-cursor-dot");

let mouseX = 0, mouseY = 0;
let ringX = 0, ringY = 0;

window.addEventListener("mousemove", (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;
  // Instantly move the dot
  if (cursorDot) {
    cursorDot.style.left = mouseX + "px";
    cursorDot.style.top = mouseY + "px";
  }
});

// Animate the ring with spring delay (lerp)
function updateCursor() {
  const lerpFactor = 0.15;
  ringX += (mouseX - ringX) * lerpFactor;
  ringY += (mouseY - ringY) * lerpFactor;
  
  if (cursorRing) {
    cursorRing.style.left = ringX + "px";
    cursorRing.style.top = ringY + "px";
  }
  requestAnimationFrame(updateCursor);
}
requestAnimationFrame(updateCursor);

// Cursor hover scaling on links/interactive elements
const interactiveSelectors = "a, button, input, select, textarea, .photo-card, .video-thumbnail-wrapper, .track-item, .qty-btn";
document.addEventListener("mouseover", (e) => {
  if (e.target.closest(interactiveSelectors) && cursorRing) {
    cursorRing.classList.add("hovered");
  }
});
document.addEventListener("mouseout", (e) => {
  if (e.target.closest(interactiveSelectors) && cursorRing) {
    cursorRing.classList.remove("hovered");
  }
});


// --- AUDIO PLAYER & ENGINE ---
const playBtn = document.getElementById("player-play-btn");
const prevBtn = document.getElementById("player-prev-btn");
const nextBtn = document.getElementById("player-next-btn");
const trackTitle = document.getElementById("player-track-title");
const currentTimeLabel = document.getElementById("player-current-time");
const totalDurationLabel = document.getElementById("player-total-duration");
const timelineSlider = document.getElementById("player-timeline-slider");
const timelineProgress = document.getElementById("player-timeline-progress");
const timelineHandle = document.getElementById("player-timeline-handle");
const volumeSlider = document.getElementById("player-volume-slider");
const volumeProgress = document.getElementById("player-volume-progress");
const volumeHandle = document.getElementById("player-volume-handle");

let globalAudio = new Audio("assets/HEARTBREAK_KID.mp3");
globalAudio.volume = 0.8;

if (playBtn) {
  playBtn.addEventListener("click", () => {
    if (globalAudio.paused) {
      globalAudio.play().then(() => {
        playBtn.innerHTML = '<i class="fas fa-pause"></i>';
        startWaveform();
      }).catch(e => console.error("Audio play failed:", e));
    } else {
      globalAudio.pause();
      playBtn.innerHTML = '<i class="fas fa-play"></i>';
      stopWaveform();
    }
  });
}

globalAudio.addEventListener('timeupdate', () => {
  if (isDraggingTimeline) return; // Don't update UI if dragging
  const current = globalAudio.currentTime;
  const duration = globalAudio.duration || 0;
  
  const currentMins = Math.floor(current / 60);
  const currentSecs = Math.floor(current % 60).toString().padStart(2, '0');
  if (currentTimeLabel) currentTimeLabel.textContent = `${currentMins}:${currentSecs}`;
  
  if (duration > 0) {
    const durMins = Math.floor(duration / 60);
    const durSecs = Math.floor(duration % 60).toString().padStart(2, '0');
    if (totalDurationLabel) totalDurationLabel.textContent = `${durMins}:${durSecs}`;
    
    const durLabelHTML = document.getElementById("vibe-lit-dur");
    if (durLabelHTML) durLabelHTML.textContent = `${durMins}:${durSecs}`;

    const percent = (current / duration) * 100;
    if (timelineProgress) timelineProgress.style.width = `${percent}%`;
    if (timelineHandle) timelineHandle.style.left = `${percent}%`;
  }
});

globalAudio.addEventListener('ended', () => {
  globalAudio.currentTime = 0;
  globalAudio.pause();
  if (playBtn) playBtn.innerHTML = '<i class="fas fa-play"></i>';
  stopWaveform();
});

// Timeline Drag Logic
let isDraggingTimeline = false;

function updateTimelineFromEvent(e) {
  if (!timelineSlider || !globalAudio.duration) return;
  const rect = timelineSlider.getBoundingClientRect();
  let percent = (e.clientX - rect.left) / rect.width;
  percent = Math.max(0, Math.min(1, percent));
  
  if (timelineProgress) timelineProgress.style.width = `${percent * 100}%`;
  if (timelineHandle) timelineHandle.style.left = `${percent * 100}%`;
  
  return percent * globalAudio.duration;
}

if (timelineSlider) {
  timelineSlider.addEventListener("mousedown", (e) => {
    isDraggingTimeline = true;
    updateTimelineFromEvent(e);
  });
  window.addEventListener("mousemove", (e) => {
    if (isDraggingTimeline) updateTimelineFromEvent(e);
  });
  window.addEventListener("mouseup", (e) => {
    if (isDraggingTimeline) {
      isDraggingTimeline = false;
      globalAudio.currentTime = updateTimelineFromEvent(e);
    }
  });
}

// Volume Drag Logic
let isDraggingVolume = false;

function updateVolumeFromEvent(e) {
  if (!volumeSlider) return;
  const rect = volumeSlider.getBoundingClientRect();
  let percent = (e.clientX - rect.left) / rect.width;
  percent = Math.max(0, Math.min(1, percent));
  
  globalAudio.volume = percent;
  if (volumeProgress) volumeProgress.style.width = `${percent * 100}%`;
  if (volumeHandle) volumeHandle.style.left = `${percent * 100}%`;
  
  const volIcon = document.getElementById("volume-icon");
  if (volIcon) {
    if (percent === 0) volIcon.className = "fas fa-volume-mute";
    else if (percent < 0.5) volIcon.className = "fas fa-volume-down";
    else volIcon.className = "fas fa-volume-up";
  }
}

if (volumeSlider) {
  volumeSlider.addEventListener("mousedown", (e) => {
    isDraggingVolume = true;
    updateVolumeFromEvent(e);
  });
  window.addEventListener("mousemove", (e) => {
    if (isDraggingVolume) updateVolumeFromEvent(e);
  });
  window.addEventListener("mouseup", (e) => {
    if (isDraggingVolume) {
      isDraggingVolume = false;
      updateVolumeFromEvent(e);
    }
  });
}

// Waveform visualizer fake animation
let waveTimer;
function startWaveform() {
  const bars = document.querySelectorAll(".wave-bar");
  if (!bars.length) return;
  
  clearInterval(waveTimer);
  waveTimer = setInterval(() => {
    bars.forEach(bar => {
      bar.style.height = `${Math.random() * 100}%`;
    });
  }, 100);
}

function stopWaveform() {
  clearInterval(waveTimer);
  const bars = document.querySelectorAll(".wave-bar");
  bars.forEach(bar => {
    bar.style.height = '10%';
  });
}

// --- PHOTO LIGHTBOX GALLERY ---

const lightbox = document.getElementById("lightbox-modal");
const lightboxImg = document.getElementById("lightbox-img");
const lightboxCaption = document.getElementById("lightbox-caption");
const lightboxClose = document.getElementById("lightbox-close");
const lightboxPrev = document.getElementById("lightbox-prev");
const lightboxNext = document.getElementById("lightbox-next");
const photoCards = document.querySelectorAll(".photo-card");
let activePhotoIndex = 0;

function openLightbox(index) {
  activePhotoIndex = index;
  const photo = photosList[activePhotoIndex];
  
  if (lightboxImg && lightboxCaption && lightbox) {
    lightboxImg.src = photo.src;
    lightboxImg.alt = photo.caption;
    lightboxCaption.innerText = photo.caption;
    
    lightbox.style.display = "flex";
    setTimeout(() => {
      lightbox.classList.add("active");
    }, 10);
  }
}

function closeLightbox() {
  if (lightbox) {
    lightbox.classList.remove("active");
    setTimeout(() => {
      lightbox.style.display = "none";
    }, 400);
  }
}

function prevLightbox() {
  let prevIdx = activePhotoIndex - 1;
  if (prevIdx < 0) prevIdx = photosList.length - 1;
  openLightbox(prevIdx);
}

function nextLightbox() {
  let nextIdx = activePhotoIndex + 1;
  if (nextIdx >= photosList.length) nextIdx = 0;
  openLightbox(nextIdx);
}

photoCards.forEach((card, idx) => {
  card.addEventListener("click", () => {
    openLightbox(idx);
  });
});

if (lightboxClose) lightboxClose.addEventListener("click", closeLightbox);
if (lightboxPrev) lightboxPrev.addEventListener("click", prevLightbox);
if (lightboxNext) lightboxNext.addEventListener("click", nextLightbox);

// Close lightbox on clicking outside background
if (lightbox) {
  if (lightbox) lightbox.addEventListener("click", (e) => {
    if (e.target === lightbox) {
      closeLightbox();
    }
  });
}

// --- VIDEO PLAYER MODAL & AMBIENT CANVAS ---

const videoModal = document.getElementById("video-modal");
const videoClose = document.getElementById("video-close");
const videoThumbnails = document.querySelectorAll(".video-thumbnail-wrapper");
const videoContainer = document.getElementById("video-player-container");

function openVideoModal(videoId, videoType) {
  if (!videoModal || !videoContainer) return;
  videoCanvasId = videoId;
  
  videoModal.style.display = "flex";
  setTimeout(() => {
    videoModal.classList.add("active");
  }, 10);
  
  if (videoType === 'youtube') {
    videoContainer.innerHTML = `<iframe width="100%" height="100%" src="https://www.youtube.com/embed/${videoId}?autoplay=1" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="border-radius: 12px; box-shadow: 0 10px 40px var(--secondary-glow);"></iframe>`;
    
    // Pause synth music if playing when playing actual video
    if (isPlaying) {
      playTrack(); // This pauses it because it toggles
    }
  } else {
    // Inject visual canvas
    videoContainer.innerHTML = '<canvas id="ambient-video-canvas" style="width:100%; height:100%; display:block;"></canvas>';
    
    // Trigger synth music play if it isn't playing
    if (!isPlaying) {
      playTrack();
    }
    
    setupAmbientVisuals();
  }
}

function closeVideoModal() {
  if (!videoModal) return;
  videoModal.classList.remove("active");
  
  // Cancel canvas animation
  if (videoCanvasAnimFrame) {
    cancelAnimationFrame(videoCanvasAnimFrame);
    videoCanvasAnimFrame = null;
  }
  
  setTimeout(() => {
    videoModal.style.display = "none";
    if (videoContainer) videoContainer.innerHTML = "";
  }, 400);
}

// Procedural visualizer drawing on canvas
function setupAmbientVisuals() {
  const canvas = document.getElementById("ambient-video-canvas");
  if (!canvas) return;
  
  const ctx = canvas.getContext("2d");
  
  // Adjust sizing
  function resizeCanvas() {
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;
  }
  resizeCanvas();
  window.addEventListener("resize", resizeCanvas);
  
  let particleArray = [];
  const particleCount = 60;
  
  class VisualParticle {
    constructor() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.size = Math.random() * 5 + 2;
      this.speedX = Math.random() * 1.5 - 0.75;
      this.speedY = Math.random() * 1.5 - 0.75;
      this.hue = Math.random() > 0.5 ? 280 : 320; // Purple / Pink
      this.alpha = Math.random() * 0.5 + 0.3;
    }
    
    update() {
      this.x += this.speedX;
      this.y += this.speedY;
      
      if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
      if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
    }
    
    draw() {
      ctx.save();
      ctx.shadowBlur = 15;
      ctx.shadowColor = `hsla(${this.hue}, 100%, 65%, ${this.alpha})`;
      ctx.fillStyle = `hsla(${this.hue}, 100%, 75%, ${this.alpha})`;
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  }
  
  for (let i = 0; i < particleCount; i++) {
    particleArray.push(new VisualParticle());
  }
  
  let frameCount = 0;
  
  function drawVisualizer() {
    frameCount++;
    
    // Clear and background
    ctx.fillStyle = "rgba(6, 2, 15, 0.08)"; // Trails effect
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Center glowing circle pulsing
    const centerGlow = ctx.createRadialGradient(
      canvas.width/2, canvas.height/2, 20, 
      canvas.width/2, canvas.height/2, canvas.height * 0.4
    );
    
    // Change speed and pulse based on track BPM
    const pulseSpeed = (bpm / 60) * 0.05;
    const pulseFactor = Math.sin(frameCount * pulseSpeed) * 15 + 80;
    
    centerGlow.addColorStop(0, `rgba(139, 92, 246, ${0.15 + Math.sin(frameCount*0.03)*0.05})`);
    centerGlow.addColorStop(0.5, `rgba(236, 72, 153, 0.03)`);
    centerGlow.addColorStop(1, "transparent");
    
    ctx.fillStyle = centerGlow;
    ctx.fillRect(0,0, canvas.width, canvas.height);
    
    // Draw concentric ring lines
    ctx.strokeStyle = "rgba(139, 92, 246, 0.08)";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.arc(canvas.width/2, canvas.height/2, pulseFactor * 1.5, 0, Math.PI * 2);
    ctx.stroke();
    
    ctx.strokeStyle = "rgba(236, 72, 153, 0.05)";
    ctx.beginPath();
    ctx.arc(canvas.width/2, canvas.height/2, pulseFactor * 2.5, 0, Math.PI * 2);
    ctx.stroke();
    
    // Draw particles
    particleArray.forEach(p => {
      p.update();
      p.draw();
    });
    
    // Waveform grid line overlay (representing the synth wave)
    ctx.strokeStyle = "rgba(236, 72, 153, 0.15)";
    ctx.lineWidth = 2;
    ctx.shadowBlur = 10;
    ctx.shadowColor = "rgba(236, 72, 153, 0.5)";
    ctx.beginPath();
    
    const sliceWidth = canvas.width / 120;
    let x = 0;
    
    for (let i = 0; i < 120; i++) {
      // Synth wave drawing
      const waveFreq = (frameCount * 0.08) + (i * 0.1);
      const amplitude = isPlaying ? (Math.sin(waveFreq) * Math.cos(waveFreq * 0.5) * 45) : 5;
      
      const y = (canvas.height / 2) + amplitude;
      if (i === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
      x += sliceWidth;
    }
    ctx.stroke();
    ctx.shadowBlur = 0; // reset shadow
    
    // Overlay text titles
    ctx.font = "bold 24px 'Outfit', sans-serif";
    ctx.fillStyle = "white";
    ctx.textAlign = "center";
    ctx.fillText("Tea // LIVE AMBIENT FEED", canvas.width/2, 50);
    
    ctx.font = "14px 'Plus Jakarta Sans', sans-serif";
    ctx.fillStyle = "var(--primary-bright)";
    ctx.fillText(`SYNCHRONIZED DECK: ${trackList[currentTrackIndex].title} • ${bpm} BPM`, canvas.width/2, canvas.height - 40);
    
    videoCanvasAnimFrame = requestAnimationFrame(drawVisualizer);
  }
  
  drawVisualizer();
}

videoThumbnails.forEach(thumb => {
  thumb.addEventListener("click", () => {
    const vidId = thumb.getAttribute("data-video-id");
    const vidType = thumb.getAttribute("data-video-type");
    openVideoModal(vidId, vidType);
  });
});

if (videoClose) videoClose.addEventListener("click", closeVideoModal);

if (videoModal) {
  if (videoModal) videoModal.addEventListener("click", (e) => {
    if (e.target === videoModal) {
      closeVideoModal();
    }
  });
}

// --- TOUR DATE TICKET BOOKING SYSTEM ---

const ticketModal = document.getElementById("ticket-modal");
const ticketClose = document.getElementById("ticket-close");
const ticketShowDetails = document.getElementById("ticket-show-details");
const qtyVal = document.getElementById("qty-val");
const qtyPlus = document.getElementById("qty-plus");
const qtyMinus = document.getElementById("qty-minus");
const ticketTotalPrice = document.getElementById("ticket-total-price");
const btnCheckout = document.getElementById("btn-ticket-checkout");
const tourItems = document.querySelectorAll(".tour-item");

const TICKET_PRICE = 45.00;
let currentQuantity = 1;
let selectedVenue = "";
let selectedLocation = "";

function openTicketModal(venue, location) {
  if (!ticketModal) return;
  selectedVenue = venue;
  selectedLocation = location;
  currentQuantity = 1;
  
  if (ticketShowDetails) {
    ticketShowDetails.innerHTML = `<strong>${selectedVenue}</strong><br>${selectedLocation}`;
  }
  updateTicketPrice();
  
  ticketModal.style.display = "flex";
  setTimeout(() => {
    ticketModal.classList.add("active");
  }, 10);
}

function closeTicketModal() {
  if (ticketModal) {
    ticketModal.classList.remove("active");
    setTimeout(() => {
      ticketModal.style.display = "none";
    }, 300);
  }
}

function updateTicketPrice() {
  if (qtyVal && ticketTotalPrice) {
    qtyVal.innerText = currentQuantity;
    const total = currentQuantity * TICKET_PRICE;
    ticketTotalPrice.innerText = `$${total.toFixed(2)}`;
  }
}

if (qtyPlus) {
  qtyPlus.addEventListener("click", () => {
    if (currentQuantity < 8) { // Max 8 tickets
      currentQuantity++;
      updateTicketPrice();
    }
  });
}

if (qtyMinus) {
  qtyMinus.addEventListener("click", () => {
    if (currentQuantity > 1) {
      currentQuantity--;
      updateTicketPrice();
    }
  });
}

// Wire up booking buttons
tourItems.forEach(item => {
  const btn = item.querySelector(".btn-tour:not(:disabled)");
  if (btn) {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      const venue = item.querySelector(".tour-venue").innerText;
      const location = item.querySelector(".tour-location").innerText;
      openTicketModal(venue, location);
    });
  }
});

if (ticketClose) ticketClose.addEventListener("click", closeTicketModal);

if (ticketModal) {
  if (ticketModal) ticketModal.addEventListener("click", (e) => {
    if (e.target === ticketModal) {
      closeTicketModal();
    }
  });
}

// Stripe mock checkout flow
if (btnCheckout) {
  btnCheckout.addEventListener("click", () => {
    btnCheckout.innerText = "Connecting to Stripe...";
    btnCheckout.disabled = true;
    
    // Quick noise for button checkout click
    if (isPlaying && audioCtx) {
      playLeadPluck(880, 0.3, audioCtx.currentTime, 0.2);
    }
    
    setTimeout(() => {
      btnCheckout.innerText = "Payment Successful!";
      btnCheckout.style.background = "#10b981"; // green
      btnCheckout.style.borderColor = "#10b981";
      
      // Show custom toast message
      const toast = document.getElementById("success-toast");
      if (toast) {
        const title = toast.querySelector("h4");
        const desc = toast.querySelector("p");
        title.innerText = "Tickets Confirmed!";
        desc.innerText = `Successfully purchased ${currentQuantity} ticket(s) for ${selectedVenue}.`;
        toast.className = "toast active";
        
        setTimeout(() => {
          toast.className = "toast";
        }, 2000);
      }
      
      setTimeout(() => {
        closeTicketModal();
        // Reset checkout button
        btnCheckout.innerText = "Checkout with Stripe";
        btnCheckout.disabled = false;
        btnCheckout.style.background = "";
        btnCheckout.style.borderColor = "";
      }, 1500);
    }, 1500);
  });
}

// --- CONTACT FORM SUBMISSION MOCKUP ---

const contactForm = document.getElementById("contact-form");
const contactSubmitBtn = document.getElementById("contact-submit-btn");

if (contactForm && contactSubmitBtn) {
  if (contactForm) contactForm.addEventListener("submit", (e) => {
    e.preventDefault();
    
    contactSubmitBtn.innerText = "Sending Message...";
    contactSubmitBtn.disabled = true;
    
    // Play confirm pluck
    if (isPlaying && audioCtx) {
      playLeadPluck(523.25, 0.25, audioCtx.currentTime, 0.25); // C5 pluck
    }
    
    setTimeout(() => {
      contactForm.reset();
      contactSubmitBtn.innerText = "Send Message";
      contactSubmitBtn.disabled = false;
      
      // Toast message
      const toast = document.getElementById("success-toast");
      if (toast) {
        const title = toast.querySelector("h4");
        const desc = toast.querySelector("p");
        title.innerText = "Message Sent Successfully";
        desc.innerText = "Thank you. We will get back to you shortly.";
        toast.className = "toast active";
        
        setTimeout(() => {
          toast.className = "toast";
        }, 2000);
      }
    }, 1200);
  });
}

// Keyboard shortcuts (Escape key closes modals)
window.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    closeLightbox();
    closeVideoModal();
    closeTicketModal();
  }
});

// Load the first track by default on page start
window.addEventListener("DOMContentLoaded", () => {
  loadTrack(0);
});

// --- TEA LOGO CLICK SCREEN ---

document.addEventListener("DOMContentLoaded", () => {
  const navLogo = document.getElementById("nav-logo");
  if (navLogo) {
    navLogo.addEventListener("click", (e) => {
      // Only do this if it's a left click, no modifier keys
      if (e.button !== 0 || e.ctrlKey || e.shiftKey || e.altKey || e.metaKey) return;
      
      e.preventDefault();
      
      const loader = document.getElementById("site-loader");
      if (loader) {
        loader.classList.add("active");
        
        // Redirect after 1 second
        setTimeout(() => {
          window.location.href = navLogo.getAttribute("href") || "index.html";
        }, 1000);
      } else {
        window.location.href = navLogo.getAttribute("href") || "index.html";
      }
    });
  }
});

// --- EMAIL POPUP MODAL ---
document.addEventListener("DOMContentLoaded", () => {
  const emailModal = document.getElementById("email-modal");
  const emailCloseBtn = document.getElementById("email-close-btn");
  const emailForm = document.getElementById("email-form");

  if (emailModal && emailCloseBtn && emailForm) {
    // Check if user has already seen or closed it
    let hasSeenPopup = false;
    try {
      hasSeenPopup = sessionStorage.getItem("tea_email_session_seen");
    } catch (e) {
      console.warn("Storage not available");
    }

    if (!hasSeenPopup) {
      setTimeout(() => {
        emailModal.classList.add("active");
        try {
          sessionStorage.setItem("tea_email_session_seen", "true");
        } catch (e) {}
      }, 2000);
    }

    const closePopup = () => {
      emailModal.classList.remove("active");
      try {
        sessionStorage.setItem("tea_email_session_seen", "true");
      } catch (e) {}
    };

    emailCloseBtn.addEventListener("click", closePopup);

    emailModal.addEventListener("click", (e) => {
      if (e.target === emailModal) {
        closePopup();
      }
    });

    emailForm.addEventListener("submit", (e) => {
      e.preventDefault();
      // Normally you would send the data to a server here.
      // For now, just close and save state.
      const submitBtn = emailForm.querySelector(".email-submit");
      const originalText = submitBtn.textContent;
      submitBtn.textContent = "Subscribed!";
      submitBtn.style.background = "#fff";
      submitBtn.style.boxShadow = "0 0 15px #fff";
      
      setTimeout(() => {
        closePopup();
        submitBtn.textContent = originalText;
        submitBtn.style.background = "";
        submitBtn.style.boxShadow = "";
        emailForm.reset();
      }, 1500);
    });
  }
});
