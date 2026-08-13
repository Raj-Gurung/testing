/**
 * Nexsus Logistics & Warehousing Company
 * Main Application Script - Training Gating & State Management
 */

(function () {
  'use strict';

  // Storage Keys
  const STORAGE_KEYS = {
    GUIDELINES_READ: 'nexsus_guidelines_read',
    QUIZ_PASSED: 'nexsus_quiz_passed',
    QUIZ_SCORE: 'nexsus_quiz_score'
  };

  // State Manager
  window.NexsusState = {
    isGuidelinesRead: function () {
      return localStorage.getItem(STORAGE_KEYS.GUIDELINES_READ) === 'true';
    },

    markGuidelinesRead: function () {
      localStorage.setItem(STORAGE_KEYS.GUIDELINES_READ, 'true');
      this.updateNavbarAccess();
    },

    getQuizScore: function () {
      const score = localStorage.getItem(STORAGE_KEYS.QUIZ_SCORE);
      return score !== null ? parseFloat(score) : null;
    },

    isQuizPassed: function () {
      const passed = localStorage.getItem(STORAGE_KEYS.QUIZ_PASSED) === 'true';
      const score = this.getQuizScore();
      return passed && score !== null && score > 60;
    },

    canAccessSimulators: function () {
      return this.isGuidelinesRead() && this.isQuizPassed();
    },

    saveQuizResult: function (scorePercent) {
      const passed = scorePercent > 60;
      localStorage.setItem(STORAGE_KEYS.QUIZ_SCORE, scorePercent.toFixed(1));
      localStorage.setItem(STORAGE_KEYS.QUIZ_PASSED, passed ? 'true' : 'false');
      this.updateNavbarAccess();
      return passed;
    },

    resetProgress: function () {
      localStorage.removeItem(STORAGE_KEYS.GUIDELINES_READ);
      localStorage.removeItem(STORAGE_KEYS.QUIZ_PASSED);
      localStorage.removeItem(STORAGE_KEYS.QUIZ_SCORE);
      this.updateNavbarAccess();
    },

    updateNavbarAccess: function () {
      updateNavbarAccess();
    }
  };

  // Inject Custom Styles for Lock Badges, Modals, and Overlay
  function injectStyles() {
    if (document.getElementById('nexsus-gating-styles')) return;

    const style = document.createElement('style');
    style.id = 'nexsus-gating-styles';
    style.textContent = `
      /* Navbar Gating Styles */
      .nav-links a.locked-nav-item {
        opacity: 0.75;
        position: relative;
        cursor: pointer;
      }
      .nav-links a.locked-nav-item::after {
        content: " 🔒";
        font-size: 13px;
        margin-left: 4px;
      }

      /* Locked Modal */
      .nexsus-modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(8, 12, 18, 0.85);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        z-index: 99999;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
        animation: nexsusFadeIn 0.25s ease-out;
      }

      @keyframes nexsusFadeIn {
        from { opacity: 0; transform: scale(0.98); }
        to { opacity: 1; transform: scale(1); }
      }

      .nexsus-modal-card {
        background: #16202E;
        border: 1px solid #2B3B4E;
        border-top: 4px solid #E8590C;
        border-radius: 12px;
        max-width: 520px;
        width: 100%;
        padding: 32px 28px;
        color: #EDEFF2;
        font-family: Arial, sans-serif;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
        text-align: center;
      }

      .nexsus-modal-icon {
        width: 64px;
        height: 64px;
        background: rgba(232, 89, 12, 0.15);
        border: 2px solid #E8590C;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 20px auto;
        font-size: 30px;
        color: #E8590C;
      }

      .nexsus-modal-card h2 {
        font-size: 22px;
        font-weight: 700;
        color: #EDEFF2;
        margin-bottom: 12px;
      }

      .nexsus-modal-card p {
        font-size: 14.5px;
        color: #98A2B0;
        line-height: 1.55;
        margin-bottom: 24px;
      }

      .nexsus-modal-status {
        background: #0F1722;
        border: 1px solid #263242;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 24px;
        font-size: 13.5px;
        text-align: left;
      }

      .nexsus-modal-status div {
        display: flex;
        justify-content: space-between;
        margin-bottom: 6px;
      }

      .nexsus-modal-status div:last-child {
        margin-bottom: 0;
      }

      .nexsus-btn-group {
        display: flex;
        gap: 12px;
        justify-content: center;
        flex-wrap: wrap;
      }

      .nexsus-btn {
        padding: 11px 20px;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 600;
        text-decoration: none;
        cursor: pointer;
        border: none;
        transition: all 0.15s ease;
      }

      .nexsus-btn-primary {
        background: #5B9DF9;
        color: #0B1220;
      }

      .nexsus-btn-primary:hover {
        background: #79AEFA;
        transform: translateY(-1px);
      }

      .nexsus-btn-secondary {
        background: #253142;
        color: #EDEFF2;
        border: 1px solid #38485E;
      }

      .nexsus-btn-secondary:hover {
        background: #314056;
      }

      .nexsus-btn-cancel {
        background: transparent;
        color: #98A2B0;
      }
      .nexsus-btn-cancel:hover {
        color: #EDEFF2;
      }
    `;
    document.head.appendChild(style);
  }

  // Show Lock Warning Modal
  function showLockModal(e) {
    // If simulator access is unlocked, do NOT intercept click or block navigation!
    if (window.NexsusState.canAccessSimulators()) {
      return;
    }

    if (e) e.preventDefault();

    const existingModal = document.getElementById('nexsus-lock-modal');
    if (existingModal) existingModal.remove();

    const isRead = window.NexsusState.isGuidelinesRead();
    const score = window.NexsusState.getQuizScore();
    const isPassed = window.NexsusState.isQuizPassed();

    let statusHtml = `
      <div>
        <span style="color:#98A2B0;">1. Read Guidelines:</span>
        <span style="font-weight:bold; color:${isRead ? '#2BAE66' : '#E8590C'};">
          ${isRead ? '✓ Completed' : '✕ Not Read'}
        </span>
      </div>
      <div>
        <span style="color:#98A2B0;">2. Pass Quiz (>60%):</span>
        <span style="font-weight:bold; color:${isPassed ? '#2BAE66' : '#E8590C'};">
          ${score !== null ? score + '% (Required: >60%)' : '✕ Not Taken'}
        </span>
      </div>
    `;

    const modal = document.createElement('div');
    modal.id = 'nexsus-lock-modal';
    modal.className = 'nexsus-modal-overlay';
    modal.innerHTML = `
      <div class="nexsus-modal-card">
        <div class="nexsus-modal-icon">🔒</div>
        <h2>Training Simulator Locked</h2>
        <p>
          Access to our interactive 3D Crane and Forklift simulators is restricted until you read the safety guidelines and pass the workplace safety quiz with <strong>more than 60%</strong>.
        </p>
        <div class="nexsus-modal-status">
          ${statusHtml}
        </div>
        <div class="nexsus-btn-group">
          <a href="./guidelines.html" class="nexsus-btn nexsus-btn-primary">Read Guidelines</a>
          <a href="./quiz.html" class="nexsus-btn nexsus-btn-secondary">Take Quiz</a>
          <button type="button" class="nexsus-btn nexsus-btn-cancel" id="nexsus-close-modal">Close</button>
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    document.getElementById('nexsus-close-modal').addEventListener('click', function () {
      modal.remove();
    });

    modal.addEventListener('click', function (event) {
      if (event.target === modal) modal.remove();
    });
  }

  function handleDropdownLock(e) {
    if (window.NexsusState.canAccessSimulators()) return;
    if (this.getAttribute('href') === '#training' || this.getAttribute('href') === '#') {
      e.preventDefault();
      showLockModal(e);
    }
  }

  // Update Navbar Links according to Access State
  function updateNavbarAccess() {
    const canAccess = window.NexsusState.canAccessSimulators();
    const trainingLinks = document.querySelectorAll('a[href*="crane.html"], a[href*="forklift.html"]');

    trainingLinks.forEach(link => {
      if (!canAccess) {
        link.classList.add('locked-nav-item');
        link.title = 'Access Locked - Complete Guidelines & Pass Quiz (>60%)';
        link.addEventListener('click', showLockModal);
      } else {
        link.classList.remove('locked-nav-item');
        link.title = 'Simulator Unlocked';
        link.removeEventListener('click', showLockModal);
      }
    });

    // Handle dropdown main trigger if clicked
    const dropdownTrigger = document.querySelector('.dropdown > a');
    if (dropdownTrigger) {
      if (!canAccess) {
        dropdownTrigger.addEventListener('click', handleDropdownLock);
      } else {
        dropdownTrigger.removeEventListener('click', handleDropdownLock);
      }
    }
  }

  // Check Direct Simulator Page Access (For crane.html & forklift.html)
  function checkSimulatorAccess() {
    const currentPath = window.location.pathname.toLowerCase();
    const isSimulatorPage = currentPath.endsWith('crane.html') || currentPath.endsWith('forklift.html');

    if (!isSimulatorPage) return;

    const canAccess = window.NexsusState.canAccessSimulators();
    if (!canAccess) {
      // Block page interaction immediately
      const score = window.NexsusState.getQuizScore();
      const isRead = window.NexsusState.isGuidelinesRead();

      const overlay = document.createElement('div');
      overlay.className = 'nexsus-modal-overlay';
      overlay.style.zIndex = '999999';
      overlay.innerHTML = `
        <div class="nexsus-modal-card">
          <div class="nexsus-modal-icon">🚫</div>
          <h2>Access Denied</h2>
          <p>
            You must read the safety guidelines and score <strong>more than 60%</strong> on the Safety & Ethics Quiz before operating the 3D training machinery.
          </p>
          <div class="nexsus-modal-status">
            <div>
              <span style="color:#98A2B0;">Guidelines Status:</span>
              <span style="font-weight:bold; color:${isRead ? '#2BAE66' : '#E8590C'};">
                ${isRead ? '✓ Completed' : '✕ Pending'}
              </span>
            </div>
            <div>
              <span style="color:#98A2B0;">Current Quiz Score:</span>
              <span style="font-weight:bold; color:${score !== null && score > 60 ? '#2BAE66' : '#E8590C'};">
                ${score !== null ? score + '% (Pass: >60%)' : '✕ Quiz Not Taken'}
              </span>
            </div>
          </div>
          <div class="nexsus-btn-group">
            <a href="./guidelines.html" class="nexsus-btn nexsus-btn-primary">1. Read Guidelines</a>
            <a href="./quiz.html" class="nexsus-btn nexsus-btn-secondary">2. Take Safety Quiz</a>
            <a href="./home.html" class="nexsus-btn nexsus-btn-cancel">Return Home</a>
          </div>
        </div>
      `;
      document.body.appendChild(overlay);

      // Disable canvas if present
      const canvas = document.querySelector('canvas');
      if (canvas) canvas.style.pointerEvents = 'none';
    }
  }

  // Mobile Menu & Dropdown Toggler
  function initMobileMenu() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    // Check or inject mobile toggle button
    let toggleBtn = navbar.querySelector('.mobile-toggle');
    if (!toggleBtn) {
      toggleBtn = document.createElement('button');
      toggleBtn.className = 'mobile-toggle';
      toggleBtn.setAttribute('aria-label', 'Toggle Navigation Menu');
      toggleBtn.innerHTML = '☰';
      navbar.appendChild(toggleBtn);
    }

    const navLinks = navbar.querySelector('.nav-links');
    if (navLinks && toggleBtn) {
      toggleBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        navLinks.classList.toggle('mobile-open');
        toggleBtn.innerHTML = navLinks.classList.contains('mobile-open') ? '✕' : '☰';
      });
    }

    // Handle Mobile Dropdown Toggling
    const dropdown = navbar.querySelector('.dropdown');
    if (dropdown) {
      const dropdownLink = dropdown.querySelector('a');
      if (dropdownLink) {
        dropdownLink.addEventListener('click', function (e) {
          if (window.innerWidth <= 880) {
            // If on mobile, expand/collapse dropdown
            const isExpanded = dropdown.classList.contains('mobile-expanded');
            dropdown.classList.toggle('mobile-expanded');
          }
        });
      }
    }

    // Close menu when clicking outside
    document.addEventListener('click', function (e) {
      if (navLinks && navLinks.classList.contains('mobile-open') && !navbar.contains(e.target)) {
        navLinks.classList.remove('mobile-open');
        if (toggleBtn) toggleBtn.innerHTML = '☰';
      }
    });
  }

  // Logo Image Fallback Handler (Fixes logo image loading issue in home.html)
  function initLogoFallback() {
    const logoImgs = document.querySelectorAll('.logo img, .navbar img');
    logoImgs.forEach(img => {
      // SVG Fallback inline data URI if local image file fails
      const fallbackSvg = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="%235B9DF9"><path d="M20 20 h20 v60 h-20 z M60 20 h20 v60 h-20 z M40 40 h20 v20 h-20 z"/><circle cx="50" cy="50" r="45" fill="none" stroke="%23ffcc00" stroke-width="8"/></svg>`;

      img.onerror = function () {
        if (this.getAttribute('data-tried-fallback') === '2') {
          this.src = fallbackSvg;
          this.onerror = null;
          return;
        }
        this.setAttribute('data-tried-fallback', (parseInt(this.getAttribute('data-tried-fallback') || '0') + 1).toString());
        if (this.src.includes('../img/')) {
          this.src = './img/nexsus_logo.png';
        } else if (this.src.includes('./img/')) {
          this.src = 'img/nexsus_logo.png';
        } else {
          this.src = './img/nexsus_logo.png';
        }
      };

      // Check if image is already broken
      if (img.complete && img.naturalWidth === 0) {
        img.onerror();
      }
    });
  }

  // Initialize on DOM Ready
  function init() {
    injectStyles();
    initMobileMenu();
    initLogoFallback();
    updateNavbarAccess();
    checkSimulatorAccess();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
