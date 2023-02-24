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

const store = {
    texts: '',
    isRecognizing: true
};

(() => {
    /* Speech API start */
    let SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!("webkitSpeechRecognition" in window)) {
        alert("미지원 브라우저입니다.")
    } else {
        const recognition = new SpeechRecognition();
        recognition.interimResults = true; // true면 음절을 연속적으로 인식하나 false면 한 음절만 기록함
        recognition.lang = 'ko-KR'; // 값이 없으면 HTML의 <html lang="en">을 참고합니다. ko-KR, en-US
        recognition.continuous = false; //각 인식에 대해 연속 결과가 반환되는지 아니면 단일 결과만 반환되는지를 제어합니다. 기본값은 단일( false.)
        recognition.maxAlternatives = 20000; // maxAlternatives가 숫자가 작을수록 발음대로 적고, 크면 문장의 적합도에 따라 알맞은 단어로 대체합니다.

        recognition.onspeechend = function () { // 음성 감지가 끝날때 실행될 이벤트
            recognition.stop();
            $('.dictate').removeClass("on");
            textField.value = store.texts;
            store.isRecognizing = true;
            sendMessage();
        };

        recognition.onresult = function (e) { //result이벤트는 음성 인식 서비스가 결과를 반환할 때 시작됩니다.
            store.texts = Array.from(e.results)
                .map(results => results[0].transcript).join("");

            console.log(store.texts);
            // sendMessage();
        };
        /* // Speech API END */

        const active = () => {
            $('.dictate').addClass('on')
            recognition.start();
            store.isRecognizing = false;
        };

        const unactive = () => {
            $('.dictate').removeClass('on')
            recognition.stop();
            store.isRecognizing = true;
        };

        $('.dictate').on('click', () => {
            if (store.isRecognizing) {
                active();
            } else {
                unactive();
            }
        });
    }
})();