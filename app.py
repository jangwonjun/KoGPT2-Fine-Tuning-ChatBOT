from flask import Flask, render_template, request
from modules.ai import WonJunAI
app = Flask(__name__)
ai = WonJunAI()

contents = [
    "이곳에서 챗봇을 체험해보세요!",
    "누구나 무료로 사용할 수 있습니다!",
    "어머나~ 이건 꼭 해야 해!"
]

@app.route('/')
def main():
    return render_template('index.html', title="IntroM", contents=contents)

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    try:
        text = request.get_json()
        if value:=text.get('text'):
            value = ai.create_response(value)
            return {'text': value}
    except Exception as e:
        print(e)
        return render_template('chatbot.html', title='IntroM')



if __name__ == '__main__':
    app.run('0.0.0.0', port=8000)
