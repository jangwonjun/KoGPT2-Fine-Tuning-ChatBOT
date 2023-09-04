from flask import Flask, render_template, request
from modules.ai import WonJunAI
import env
app = Flask(__name__)
ai = WonJunAI(env.PT_ROUTE)

contents = [
    "안녕하세요! AbaChat 입니다",
    "새학년, 새학기 모르는 사람들에게 자기소개를 하는것이 귀찮거나, 부끄럽지 않으신가요? 그럴때는 AbaChat을 사용해보세요! AbaChat은 부끄러운 당신을 위한 아바타 자기소개 챗봇입니다. 자신을 소개하는 자리에서 자신 아바타 챗봇 링크를 주고 자신을 소개해 보세요!"
]

@app.route('/')
def main():
    return render_template('index.html', title="AbaChat", contents=contents)

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    try:
        text = request.get_json()
        if value:=text.get('text'):
            value = ai.create_response(value)
            return {'text': value}
    except Exception as e:
        print(e)
        return render_template('chatbot.html', title='AbaChat')



if __name__ == '__main__':
    app.run('0.0.0.0', debug = True, port=8000)
