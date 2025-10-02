// Cybersecurity Themed Preloader - Hackversity Digital Fortress
// This preloader enhances user experience without affecting existing functionality

class CyberSecurityPreloader {
    constructor() {
        this.preloader = null;
        this.progressBar = null;
        this.statusText = null;
        this.minDisplayTime = 2000; // Minimum 2 seconds display
        this.maxDisplayTime = 5000; // Maximum 5 seconds display
        this.startTime = Date.now();
        
        // Security-themed status messages
        this.statusMessages = [
            'Initializing Security Protocols...',
            'Scanning Network Perimeter...',
            'Validating Authentication Systems...',
            'Loading Encryption Modules...',
            'Establishing Secure Connection...',
            'Activating Firewall Protection...',
            'Verifying Digital Signatures...',
            'Deploying Security Framework...',
            'System Ready - Welcome to Hackversity'
        ];
        
        this.currentMessageIndex = 0;
        this.messageInterval = null;
        this.progressInterval = null;
        
        this.init();
    }
    
    init() {
        // Get references to existing preloader elements
        this.preloader = document.getElementById('cyber-preloader');
        this.progressBar = document.getElementById('progress-bar');
        this.statusText = document.getElementById('preloader-status');
        
        if (this.preloader) {
            this.startAnimation();
            
            // Hide preloader when page is fully loaded
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => {
                    this.checkPageLoad();
                });
            } else {
                // Page already loaded, start hiding process
                setTimeout(() => {
                    this.checkPageLoad();
                }, 100);
            }
            
            window.addEventListener('load', () => {
                this.hidePreloader();
            });
        }
    }
    
    createPreloader() {
        // Get references to existing preloader elements (created inline in HTML)
        this.preloader = document.getElementById('cyber-preloader');
        this.progressBar = document.getElementById('progress-bar');
        this.statusText = document.getElementById('preloader-status');
        
        // If preloader doesn't exist, create it (fallback)
        if (!this.preloader) {
            const preloaderHTML = `
                <div class="preloader" id="cyber-preloader">
                    <div class="security-grid"></div>
                    <div class="security-icons">
                        <div class="security-icon">🛡️</div>
                        <div class="security-icon">🔐</div>
                        <div class="security-icon">🔒</div>
                        <div class="security-icon">⚡</div>
                        <div class="security-icon">🔑</div>
                    </div>
                    <div class="preloader-logo">
                        <h1 class="preloader-title">Hackversity</h1>
                        <p class="preloader-subtitle">Digital Fortress</p>
                    </div>
                    <div class="security-scanner">
                        <div class="scanner-ring"></div>
                        <div class="scanner-ring"></div>
                        <div class="scanner-ring"></div>
                        <div class="scanner-center"></div>
                    </div>
                    <div class="progress-container">
                        <div class="progress-bar" id="progress-bar"></div>
                    </div>
                    <div class="preloader-status" id="preloader-status">
                        Initializing Security Protocols...
                    </div>
                </div>
            `;
            
            document.body.insertAdjacentHTML('afterbegin', preloaderHTML);
            
            // Get references again
            this.preloader = document.getElementById('cyber-preloader');
            this.progressBar = document.getElementById('progress-bar');
            this.statusText = document.getElementById('preloader-status');
        }
    }
    
    startAnimation() {
        if (!this.preloader) return;
        
        // Start message rotation
        this.startMessageRotation();
        
        // Start progress animation
        this.startProgressAnimation();
    }
    
    startMessageRotation() {
        this.messageInterval = setInterval(() => {
            if (this.currentMessageIndex < this.statusMessages.length - 1) {
                this.currentMessageIndex++;
                if (this.statusText) {
                    this.statusText.textContent = this.statusMessages[this.currentMessageIndex];
                }
            }
        }, 500);
    }
    
    startProgressAnimation() {
        let progress = 0;
        const increment = Math.random() * 3 + 1; // Random increment between 1-4
        
        this.progressInterval = setInterval(() => {
            progress += increment;
            if (progress > 100) progress = 100;
            
            if (this.progressBar) {
                this.progressBar.style.width = `${progress}%`;
            }
            
            if (progress >= 100) {
                clearInterval(this.progressInterval);
                setTimeout(() => {
                    this.hidePreloader();
                }, 500);
            }
        }, 50);
    }
    
    checkPageLoad() {
        // Ensure minimum display time
        const elapsedTime = Date.now() - this.startTime;
        const remainingTime = Math.max(0, this.minDisplayTime - elapsedTime);
        
        setTimeout(() => {
            if (document.readyState === 'complete') {
                this.hidePreloader();
            }
        }, remainingTime);
    }
    
    hidePreloader() {
        if (!this.preloader) return;
        
        // Clear intervals
        if (this.messageInterval) {
            clearInterval(this.messageInterval);
        }
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
        }
        
        // Ensure we've shown for minimum time
        const elapsedTime = Date.now() - this.startTime;
        const delay = Math.max(0, this.minDisplayTime - elapsedTime);
        
        setTimeout(() => {
            // Final status message
            if (this.statusText) {
                this.statusText.textContent = 'System Ready - Welcome to Hackversity';
            }
            
            // Set progress to 100%
            if (this.progressBar) {
                this.progressBar.style.width = '100%';
            }
            
            // Hide preloader after a brief delay
            setTimeout(() => {
                if (this.preloader) {
                    this.preloader.classList.add('hidden');
                    
                    // Remove from DOM after transition
                    setTimeout(() => {
                        if (this.preloader && this.preloader.parentNode) {
                            this.preloader.parentNode.removeChild(this.preloader);
                        }
                    }, 800);
                }
            }, 300);
        }, delay);
    }
    
    // Public method to manually hide preloader (for emergency cases)
    forceHide() {
        if (this.preloader) {
            this.preloader.classList.add('hidden');
            setTimeout(() => {
                if (this.preloader && this.preloader.parentNode) {
                    this.preloader.parentNode.removeChild(this.preloader);
                }
            }, 800);
        }
    }
}

// Initialize preloader immediately or when DOM is ready
function initializePreloader() {
    // Only initialize if we haven't already and it's a fresh page load
    if (!window.cyberPreloader && !document.body.classList.contains('ajax-loading')) {
        window.cyberPreloader = new CyberSecurityPreloader();
    }
}

// Try to initialize immediately
if (document.readyState === 'loading') {
    // If document is still loading, initialize right away
    initializePreloader();
} else {
    // If document is already loaded, check if we should still show preloader
    document.addEventListener('DOMContentLoaded', initializePreloader);
}

// Fallback initialization if DOMContentLoaded already fired
if (document.readyState !== 'loading') {
    initializePreloader();
}

// Prevent preloader on back/forward navigation
window.addEventListener('pageshow', (event) => {
    if (event.persisted && window.cyberPreloader) {
        window.cyberPreloader.forceHide();
    }
});

// Export for potential use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CyberSecurityPreloader;
}