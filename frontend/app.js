const API_BASE = '/api/projects';

async function fetchProjects() {
    try {
        const response = await fetch(`${API_BASE}/`);
        if (!response.ok) throw new Error('Failed to fetch projects');
        return await response.json();
    } catch (error) {
        console.error('Error fetching projects:', error);
        return { projects: [], total: 0 };
    }
}

function createProjectCard(project) {
    const elapsed = project.elapsed_time || { days: 0, hours: 0, minutes: 0, seconds: 0 };
    const spent = project.spent_time || { days: 0, hours: 0, minutes: 0, seconds: 0 };
    
    const card = document.createElement('div');
    card.className = 'project-card';
    card.innerHTML = `
        <div class="project-header">
            <h2 class="project-name">${escapeHtml(project.name)}</h2>
            <div class="project-indicator" style="background-color: ${project.color}"></div>
        </div>
        
        <p class="project-description">${escapeHtml(project.description)}</p>
        

        <div style="margin-bottom: 5px; font-size: 0.8rem; color: #888;">Time elapsed (real-time):</div>
        <div class="time-display elapsed-time">
            <div class="time-unit">
                <span class="time-value">${elapsed.days}</span>
                <span class="time-label">days</span>
            </div>
            <span class="time-separator">•</span>
            <div class="time-unit">
                <span class="time-value">${String(elapsed.hours).padStart(2, '0')}</span>
                <span class="time-label">h</span>
            </div>
            <span class="time-separator">•</span>
            <div class="time-unit">
                <span class="time-value">${String(elapsed.minutes).padStart(2, '0')}</span>
                <span class="time-label">m</span>
            </div>
            <span class="time-separator">•</span>
            <div class="time-unit">
                <span class="time-value">${String(elapsed.seconds).padStart(2, '0')}</span>
                <span class="time-label">s</span>
            </div>
        </div>
        
        <div style="margin-top: 15px; margin-bottom: 5px; font-size: 0.8rem; color: #888;">Time spent (Pomodoro):</div>
        <div class="time-display spent-time" style="background-color: #2a2a2a;">
            <div class="time-unit">
                <span class="time-value" style="color: #4CAF50;">${spent.days}</span>
                <span class="time-label">days</span>
            </div>
            <span class="time-separator">•</span>
            <div class="time-unit">
                <span class="time-value" style="color: #4CAF50;">${String(spent.hours).padStart(2, '0')}</span>
                <span class="time-label">h</span>
            </div>
            <span class="time-separator">•</span>
            <div class="time-unit">
                <span class="time-value" style="color: #4CAF50;">${String(spent.minutes).padStart(2, '0')}</span>
                <span class="time-label">m</span>
            </div>
            <span class="time-separator">•</span>
            <div class="time-unit">
                <span class="time-value" style="color: #4CAF50;">${String(spent.seconds).padStart(2, '0')}</span>
                <span class="time-label">s</span>
            </div>
        </div>

        
        <div class="progress-bar">
            <div class="progress-fill" style="background-color: ${project.color}; width: 65%;"></div>
        </div>
        
        <div class="project-footer">
            → Open on GitHub
        </div>
    `;
    
    card.addEventListener('click', () => {
        window.open(project.github_url, '_blank');
    });
    
    return card;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function loadProjects() {
    const grid = document.getElementById('projectsGrid');
    const data = await fetchProjects();
    
    grid.innerHTML = '';
    
    if (data.projects && data.projects.length > 0) {
        data.projects.forEach(project => {
            const card = createProjectCard(project);
            grid.appendChild(card);
        });
    } else {
        grid.innerHTML = '<div class="loading">No projects found. Visit the admin panel to create one!</div>';
    }
}

function updateAllTimers() {
    const timeValues = document.querySelectorAll('.elapsed-time .time-value');
    timeValues.forEach(el => {
        const parent = el.closest('.time-unit');
        if (parent) {
            const label = parent.querySelector('.time-label');
            if (label && label.textContent === 's') {
                const currentValue = parseInt(el.textContent);
                const newValue = (currentValue + 1) % 60;
                el.textContent = String(newValue).padStart(2, '0');
                
                if (newValue === 0) {
                    const minuteUnit = parent.parentElement.querySelector('.time-unit:nth-child(3)');
                    if (minuteUnit) {
                        const minuteValue = minuteUnit.querySelector('.time-value');
                        const currentMin = parseInt(minuteValue.textContent);
                        const newMin = (currentMin + 1) % 60;
                        minuteValue.textContent = String(newMin).padStart(2, '0');
                        
                        if (newMin === 0) {
                            const hourUnit = parent.parentElement.querySelector('.time-unit:nth-child(5)');
                            if (hourUnit) {
                                const hourValue = hourUnit.querySelector('.time-value');
                                const currentHour = parseInt(hourValue.textContent);
                                const newHour = (currentHour + 1) % 24;
                                hourValue.textContent = String(newHour).padStart(2, '0');
                                
                                if (newHour === 0) {
                                    const dayUnit = parent.parentElement.querySelector('.time-unit:nth-child(1)');
                                    if (dayUnit) {
                                        const dayValue = dayUnit.querySelector('.time-value');
                                        dayValue.textContent = parseInt(dayValue.textContent) + 1;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    loadProjects();
    
    setInterval(updateAllTimers, 1000);
    
    setInterval(loadProjects, 60000);
});
