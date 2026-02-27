const API_URL = 'http://localhost:5000';

async function makePrediction() {
    const data = {
        student_id: document.getElementById('studentId').value,
        'Attendance': parseFloat(document.getElementById('attendance').value),
        'Internal Test 1': parseInt(document.getElementById('test1').value),
        'Internal Test 2': parseInt(document.getElementById('test2').value),
        'Assignment': parseInt(document.getElementById('assignment').value),
        'Study Hours': parseFloat(document.getElementById('studyHours').value)
    };
    
    if (!data.student_id || isNaN(data.Attendance) || isNaN(data['Internal Test 1']) || 
        isNaN(data['Internal Test 2']) || isNaN(data.Assignment) || isNaN(data['Study Hours'])) {
        alert('⚠️ Please fill all fields correctly');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayResults(result.prediction);
            loadStatistics();
        } else {
            alert('❌ Error: ' + result.error);
        }
    } catch (error) {
        alert('❌ Cannot connect to AI server. Make sure backend is running on port 5000');
        console.error(error);
    }
}

function displayResults(prediction) {
    const colors = {
        'Excellent': '#10b981',
        'Good': '#3b82f6',
        'Average': '#f59e0b',
        'Poor': '#ef4444'
    };
    
    const color = colors[prediction.category];
    
    const html = `
        <div class="result-display">
            <div class="score-circle" style="background: ${color}">
                ${prediction.predicted_score}
            </div>
            <div class="category" style="color: ${color}">
                ${prediction.category} Performance
            </div>
            <div class="confidence-badge" style="background: ${color}20; color: ${color}">
                ${prediction.confidence} Confidence
            </div>
            
            <div class="contributions">
                <h3>🧠 AI Feature Analysis:</h3>
                <div class="contribution-item">
                    <span>📚 Attendance Impact:</span>
                    <strong>${prediction.contributions.attendance}%</strong>
                </div>
                <div class="contribution-item">
                    <span>📝 Tests Impact:</span>
                    <strong>${prediction.contributions.tests}%</strong>
                </div>
                <div class="contribution-item">
                    <span>✍️ Assignment Impact:</span>
                    <strong>${prediction.contributions.assignment}%</strong>
                </div>
                <div class="contribution-item">
                    <span>⏰ Study Hours Impact:</span>
                    <strong>${prediction.contributions.study_hours}%</strong>
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('results').innerHTML = html;
}

async function loadStatistics() {
    try {
        const response = await fetch(`${API_URL}/statistics`);
        const data = await response.json();
        
        if (data.success) {
            const stats = data.statistics;
            let html = `
                <div class="stat-card">
                    <div class="stat-value">${stats.total}</div>
                    <div class="stat-label">Total AI Predictions</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.average_score}</div>
                    <div class="stat-label">Average Predicted Score</div>
                </div>
            `;
            
            Object.entries(stats.by_category).forEach(([cat, count]) => {
                html += `
                    <div class="stat-card">
                        <div class="stat-value">${count}</div>
                        <div class="stat-label">${cat}</div>
                    </div>
                `;
            });
            
            document.getElementById('statistics').innerHTML = html;
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

window.onload = loadStatistics;