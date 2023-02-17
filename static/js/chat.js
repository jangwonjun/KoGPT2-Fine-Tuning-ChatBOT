function chat_msg(text) {
    return `
    <div class="col-start-1 col-end-8 p-3 rounded-lg">
        <div class="flex flex-row items-center">
            <div class="flex items-center justify-center h-10 w-10 rounded-full bg-red-500 flex-shrink-0">
            C
            </div>
            <div class="relative ml-3 text-sm bg-white py-2 px-4 shadow rounded-xl">
                <div>
                ${text}
                </div>
            </div>
        </div>
    </div>`;
}

function user_msg(text) {
    return `<div class="col-start-6 col-end-13 p-3 rounded-lg">
    <div class="flex items-center justify-start flex-row-reverse">
      <div class="flex items-center justify-center h-10 w-10 rounded-full bg-indigo-500 flex-shrink-0">
        U
      </div>
      <div class="relative mr-3 text-sm bg-indigo-100 py-2 px-4 shadow rounded-xl">
        <div>${text}</div>
      </div>
    </div>
  </div>`
}
function sendMessage() {
    let text = textField.value;
    if (text !== '') {
        chat.innerHTML += user_msg(text);
        fetch('/chatbot', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 'text': text })
        }).then((response) => {
            return response.json()
        }).then((data) => {
            chat.innerHTML += chat_msg(data.text);
        });
        textField.value = '';
    }
}
let chat = window.document.getElementById('chatTexts');
let submit = window.document.getElementById('send');
let textField = window.document.getElementById('content');
submit.addEventListener('click', () => {
    sendMessage();
});
window.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        sendMessage();
    }
});
chat.innerHTML += chat_msg('안녕하세요! 무엇을 도와드릴까요?');
