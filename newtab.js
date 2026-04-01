// Background images
const backgrounds = [
  'backgrounds/5571.jpg',
  'backgrounds/5572.jpg',
  'backgrounds/5573.jpg',
  'backgrounds/5574.jpg',
  'backgrounds/5575.jpg',
  'backgrounds/5576.jpg',
  'backgrounds/5577.jpg',
  'backgrounds/5578.jpg',
  'backgrounds/5579.jpg',
  'backgrounds/5580.jpg'
];

// Pick a random background, avoid repeating last one
function setBackground() {
  const lastBg = localStorage.getItem('tvk_last_bg') || '';
  let available = backgrounds.filter(b => b !== lastBg);
  if (available.length === 0) available = backgrounds;
  const chosen = available[Math.floor(Math.random() * available.length)];
  localStorage.setItem('tvk_last_bg', chosen);

  const bgEl = document.getElementById('bg');
  bgEl.style.backgroundImage = 'url(' + chosen + ')';
}

// Clock
function updateClock() {
  const now = new Date();
  const hours = now.getHours().toString().padStart(2, '0');
  const minutes = now.getMinutes().toString().padStart(2, '0');
  document.getElementById('clock').textContent = hours + ':' + minutes;

  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  document.getElementById('date').textContent = now.toLocaleDateString('en-US', options);
}

// Search
document.getElementById('searchBar').addEventListener('keydown', function(e) {
  if (e.key === 'Enter' && this.value.trim()) {
    var query = encodeURIComponent(this.value.trim());
    window.location.href = 'https://www.google.com/search?q=' + query;
  }
});

// Top sites
function loadShortcuts() {
  if (chrome && chrome.topSites) {
    chrome.topSites.get(function(sites) {
      var container = document.getElementById('shortcuts');
      var topSites = sites.slice(0, 8);
      topSites.forEach(function(site) {
        var domain = '';
        try { domain = new URL(site.url).hostname; } catch(e) { domain = site.url; }
        var initial = domain.replace('www.', '').charAt(0).toUpperCase();

        var a = document.createElement('a');
        a.className = 'shortcut';
        a.href = site.url;

        var iconDiv = document.createElement('div');
        iconDiv.className = 'shortcut-icon';
        iconDiv.textContent = initial;

        var label = document.createElement('span');
        label.className = 'shortcut-label';
        label.textContent = site.title || domain;

        a.appendChild(iconDiv);
        a.appendChild(label);
        container.appendChild(a);
      });
    });
  }
}

// Init
setBackground();
updateClock();
setInterval(updateClock, 10000);
loadShortcuts();
