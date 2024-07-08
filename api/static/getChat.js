document.getElementById('chat-button').onclick = function() {
            var chatFrame = document.getElementById('chat-container');
            if (chatFrame.style.display === 'none') {
                chatFrame.style.display = 'block';
                chatFrame.innerHTML = '<iframe src="http://localhost:5000" frameborder="0" width="100%" height="100%"></iframe>';
            } else {
                chatFrame.style.display = 'none';
            }
        };