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
    // Create theme toggle button
    this.createThemeToggle();
    
    // Set initial theme
    this.setInitialTheme();
    
    // Listen for system theme changes
    this.watchSystemTheme();
  }
  
  createThemeToggle() {
    const toggle = document.createElement('button');
    toggle.className = 'theme-toggle';
    toggle.setAttribute('aria-label', 'Toggle dark/light theme');
    toggle.setAttribute('type', 'button');
    toggle.innerHTML = `
      <span class="theme-toggle-icon" aria-hidden="true">🌙</span>
    `;
    
    toggle.addEventListener('click', () => this.toggleTheme());
    
    // Add to page
    document.body.appendChild(toggle);
    this.toggleButton = toggle;
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
    const icon = this.toggleButton.querySelector('.theme-toggle-icon');
    icon.textContent = theme === this.themes.dark ? '☀️' : '🌙';
  }
  
  updateToggleLabel(theme) {
    const nextTheme = theme === this.themes.dark ? 'light' : 'dark';
    this.toggleButton.setAttribute('aria-label', `Switch to ${nextTheme} theme`);
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
