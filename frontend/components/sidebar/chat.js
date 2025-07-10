// Add this function at the top of your chat.js file
function getUserId() {
    let userId = localStorage.getItem('creatormate_user_id');
    if (!userId) {
        userId = 'user_' + Math.random().toString(36).substring(2, 15);
        localStorage.setItem('creatormate_user_id', userId);
    }
    return userId;
}

// Add this code in your DOMContentLoaded event handler
const channelForm = document.getElementById('channel-info-form');
if (channelForm) {
    channelForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const channelInfo = {
            name: document.getElementById('channel-name')?.value || "Unknown",
            niche: document.getElementById('channel-niche')?.value || "Unknown",
            content_type: document.getElementById('channel-type')?.value || "Unknown",
            subscriber_count: parseInt(document.getElementById('channel-subs')?.value || "0"),
            avg_view_count: parseInt(document.getElementById('channel-views')?.value || "0"),
            ctr: parseFloat(document.getElementById('channel-ctr')?.value || "0"),
            retention: parseFloat(document.getElementById('channel-retention')?.value || "0"),
            upload_frequency: document.getElementById('channel-frequency')?.value || "Unknown",
            video_length: document.getElementById('channel-length')?.value || "Unknown",
            monetization_status: document.getElementById('channel-monetization')?.value || "Unknown",
            primary_goal: document.getElementById('channel-goal')?.value || "Unknown",
            notes: document.getElementById('channel-notes')?.value || "",
            user_id: getUserId()
        };
        
        fetch('/api/agent/set-channel-info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(channelInfo)
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                addMessage('agent', 'Thank you for updating your channel information! I can now provide more personalized advice tailored to your specific channel metrics and goals.');
            }
        })
        .catch(err => {
            console.error('Error:', err);
            addMessage('agent', 'Sorry, I encountered an error updating your channel information. Please try again.');
        });
    });
}

// Update your sendMessage function to include user_id
function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;
    
    console.log('Sending message:', message);
    
    // Add user message to chat
    addMessage('user', message);
    
    // Clear input
    chatInput.value = '';
    
    // Get user ID
    const userId = getUserId();
    
    // Call API
    fetch('/api/agent/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            message,
            user_id: userId
        })
    })
    .then(res => {
        console.log('Response status:', res.status);
        return res.json();
    })
    .then(data => {
        console.log('Response data:', data);
        // Add AI response
        addMessage('agent', data.response);
    })
    .catch(err => {
        console.error('Error:', err);
        addMessage('agent', 'Sorry, I encountered an error. Please try again.');
    });
}
// Add support for agent personalization

// Listen for agent settings updates
document.addEventListener('agentSettingsUpdated', function(event) {
  updateChatAvatars(event.detail);
});

// Check for settings when the chat initializes
document.addEventListener('DOMContentLoaded', function() {
  if (window.agentSettings) {
    updateChatAvatars(window.agentSettings);
  }
});

// Update agent avatars in chat messages
function updateChatAvatars(settings) {
  // Get the avatar source based on settings
  const avatarSrc = `https://placehold.co/100x100/6366f1/FFFFFF.png?text=${settings.avatar.split('-')[1]}`;
  
  // Find all agent avatars in chat and update them
  document.querySelectorAll('.agent-avatar').forEach(img => {
    img.src = avatarSrc;
  });
}