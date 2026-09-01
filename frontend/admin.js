const API_BASE = '/api/projects';
let currentEditId = null;

async function fetchProjects() {
    try {
        const response = await fetch(`${API_BASE}/`);
        if (!response.ok) throw new Error('Failed to fetch projects');
        return await response.json();
    } catch (error) {
        console.error('Error fetching projects:', error);
        showAlert('Failed to load projects', 'error');
        return { projects: [], total: 0 };
    }
}

async function createProject(data) {
    try {
        const response = await fetch(`${API_BASE}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error('Failed to create project');
        showAlert('Project created successfully', 'success');
        return await response.json();
    } catch (error) {
        console.error('Error creating project:', error);
        showAlert('Failed to create project', 'error');
        return null;
    }
}

async function updateProject(id, data) {
    try {
        const response = await fetch(`${API_BASE}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error('Failed to update project');
        showAlert('Project updated successfully', 'success');
        return await response.json();
    } catch (error) {
        console.error('Error updating project:', error);
        showAlert('Failed to update project', 'error');
        return null;
    }
}

async function deleteProject(id) {
    if (!confirm('Are you sure you want to delete this project?')) return;
    
    try {
        const response = await fetch(`${API_BASE}/${id}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Failed to delete project');
        showAlert('Project deleted successfully', 'success');
        loadProjects();
    } catch (error) {
        console.error('Error deleting project:', error);
        showAlert('Failed to delete project', 'error');
    }
}

async function changeStatus(id, status) {
    try {
        const response = await fetch(`${API_BASE}/${id}/status`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status })
        });
        if (!response.ok) throw new Error('Failed to change status');
        showAlert('Status updated successfully', 'success');
        loadProjects();
    } catch (error) {
        console.error('Error changing status:', error);
        showAlert('Failed to change status', 'error');
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function loadProjects() {
    const tbody = document.getElementById('projectsBody');
    const data = await fetchProjects();
    
    if (!data.projects || data.projects.length === 0) {
        tbody.innerHTML = '<tr class="loading-row"><td colspan="6">No projects yet. Create one to get started!</td></tr>';
        return;
    }
    
    tbody.innerHTML = data.projects.map(project => `
        <tr>
            <td>${escapeHtml(project.name)}</td>
            <td>${escapeHtml(project.description || '-')}</td>
            <td><a href="${project.github_url}" target="_blank" style="color: var(--primary); text-decoration: none;">GitHub →</a></td>
            <td>
                <select class="status-select" data-id="${project.id}" value="${project.status}">
                    <option value="active">Active</option>
                    <option value="paused">Paused</option>
                    <option value="completed">Completed</option>
                    <option value="archived">Archived</option>
                </select>
            </td>
            <td>
                <div style="width: 30px; height: 30px; background-color: ${project.color}; border-radius: 6px;"></div>
            </td>
            <td>
                <div class="actions">
                    <button class="btn btn-sm btn-primary" onclick="openPomodoro(${project.id}, \`${escapeHtml(project.name)}\`)">Pomodoro</button>
                    <button class="btn btn-sm btn-secondary" onclick="editProject(${project.id})">Edit</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteProject(${project.id})">Delete</button>
                </div>
            </td>
        </tr>
    `).join('');
    
    document.querySelectorAll('.status-select').forEach(select => {
        select.addEventListener('change', async (e) => {
            const id = parseInt(e.target.dataset.id);
            const status = e.target.value;
            await changeStatus(id, status);
        });
    });
}

function editProject(id) {
    const tbody = document.getElementById('projectsBody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const row = rows.find(r => r.querySelector(`[data-id="${id}"]`) || 
        Array.from(r.querySelectorAll('button')).some(btn => btn.textContent.includes('Edit') && btn.onclick.toString().includes(id)));
    
    if (!row) return;
    
    const cells = row.querySelectorAll('td');
    const name = cells[0].textContent;
    const description = cells[1].textContent === '-' ? '' : cells[1].textContent;
    const github = cells[2].querySelector('a')?.href || '';
    
    currentEditId = id;
    document.getElementById('editId').value = id;
    document.getElementById('editName').value = name;
    document.getElementById('editDescription').value = description;
    document.getElementById('editGithubUrl').value = github;
    
    const modal = document.getElementById('editModal');
    modal.style.display = 'flex';
}

function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.admin-content') || document.querySelector('.admin-container');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => alertDiv.remove(), 3000);
}

document.addEventListener('DOMContentLoaded', () => {
    loadProjects();
    
    document.getElementById('createForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData);
        
        if (!data.name.trim() || !data.github_url.trim()) {
            showAlert('Please fill in required fields', 'error');
            return;
        }
        
        const project = await createProject(data);
        if (project) {
            e.target.reset();
            loadProjects();
        }
    });
    
    document.getElementById('editForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData);
        delete data.id;
        
        const project = await updateProject(currentEditId, data);
        if (project) {
            document.getElementById('editModal').style.display = 'none';
            loadProjects();
        }
    });
    
    const modal = document.getElementById('editModal');
    const closeBtn = modal.querySelector('.close');
    const cancelBtn = document.getElementById('cancelBtn');
    
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });
    
    cancelBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });
    
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    document.getElementById('color').addEventListener('input', (e) => {
        document.getElementById('colorValue').textContent = e.target.value;
    });
    
    document.getElementById('editColor').addEventListener('input', (e) => {
        document.getElementById('editColorValue').textContent = e.target.value;
    });
});


async function exportProjects() {
    try {
        const response = await fetch(`${API_BASE}/export/all`);
        if (!response.ok) throw new Error('Failed to export projects');
        const data = await response.json();
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data, null, 2));
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", "projects_backup.json");
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
    } catch (error) {
        console.error('Error exporting projects:', error);
        showAlert('Failed to export projects', 'error');
    }
}

async function importProjects(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async (e) => {
        try {
            const projects = JSON.parse(e.target.result);
            const response = await fetch(`${API_BASE}/import/all`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(projects)
            });
            if (!response.ok) throw new Error('Failed to import projects');
            const result = await response.json();
            showAlert(`Successfully imported ${result.imported} projects`, 'success');
            loadProjects();
        } catch (error) {
            console.error('Error importing projects:', error);
            showAlert('Failed to import projects. Invalid JSON or server error.', 'error');
        }
        event.target.value = '';
    };
    reader.readAsText(file);
}

let pomodoroInterval;
let pomodoroTimeLeft = 25 * 60;
let pomodoroTimeSpent = 0;
let currentPomodoroProjectId = null;

function openPomodoro(projectId, projectName) {
    currentPomodoroProjectId = projectId;
    document.getElementById('pomodoroProjectName').textContent = projectName;
    pomodoroTimeLeft = 25 * 60;
    pomodoroTimeSpent = 0;
    updatePomodoroDisplay();
    document.getElementById('pomodoroModal').style.display = 'flex';
    document.getElementById('startPomodoroBtn').style.display = 'inline-block';
    document.getElementById('pausePomodoroBtn').style.display = 'none';
}

function updatePomodoroDisplay() {
    const m = Math.floor(pomodoroTimeLeft / 60);
    const s = pomodoroTimeLeft % 60;
    document.getElementById('pomodoroTimer').textContent = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('startPomodoroBtn').addEventListener('click', () => {
        document.getElementById('startPomodoroBtn').style.display = 'none';
        document.getElementById('pausePomodoroBtn').style.display = 'inline-block';
        pomodoroInterval = setInterval(() => {
            if (pomodoroTimeLeft > 0) {
                pomodoroTimeLeft--;
                pomodoroTimeSpent++;
                updatePomodoroDisplay();
            } else {
                clearInterval(pomodoroInterval);
                alert("Pomodoro finished!");
            }
        }, 1000);
    });

    document.getElementById('pausePomodoroBtn').addEventListener('click', () => {
        clearInterval(pomodoroInterval);
        document.getElementById('startPomodoroBtn').style.display = 'inline-block';
        document.getElementById('pausePomodoroBtn').style.display = 'none';
    });

    document.getElementById('stopPomodoroBtn').addEventListener('click', async () => {
        clearInterval(pomodoroInterval);
        if (pomodoroTimeSpent > 0) {
            try {
                const response = await fetch(`${API_BASE}/${currentPomodoroProjectId}/spent-time`, {
                    method: 'PATCH',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ seconds: pomodoroTimeSpent })
                });
                if (!response.ok) throw new Error('Failed to save time');
                showAlert(`Saved ${pomodoroTimeSpent} seconds!`, 'success');
                loadProjects();
            } catch (e) {
                console.error(e);
                showAlert('Failed to save time', 'error');
            }
        }
        document.getElementById('pomodoroModal').style.display = 'none';
    });

    document.getElementById('closePomodoro').addEventListener('click', () => {
        clearInterval(pomodoroInterval);
        document.getElementById('pomodoroModal').style.display = 'none';
    });
});
