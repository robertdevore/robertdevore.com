document.addEventListener('DOMContentLoaded', function () {
  calculateReadingTime();
});

// Function to calculate reading time based on word count
function calculateReadingTime() {  
  const WORDS_PER_MINUTE = 200;
  
  // Try different selectors to find the article content
  let articleDiv = document.getElementById('article');
  if (!articleDiv) {
    articleDiv = document.querySelector('article.prose');
  }
  if (!articleDiv) {
    articleDiv = document.querySelector('.stattic-content');
  }
  if (!articleDiv) {
    articleDiv = document.querySelector('article');
  }

  // If articleDiv is missing, do nothing
  if (!articleDiv) {
    return;
  }

  // Get plain text (ignores inner HTML tags)
  const text = articleDiv.textContent || articleDiv.innerText || "";
  const wordCount = text.trim().split(/\s+/).length;
  const readingMinutes = Math.ceil(wordCount / WORDS_PER_MINUTE);
  const output = `${readingMinutes} minute${readingMinutes !== 1 ? 's' : ''}`;

  // Check for the .reading-time span and update if found
  const readTimeEl = document.querySelector('.reading-time');
  if (readTimeEl) {
    readTimeEl.textContent = output;
  } else {
    console.log('No .reading-time span found');
  }
  
  // Also check for .read-time span for backward compatibility
  const readTimeElAlt = document.querySelector('.read-time');
  if (readTimeElAlt) {
    readTimeElAlt.textContent = output;
  } else {
    console.log('No .read-time span found');
  }
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        
        if (targetElement) {
        targetElement.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
        }
    });
});