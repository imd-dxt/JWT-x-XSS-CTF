fetch('/api/profile/')
    .then(response => response.json())
    .then(data => {
        document.getElementById('username').textContent = data.username;
        document.getElementById('welcomeUsername').textContent = data.username;
        document.getElementById('userRole').textContent = data.role;
        document.getElementById('profileUsername').textContent = data.username;
        document.getElementById('profileEmail').textContent = data.email || 'admin@secops.example';
        document.getElementById('profileRole').textContent = data.role === 'admin' ? 'System Administrator' : data.role;
        
        
        if (data.role !== 'admin') {
            alert('Admin access required!');
            window.location.href = '/dashboard/';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        window.location.href = '/';
    });


const sidebarLinks = document.querySelectorAll('.sidebar-link[data-section]');
const sections = document.querySelectorAll('.dashboard-section, .reports-section, .messages-section, .settings-section');

sidebarLinks.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        
        
        sidebarLinks.forEach(l => l.classList.remove('active'));
        sections.forEach(s => s.classList.remove('active-section'));
        
        
        this.classList.add('active');
        const sectionId = this.dataset.section + 'Section';
        document.getElementById(sectionId).classList.add('active-section');
        
        
        if (sectionId === 'messagesSection') {
            loadMessages();
        }
    });
});


document.getElementById('profileLink').addEventListener('click', function(e) {
    e.preventDefault();
    
    sidebarLinks.forEach(l => l.classList.remove('active'));
    sections.forEach(s => s.classList.remove('active-section'));
    
    
    document.querySelector('.sidebar-link[data-section="settings"]').classList.add('active');
    document.getElementById('settingsSection').classList.add('active-section');
});


function loadMessages() {
    fetch('/api/admin/messages/')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('messagesContainer');
            container.innerHTML = ''; // Clear container
            
            
            data.messages.forEach(message => {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message-box ${message.author === 'Admin' ? 'admin-message' : 'user-message'}`;
                
               
                messageDiv.innerHTML = `<strong>${message.author}:</strong><br>
                                      <div>${message.content}</div>
                                      <small class="text-muted mt-1">${message.timestamp || 'Just now'}</small>`;
                
                container.appendChild(messageDiv);
            });
            
            
            if (data.secretFlag) {
                alert(`Flag: ${data.secretFlag}`);
            }
        })
        .catch(error => console.error('Error loading messages:', error));
}


document.getElementById('sendMessage').addEventListener('click', function() {
    const messageInput = document.getElementById('messageInput');
    const authorInput = document.getElementById('authorInput');
    
    if (!messageInput.value.trim()) {
        alert('Please enter a message!');
        return;
    }
    
    const author = authorInput.value.trim() || 'User';
    
    fetch('/api/admin/messages/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            author: author,
            message: messageInput.value
        }),
    })
    .then(response => response.json())
    .then(data => {
        
        messageInput.value = '';
        authorInput.value = '';
        
        
        if (data.secretFlag) {
            alert(`Flag: ${data.secretFlag}`);
        }
        
        
        loadMessages();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to send message!');
    });
});


document.getElementById('logoutBtn').addEventListener('click', function() {
    document.cookie = 'access_token=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    window.location.href = '/';
});

document.getElementById('logoutBtnSettings').addEventListener('click', function() {
    document.cookie = 'access_token=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    window.location.href = '/';
});

if (document.getElementById('messagesSection').classList.contains('active-section')) {
    loadMessages();
}

const dummyMessages = [
    {
        author: 'Admin',
        content: 'Welcome to the internal messaging system. Please remember to follow security protocols when sharing sensitive information.',
        timestamp: 'Today at 08:30 AM'
    },
    {
        author: 'Security_Analyst',
        content: 'New vulnerability found in our third-party payment processor. Details in the latest security report.',
        timestamp: 'Today at 09:15 AM'
    },
    {
        author: 'System',
        content: 'Scheduled maintenance will occur tonight at 2:00 AM. Expect 30 minutes of downtime.',
        timestamp: 'Yesterday at 04:45 PM'
    }
];