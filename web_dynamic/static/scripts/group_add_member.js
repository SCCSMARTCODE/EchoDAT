document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    fetch(`/search_user?username=${username}`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('search-results');
            resultsDiv.innerHTML = '';
            if (data.length > 0) {
                data.forEach(user => {
                    const userDiv = document.createElement('div');
                    userDiv.textContent = user.username;
                    const addButton = document.createElement('button');
                    addButton.textContent = 'Add to Group';
                    addButton.addEventListener('click', () => addToGroup(user.id));
                    userDiv.appendChild(addButton);
                    resultsDiv.appendChild(userDiv);
                });
            } else {
                resultsDiv.textContent = 'No users found.';
            }
            resultsDiv.style.display = 'block';
        });
});


function addToGroup(userId) {
    fetch(`/add_to_group`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: userId, group_id: 'your_group_id' })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    });
}
