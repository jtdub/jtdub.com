/**
 * Theme Toggle Functionality
 * Handles dark/light mode switching with persistent user preference
 */

class ThemeManager {
  constructor() {
    this.storageKey = 'jtdub-theme-preference';
    this.themes = {
      light: 'light',
      dark: 'dark'
    };
    
    this.init();
  }
  
  init() {
    // Set initial theme before DOM manipulation
    this.setInitialTheme();
    
    // Initialize theme toggle button functionality
    this.initializeThemeToggle();
    
    // Listen for system theme changes
    this.watchSystemTheme();
  }
  
  initializeThemeToggle() {
    // Find both desktop and mobile theme toggle buttons
    this.toggleButton = document.querySelector('.theme-toggle');
    this.toggleButtonMobile = document.querySelector('.theme-toggle-mobile');
    
    // Add click event listeners for both buttons
    if (this.toggleButton) {
      this.toggleButton.addEventListener('click', () => this.toggleTheme());
    }
    
    if (this.toggleButtonMobile) {
      this.toggleButtonMobile.addEventListener('click', () => this.toggleTheme());
    }
    
    // Update initial icon and label based on current theme
    const currentTheme = this.getCurrentTheme();
    this.updateToggleIcon(currentTheme);
    this.updateToggleLabel(currentTheme);
  }
  
  setInitialTheme() {
    // Check for saved preference first
    const savedTheme = localStorage.getItem(this.storageKey);
    
    if (savedTheme && Object.values(this.themes).includes(savedTheme)) {
      this.applyTheme(savedTheme);
    } else {
      // Fall back to system preference
      const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      this.applyTheme(systemPrefersDark ? this.themes.dark : this.themes.light);
    }
  }
  
  toggleTheme() {
    const currentTheme = this.getCurrentTheme();
    const newTheme = currentTheme === this.themes.dark ? this.themes.light : this.themes.dark;
    
    this.applyTheme(newTheme);
    this.saveThemePreference(newTheme);
    
    // Announce theme change to screen readers
    this.announceThemeChange(newTheme);
  }
  
  applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    this.updateToggleIcon(theme);
    this.updateToggleLabel(theme);
  }
  
  getCurrentTheme() {
    return document.documentElement.getAttribute('data-theme') || this.themes.light;
  }
  
  updateToggleIcon(theme) {
    const icon = theme === this.themes.dark ? '☀️' : '🌙';
    
    // Update desktop button
    if (this.toggleButton) {
      const iconElement = this.toggleButton.querySelector('.theme-toggle-icon');
      if (iconElement) {
        iconElement.textContent = icon;
      }
    }
    
    // Update mobile button
    if (this.toggleButtonMobile) {
      const iconElement = this.toggleButtonMobile.querySelector('.theme-toggle-icon');
      if (iconElement) {
        iconElement.textContent = icon;
      }
    }
  }
  
  updateToggleLabel(theme) {
    const nextTheme = theme === this.themes.dark ? 'light' : 'dark';
    const label = `Switch to ${nextTheme} theme`;
    
    // Update desktop button
    if (this.toggleButton) {
      this.toggleButton.setAttribute('aria-label', label);
    }
    
    // Update mobile button
    if (this.toggleButtonMobile) {
      this.toggleButtonMobile.setAttribute('aria-label', label);
    }
  }
  
  saveThemePreference(theme) {
    try {
      localStorage.setItem(this.storageKey, theme);
    } catch (error) {
      console.warn('Could not save theme preference:', error);
    }
  }
  
  announceThemeChange(theme) {
    // Create temporary announcement for screen readers
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only';
    announcement.textContent = `Switched to ${theme} theme`;
    
    document.body.appendChild(announcement);
    
    // Remove after announcement
    setTimeout(() => {
      document.body.removeChild(announcement);
    }, 1000);
  }
  
  watchSystemTheme() {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    mediaQuery.addEventListener('change', (e) => {
      // Only auto-switch if user hasn't set a manual preference
      const savedTheme = localStorage.getItem(this.storageKey);
      if (!savedTheme) {
        this.applyTheme(e.matches ? this.themes.dark : this.themes.light);
      }
    });
  }
  
  // Public API for external theme detection
  isDarkMode() {
    return this.getCurrentTheme() === this.themes.dark;
  }
  
  isLightMode() {
    return this.getCurrentTheme() === this.themes.light;
  }
}

// Initialize theme manager when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.themeManager = new ThemeManager();
});

// Prevent flash of unstyled content by applying theme immediately
(function() {
  const storageKey = 'jtdub-theme-preference';
  const savedTheme = localStorage.getItem(storageKey);
  
  if (savedTheme && (savedTheme === 'light' || savedTheme === 'dark')) {
    document.documentElement.setAttribute('data-theme', savedTheme);
  } else {
    // Use system preference
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    document.documentElement.setAttribute('data-theme', systemPrefersDark ? 'dark' : 'light');
  }
})();
