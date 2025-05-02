/**
 * Q&A Application - Main JavaScript
 * Handles the interaction between UI and the Q&A API
 */

// Constants
const API_URL = 'http://0.0.0.0:8000'; // Base API URL
const API_ENDPOINTS = {
  ask: `${API_URL}/api/ask`,
  history: `${API_URL}/api/history`
};

// Initialize the application when DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
  initializeApp();
});

/**
 * Initialize application components and event listeners
 */
function initializeApp() {
  // Cache DOM elements
  const elements = {
    questionForm: document.getElementById('question-form'),
    questionInput: document.getElementById('question-input'),
    submitButton: document.getElementById('submit-btn'),
    loaderContainer: document.getElementById('loader-container'),
    answerContainer: document.getElementById('answer-container'),
    answerText: document.getElementById('answer-text'),
    errorContainer: document.getElementById('error-container'),
    errorText: document.getElementById('error-text'),
    sourcesList: document.getElementById('sources-list'),
    historyContainer: document.getElementById('history-container'),
    historyList: document.getElementById('history-list')
  };

  // Setup event listeners
  setupEventListeners(elements);
  
  // Load question history
  loadQuestionHistory(elements);
}

/**
 * Set up event listeners for various UI interactions
 * @param {Object} elements - DOM elements
 */
function setupEventListeners(elements) {
  // Question form submission
  elements.questionForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    await handleQuestionSubmit(elements);
  });
}

/**
 * Handle question submission
 * @param {Object} elements - DOM elements
 */
async function handleQuestionSubmit(elements) {
  const { 
    questionInput, 
    submitButton, 
    loaderContainer,
    answerContainer, 
    errorContainer 
  } = elements;
  
  // Get the question
  const question = questionInput.value.trim();
  
  // Validate question
  if (!question || question.length < 3) {
    showError(elements, 'Please enter a valid question (at least 3 characters).');
    return;
  }
  
  // Update UI to loading state
  submitButton.disabled = true;
  loaderContainer.style.display = 'block';
  answerContainer.style.display = 'none';
  errorContainer.style.display = 'none';
  
  try {
    // Send API request
    const response = await fetch(API_ENDPOINTS.ask, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ question })
    });
    
    // Check for errors
    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }
    
    // Parse response
    const data = await response.json();
    
    // Display the answer
    displayAnswer(elements, data);
    
    // Refresh history
    loadQuestionHistory(elements);
    
  } catch (error) {
    console.error('Error submitting question:', error);
    showError(elements, `An error occurred: ${error.message}`);
  } finally {
    // Reset UI state
    submitButton.disabled = false;
    loaderContainer.style.display = 'none';
  }
}

/**
 * Display the API response answer in the UI
 * @param {Object} elements - DOM elements
 * @param {Object} data - Response data from the API
 */
function displayAnswer(elements, data) {
  const { answerContainer, answerText, sourcesList } = elements;
  
  // Set answer text
  answerText.textContent = data.answer;
  
  // Clear and populate sources if available
  sourcesList.innerHTML = '';
  if (data.sources && data.sources.length > 0) {
    data.sources.forEach(source => {
      const li = document.createElement('li');
      li.textContent = source;
      sourcesList.appendChild(li);
    });
    document.getElementById('sources-container').style.display = 'block';
  } else {
    document.getElementById('sources-container').style.display = 'none';
  }
  
  // Show the answer container
  answerContainer.style.display = 'block';
}

/**
 * Show error message in the UI
 * @param {Object} elements - DOM elements
 * @param {String} message - Error message to display
 */
function showError(elements, message) {
  const { errorContainer, errorText } = elements;
  errorText.textContent = message;
  errorContainer.style.display = 'block';
}

/**
 * Load and display question history from the API
 * @param {Object} elements - DOM elements
 */
async function loadQuestionHistory(elements) {
  const { historyList, historyContainer } = elements;
  
  try {
    // Fetch history from API
    const response = await fetch(API_ENDPOINTS.history);
    
    if (!response.ok) {
      throw new Error(`Failed to load history: ${response.status}`);
    }
    
    const data = await response.json();
    const history = data.history || [];
    
    // Clear existing list
    historyList.innerHTML = '';
    
    // If no history items, show a message
    if (history.length === 0) {
      historyList.innerHTML = `
        <div class="empty-history">
          <p>No questions have been asked yet.</p>
        </div>
      `;
      return;
    }
    
    // Create history items
    history.forEach(item => {
      const historyItem = createHistoryItem(item, elements);
      historyList.appendChild(historyItem);
    });
    
  } catch (error) {
    console.error('Error loading history:', error);
  }
}

/**
 * Create a history item element
 * @param {Object} item - History item data
 * @param {Object} elements - DOM elements
 * @returns {HTMLElement} - List item element
 */
function createHistoryItem(item, elements) {
  const { id, question, answer, timestamp } = item;
  const date = new Date(timestamp);
  const formattedDate = date.toLocaleString();
  
  // Create list item
  const li = document.createElement('li');
  li.className = 'history-item';
  li.dataset.id = id;
  
  // Create history content
  li.innerHTML = `
    <div class="history-question">${question}</div>
    <div class="history-answer">${truncateText(answer, 100)}</div>
    <div class="history-meta">
      <span>${formattedDate}</span>
    </div>
  `;
  
  // Add click handler to reload the Q&A
  li.addEventListener('click', () => {
    elements.questionInput.value = question;
    const data = { answer, sources: [] };
    displayAnswer(elements, data);
    elements.answerContainer.scrollIntoView({ behavior: 'smooth' });
  });
  
  return li;
}

/**
 * Truncate text to a specified length
 * @param {String} text - Text to truncate
 * @param {Number} maxLength - Maximum length
 * @returns {String} - Truncated text
 */
function truncateText(text, maxLength) {
  if (text.length <= maxLength) return text;
  return text.substr(0, maxLength) + '...';
}
