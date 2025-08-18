/**
 * Image Optimization and Lazy Loading
 * Enhances performance with intersection observer and progressive loading
 */

class ImageOptimizer {
  constructor() {
    this.lazyImages = [];
    this.imageObserver = null;
    this.init();
  }
  
  init() {
    // Set up intersection observer for lazy loading
    this.setupIntersectionObserver();
    
    // Enhance existing images
    this.enhanceImages();
    
    // Preload critical images
    this.preloadCriticalImages();
    
    // Add loading event listeners
    this.addLoadingHandlers();
  }
  
  setupIntersectionObserver() {
    if ('IntersectionObserver' in window) {
      this.imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            this.loadImage(img);
            observer.unobserve(img);
          }
        });
      }, {
        // Load images 50px before they enter the viewport
        rootMargin: '50px 0px',
        threshold: 0.01
      });
    }
  }
  
  enhanceImages() {
    // Find all images with loading="lazy"
    const lazyImages = document.querySelectorAll('img[loading="lazy"]');
    
    lazyImages.forEach(img => {
      // Add to intersection observer if available
      if (this.imageObserver) {
        this.imageObserver.observe(img);
      } else {
        // Fallback for browsers without intersection observer
        this.loadImage(img);
      }
    });
    
    // Handle images that are already loaded
    const eagerImages = document.querySelectorAll('img[loading="eager"], img:not([loading])');
    eagerImages.forEach(img => {
      if (img.complete) {
        img.classList.add('loaded');
      } else {
        img.addEventListener('load', () => {
          img.classList.add('loaded');
        });
      }
    });
  }
  
  loadImage(img) {
    // Don't reload if already loaded
    if (img.classList.contains('loaded')) {
      return;
    }
    
    // Create a new image to test loading
    const imageLoader = new Image();
    
    imageLoader.onload = () => {
      // Image loaded successfully
      img.src = imageLoader.src;
      img.classList.add('loaded');
      this.announceImageLoad(img);
    };
    
    imageLoader.onerror = () => {
      // Handle loading error
      console.warn('Failed to load image:', img.src);
      img.classList.add('error');
      img.alt = img.alt + ' (Image failed to load)';
    };
    
    // Start loading
    imageLoader.src = img.src;
  }
  
  preloadCriticalImages() {
    // Preload hero images and first carousel image
    const criticalImages = document.querySelectorAll('.hero-image, .carousel-item.active img');
    
    criticalImages.forEach(img => {
      if (img.loading !== 'eager') {
        img.loading = 'eager';
      }
      
      const link = document.createElement('link');
      link.rel = 'preload';
      link.as = 'image';
      link.href = img.src;
      document.head.appendChild(link);
    });
  }
  
  addLoadingHandlers() {
    // Add loading class management
    document.addEventListener('DOMContentLoaded', () => {
      const allImages = document.querySelectorAll('img');
      
      allImages.forEach(img => {
        if (!img.complete) {
          img.addEventListener('load', () => {
            img.classList.add('loaded');
          });
          
          img.addEventListener('error', () => {
            img.classList.add('error');
          });
        } else {
          img.classList.add('loaded');
        }
      });
    });
  }
  
  announceImageLoad(img) {
    // Announce to screen readers if image has important context
    if (img.getAttribute('data-announce')) {
      const announcement = document.createElement('div');
      announcement.setAttribute('aria-live', 'polite');
      announcement.setAttribute('aria-atomic', 'true');
      announcement.className = 'sr-only';
      announcement.textContent = `Image loaded: ${img.alt}`;
      
      document.body.appendChild(announcement);
      
      setTimeout(() => {
        document.body.removeChild(announcement);
      }, 1000);
    }
  }
  
  // Public method to force load all lazy images (useful for print, etc.)
  loadAllImages() {
    const lazyImages = document.querySelectorAll('img[loading="lazy"]:not(.loaded)');
    lazyImages.forEach(img => this.loadImage(img));
  }
  
  // Public method to get loading statistics
  getLoadingStats() {
    const allImages = document.querySelectorAll('img');
    const loadedImages = document.querySelectorAll('img.loaded');
    const errorImages = document.querySelectorAll('img.error');
    
    return {
      total: allImages.length,
      loaded: loadedImages.length,
      errors: errorImages.length,
      pending: allImages.length - loadedImages.length - errorImages.length
    };
  }
}

// Initialize image optimizer when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.imageOptimizer = new ImageOptimizer();
});

// Load all images before printing
window.addEventListener('beforeprint', () => {
  if (window.imageOptimizer) {
    window.imageOptimizer.loadAllImages();
  }
});

// Performance monitoring
if ('PerformanceObserver' in window) {
  const perfObserver = new PerformanceObserver((list) => {
    list.getEntries().forEach((entry) => {
      if (entry.entryType === 'largest-contentful-paint') {
        // Log LCP for debugging
        console.log('Largest Contentful Paint:', entry.startTime);
      }
    });
  });
  
  perfObserver.observe({ entryTypes: ['largest-contentful-paint'] });
}
