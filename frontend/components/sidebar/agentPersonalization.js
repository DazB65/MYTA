/**
 * Agent Personalization Module
 * Handles the customization of the AI agent appearance and identity
 */
(function() {
  // Settings object with defaults
  const defaultSettings = {
    name: "Your Personal Agent",
    avatar: "avatar-1"
  };
  
  // State management
  let agentSettings = {...defaultSettings};
  
  // DOM Elements
  let elements = {
    nameDisplay: null,
    avatarImages: null,
    modal: null
  };
  
  /**
   * Initialize the personalization module
   */
  function init() {
    // Load saved settings
    loadSettings();
    
    // Cache DOM elements
    cacheElements();
    
    // Attach event listeners
    attachEventListeners();
    
    // Apply current settings
    applySettings();
    
    // Expose settings to window for other components
    window.agentSettings = agentSettings;
    
    // Make API available to other modules
    window.agentPersonalization = {
      getSettings: getSettings,
      updateSettings: updateSettings,
      openModal: openModal,
      closeModal: closeModal
    };
  }
  
  /**
   * Cache DOM elements for performance
   */
  function cacheElements() {
    elements.nameDisplay = document.getElementById('agent-name-display');
    elements.avatarImages = document.querySelectorAll('.agent-avatar');
    elements.modal = document.getElementById('personalization-modal');
    elements.nameInput = document.getElementById('agent-name');
    elements.avatarOptions = document.querySelectorAll('.avatar-option');
    elements.saveButton = document.getElementById('save-personalization');
    elements.closeButton = document.querySelector('.close-modal');
    elements.personalizeButton = document.getElementById('personalize-agent');
  }
  
  /**
   * Attach event listeners to DOM elements
   */
  function attachEventListeners() {
    // Only attach events if elements exist
    if (elements.personalizeButton) {
      elements.personalizeButton.addEventListener('click', openModal);
    }
    
    if (elements.closeButton) {
      elements.closeButton.addEventListener('click', closeModal);
    }
    
    if (elements.modal) {
      // Close when clicking outside the modal content
      elements.modal.addEventListener('click', function(e) {
        if (e.target === elements.modal) {
          closeModal();
        }
      });
    }
    
    // Avatar selection
    elements.avatarOptions.forEach(option => {
      option.addEventListener('click', function() {
        selectAvatar(this.dataset.avatar);
      });
    });
    
    // Save button
    if (elements.saveButton) {
      elements.saveButton.addEventListener('click', saveSettings);
    }
    
    // Listen for changes in other tabs/windows
    window.addEventListener('storage', function(e) {
      if (e.key === 'agentSettings') {
        loadSettings();
        applySettings();
      }
    });
  }
  
  /**
   * Load settings from localStorage
   */
  function loadSettings() {
    try {
      const savedSettings = localStorage.getItem('agentSettings');
      if (savedSettings) {
        agentSettings = {...defaultSettings, ...JSON.parse(savedSettings)};
      }
    } catch (e) {
      console.error('Error loading agent settings', e);
      agentSettings = {...defaultSettings};
    }
  }
  
  /**
   * Save current settings to localStorage
   */
  function saveSettings() {
    // Get current values from modal
    if (elements.nameInput) {
      agentSettings.name = elements.nameInput.value.trim() || defaultSettings.name;
    }
    
    const selectedAvatar = document.querySelector('.avatar-option.border-purple-700');
    if (selectedAvatar) {
      agentSettings.avatar = selectedAvatar.dataset.avatar;
    }
    
    // Save to localStorage
    localStorage.setItem('agentSettings', JSON.stringify(agentSettings));
    
    // Update UI
    applySettings();
    
    // Update window object for other components
    window.agentSettings = {...agentSettings};
    
    // Notify other components
    document.dispatchEvent(new CustomEvent('agentSettingsUpdated', {
      detail: {...agentSettings}
    }));
    
    // Close modal
    closeModal();
  }
  
  /**
   * Get a copy of the current settings
   */
  function getSettings() {
    return {...agentSettings};
  }
  
  /**
   * Update settings programmatically
   */
  function updateSettings(newSettings) {
    agentSettings = {...agentSettings, ...newSettings};
    localStorage.setItem('agentSettings', JSON.stringify(agentSettings));
    applySettings();
    
    // Notify other components
    document.dispatchEvent(new CustomEvent('agentSettingsUpdated', {
      detail: {...agentSettings}
    }));
  }
  
  /**
   * Apply current settings to the UI
   */
  function applySettings() {
    // Update agent name display
    if (elements.nameDisplay) {
      elements.nameDisplay.textContent = agentSettings.name;
    }
    
    // Update avatar images
    const avatarSrc = `assets/images/CM Logo White.svg`;
    elements.avatarImages.forEach(img => {
      img.src = avatarSrc;
    });
  }
  
  /**
   * Open the personalization modal
   */
  function openModal() {
    // Pre-fill current settings
    if (elements.nameInput) {
      elements.nameInput.value = agentSettings.name;
    }
    
    // Select current avatar
    selectAvatar(agentSettings.avatar);
    
    // Show modal
    if (elements.modal) {
      elements.modal.classList.remove('hidden');
    }
  }
  
  /**
   * Close the personalization modal
   */
  function closeModal() {
    if (elements.modal) {
      elements.modal.classList.add('hidden');
    }
  }
  
  /**
   * Select an avatar in the modal
   */
  function selectAvatar(avatarId) {
    elements.avatarOptions.forEach(option => {
      option.classList.remove('border-purple-700');
      option.classList.add('border-transparent');
      
      if (option.dataset.avatar === avatarId) {
        option.classList.remove('border-transparent');
        option.classList.add('border-purple-700');
      }
    });
  }
  
  // Initialize when DOM is ready
  document.addEventListener('DOMContentLoaded', init);
})();