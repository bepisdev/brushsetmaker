// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
  const navbarToggle = document.getElementById('navbarToggle');
  const navbarMenu = document.getElementById('navbarMenu');
  
  if (navbarToggle && navbarMenu) {
    navbarToggle.addEventListener('click', function() {
      navbarMenu.classList.toggle('active');
      navbarToggle.classList.toggle('active');
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
      if (!navbarToggle.contains(event.target) && !navbarMenu.contains(event.target)) {
        navbarMenu.classList.remove('active');
        navbarToggle.classList.remove('active');
      }
    });
  }
});

// Smooth Scrolling for Anchor Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (href === '#') return;
    
    e.preventDefault();
    const target = document.querySelector(href);
    
    if (target) {
      const navbarHeight = document.querySelector('.site-header').offsetHeight;
      const targetPosition = target.offsetTop - navbarHeight - 20;
      
      window.scrollTo({
        top: targetPosition,
        behavior: 'smooth'
      });
      
      // Close mobile menu if open
      const navbarMenu = document.getElementById('navbarMenu');
      if (navbarMenu) {
        navbarMenu.classList.remove('active');
      }
    }
  });
});

// Table of Contents Generator
function generateTableOfContents() {
  const tocElement = document.getElementById('toc');
  if (!tocElement) return;
  
  const content = document.querySelector('.page-body, .post-content');
  if (!content) return;
  
  const headings = content.querySelectorAll('h2, h3, h4');
  if (headings.length === 0) return;
  
  const toc = document.createElement('ul');
  toc.className = 'toc-list';
  
  headings.forEach((heading, index) => {
    // Add ID to heading if it doesn't have one
    if (!heading.id) {
      heading.id = 'heading-' + index;
    }
    
    const li = document.createElement('li');
    li.className = 'toc-item toc-' + heading.tagName.toLowerCase();
    
    const link = document.createElement('a');
    link.href = '#' + heading.id;
    link.textContent = heading.textContent;
    
    li.appendChild(link);
    toc.appendChild(li);
  });
  
  tocElement.appendChild(toc);
}

// Highlight Active TOC Item on Scroll
function highlightActiveTocItem() {
  const tocLinks = document.querySelectorAll('#toc a');
  if (tocLinks.length === 0) return;
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const id = entry.target.getAttribute('id');
      const tocLink = document.querySelector(`#toc a[href="#${id}"]`);
      
      if (tocLink) {
        if (entry.isIntersecting) {
          tocLinks.forEach(link => link.classList.remove('active'));
          tocLink.classList.add('active');
        }
      }
    });
  }, {
    rootMargin: '-100px 0px -66%',
    threshold: 0
  });
  
  const headings = document.querySelectorAll('.page-body h2, .page-body h3, .page-body h4, .post-content h2, .post-content h3, .post-content h4');
  headings.forEach(heading => observer.observe(heading));
}

// Copy Code to Clipboard
function setupCodeCopy() {
  const copyButtons = document.querySelectorAll('.copy-button');
  
  copyButtons.forEach(button => {
    button.addEventListener('click', async function() {
      const targetId = this.getAttribute('data-clipboard-target');
      const codeBlock = document.querySelector(targetId);
      
      if (!codeBlock) return;
      
      const code = codeBlock.textContent;
      
      try {
        await navigator.clipboard.writeText(code);
        
        const originalText = this.innerHTML;
        this.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg> Copied!';
        this.style.borderColor = 'var(--success)';
        this.style.color = 'var(--success)';
        
        setTimeout(() => {
          this.innerHTML = originalText;
          this.style.borderColor = '';
          this.style.color = '';
        }, 2000);
      } catch (err) {
        console.error('Failed to copy code:', err);
      }
    });
  });
}

// Add Copy Buttons to Code Blocks
function addCopyButtonsToCodeBlocks() {
  const codeBlocks = document.querySelectorAll('pre code');
  
  codeBlocks.forEach((codeBlock, index) => {
    const pre = codeBlock.parentElement;
    
    // Skip if already has a copy button
    if (pre.parentElement.classList.contains('code-block')) return;
    
    // Wrap in code-block div
    const wrapper = document.createElement('div');
    wrapper.className = 'code-block';
    pre.parentNode.insertBefore(wrapper, pre);
    wrapper.appendChild(pre);
    
    // Add header with copy button
    const header = document.createElement('div');
    header.className = 'code-header';
    
    const language = codeBlock.className.match(/language-(\w+)/);
    const langSpan = document.createElement('span');
    langSpan.className = 'code-language';
    langSpan.textContent = language ? language[1] : 'code';
    
    const copyBtn = document.createElement('button');
    copyBtn.className = 'copy-button';
    copyBtn.setAttribute('data-clipboard-target', '#code-' + index);
    copyBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg> Copy';
    
    header.appendChild(langSpan);
    header.appendChild(copyBtn);
    
    wrapper.insertBefore(header, pre);
    
    // Add ID to code block
    codeBlock.id = 'code-' + index;
  });
}

// Back to Top Button
function setupBackToTop() {
  const backToTopBtn = document.createElement('button');
  backToTopBtn.className = 'back-to-top';
  backToTopBtn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 19V5M5 12l7-7 7 7"/></svg>';
  backToTopBtn.setAttribute('aria-label', 'Back to top');
  document.body.appendChild(backToTopBtn);
  
  // Add styles
  const style = document.createElement('style');
  style.textContent = `
    .back-to-top {
      position: fixed;
      bottom: 2rem;
      right: 2rem;
      width: 50px;
      height: 50px;
      background-color: var(--primary-color);
      color: white;
      border: none;
      border-radius: var(--radius-full);
      cursor: pointer;
      opacity: 0;
      visibility: hidden;
      transition: all var(--transition-base);
      box-shadow: var(--shadow-lg);
      z-index: 999;
    }
    
    .back-to-top.visible {
      opacity: 1;
      visibility: visible;
    }
    
    .back-to-top:hover {
      background-color: var(--primary-dark);
      transform: translateY(-4px);
      box-shadow: var(--shadow-xl);
    }
    
    @media (max-width: 768px) {
      .back-to-top {
        bottom: 1rem;
        right: 1rem;
        width: 45px;
        height: 45px;
      }
    }
  `;
  document.head.appendChild(style);
  
  // Show/hide on scroll
  window.addEventListener('scroll', function() {
    if (window.pageYOffset > 300) {
      backToTopBtn.classList.add('visible');
    } else {
      backToTopBtn.classList.remove('visible');
    }
  });
  
  // Scroll to top on click
  backToTopBtn.addEventListener('click', function() {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
}

// Add Active Class to Current Nav Item
function highlightCurrentNavItem() {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
  
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href && (currentPath === href || currentPath.startsWith(href + '/'))) {
      link.classList.add('active');
    }
  });
}

// External Links - Open in New Tab
function setupExternalLinks() {
  const links = document.querySelectorAll('a[href^="http"]');
  const currentDomain = window.location.hostname;
  
  links.forEach(link => {
    const linkDomain = new URL(link.href).hostname;
    if (linkDomain !== currentDomain) {
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener noreferrer');
    }
  });
}

// Initialize all functions
document.addEventListener('DOMContentLoaded', function() {
  generateTableOfContents();
  highlightActiveTocItem();
  addCopyButtonsToCodeBlocks();
  setupCodeCopy();
  setupBackToTop();
  highlightCurrentNavItem();
  setupExternalLinks();
});

// Handle page visibility changes
document.addEventListener('visibilitychange', function() {
  if (!document.hidden) {
    highlightCurrentNavItem();
  }
});

// Animate elements on scroll
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function(entries) {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate-in');
    }
  });
}, observerOptions);

// Observe elements with animation class
document.addEventListener('DOMContentLoaded', function() {
  const animatedElements = document.querySelectorAll('.feature-card, .page-content, .post-content');
  animatedElements.forEach(el => observer.observe(el));
  
  // Add animation styles
  const animationStyle = document.createElement('style');
  animationStyle.textContent = `
    .feature-card {
      opacity: 0;
      transform: translateY(20px);
      transition: opacity 0.6s ease, transform 0.6s ease;
    }
    
    .feature-card.animate-in {
      opacity: 1;
      transform: translateY(0);
    }
    
    .feature-card:nth-child(1) { transition-delay: 0.1s; }
    .feature-card:nth-child(2) { transition-delay: 0.2s; }
    .feature-card:nth-child(3) { transition-delay: 0.3s; }
    .feature-card:nth-child(4) { transition-delay: 0.4s; }
    .feature-card:nth-child(5) { transition-delay: 0.5s; }
    .feature-card:nth-child(6) { transition-delay: 0.6s; }
  `;
  document.head.appendChild(animationStyle);
});
