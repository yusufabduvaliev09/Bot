from flask import Flask, render_template_string, request, redirect
import telebot
import random

BOT_TOKEN = "8144352720:AAEoGHZv9ngCzwQqeEo_OdnuA-BfMtsEtZM"  # вставь свой токен
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)

# HTML страница регистрации
html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Регистрация Abu Cargo</title>
    <style>
        body { font-family: Arial; background:#f5f5f5; padding:30px; }
        .box { background:white; padding:20px; border-radius:10px; max-width:400px; margin:auto; box-shadow:0 0 10px #ccc; }
        input, select { width:100%; padding:10px; margin:10px 0; border:1px solid #ddd; border-radius:5px; }
        button { background:#0088cc; color:white; border:none; padding:10px; width:100%; border-radius:5px; }
    </style>
</head>
<body>
<div class="box">
    <h2>Регистрация Abu Cargo</h2>
    <form action="/register" method="post">
        <input name="fio" placeholder="Введите ФИО" required>
        <input name="phone" placeholder="Введите номер телефона" required>
        <label>Выберите ПВЗ:</label>
        <select name="pvz" required>
            <option>ПВЗ №1 — Бишкек</option>
            <option>ПВЗ №2 — Ош</option>
            <option>ПВЗ №3 — Джалал-Абад</option>
        </select>
        <button type="submit">Регистрация</button>
    </form>
</div>
</body>
</html>
"""

@app.route('/')
def home():
    return html

@app.route('/register', methods=['POST'])
def register():
    fio = request.form['fio']
    phone = request.form['phone']
    pvz = request.form['pvz']

    # Генерация персонального кода
    code = "YX" + str(random.randint(1000, 9999))

    # Сообщение для пользователя
    message = f"""
🎉 *Регистрация прошла успешно!* 🎉
Спасибо, что подписались 🙏

📃 *Ваш профиль* 📃

🪪 Персональный КОД: `{code}`
👤 ФИО: {fio}
📞 Номер: {phone}
🏡 Адрес: 
📍 ПВЗ: {pvz}
📍 ПВЗ номер: +996550997200
📍 Часы работы: 9:00–18:00

📩 Скопируйте ниже адрес склада в Китае:
御玺{code}
15727306315 
浙江省金华市义乌市北苑街道春晗二区36栋好运国际货运5697库入仓号:御玺{code}
    """

    # Отправляем пользователю в Telegram
    # (замени chat_id на ID менеджера, если хочешь получать копии)
    bot.send_message(8171485600, message, parse_mode="Markdown")

    # Показываем страницу с переходом обратно в Telegram
    return redirect("https://t.me/Abucargo_osh_bot")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
