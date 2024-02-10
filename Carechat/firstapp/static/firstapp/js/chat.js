// chat.js
document.addEventListener('DOMContentLoaded', function() {
    // 'いいね'ボタンにクリックイベントリスナーを追加
    document.querySelectorAll('.like-button').forEach(button => {
        button.onclick = function() {
            const messageId = this.dataset.messageId; // メッセージIDを取得
            // AJAXを使ってサーバーに'いいね'リクエストを送る
            fetch(`/like/${messageId}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // CSRFトークンを取得してヘッダーに追加
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // いいねの総数を更新
                    const likesElement = button.nextElementSibling;
                    likesElement.textContent = data.likes;
                }
            });
        };
    });
});

// DjangoのCSRFトークンを取得するためのヘルパー関数
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // このCookieの名前がリクエストされたものと一致するかどうかをチェック
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
