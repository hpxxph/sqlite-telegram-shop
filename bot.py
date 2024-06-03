import telebot
from telebot import types
from database import get_users, get_categories, get_products, create_order, add_review, apply_discount, initialize_database
from config import API_TOKEN

bot = telebot.TeleBot(API_TOKEN)

initialize_database()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Show users", callback_data='show_users'))
    markup.add(types.InlineKeyboardButton("Show categories", callback_data='show_categories'))
    markup.add(types.InlineKeyboardButton("Show products", callback_data='show_products'))
    markup.add(types.InlineKeyboardButton("Create order", callback_data='create_order'))
    markup.add(types.InlineKeyboardButton("Add review", callback_data='add_review'))
    markup.add(types.InlineKeyboardButton("Apply discount", callback_data='apply_discount'))
    bot.send_message(message.chat.id, "Welcome to the store! Choose an action:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'show_users':
        users = get_users()
        response = "Users:\n" + "\n".join([f"{user[0]}: {user[1]}, {user[2]}" for user in users])
        bot.send_message(call.message.chat.id, response)

    elif call.data == 'show_categories':
        categories = get_categories()
        response = "Categories:\n" + "\n".join([f"{category[0]}: {category[1]}" for category in categories])
        bot.send_message(call.message.chat.id, response)

    elif call.data == 'show_products':
        products = get_products()
        response = "Products:\n" + "\n".join([f"{product[0]}: {product[1]}, Цена: {product[2]}, В наличии: {product[3]}" for product in products])
        bot.send_message(call.message.chat.id, response)

    elif call.data == 'create_order':
        msg = bot.send_message(call.message.chat.id, "Enter the user ID, product ID and quantity (for example: 1,1,2 for 2 units of product 1 from user 1):")
        bot.register_next_step_handler(msg, process_order_step)

    elif call.data == 'add_review':
        msg = bot.send_message(call.message.chat.id, "Enter your user ID, product ID, rating and comment (for example: 1,1,5,Great product!):")
        bot.register_next_step_handler(msg, process_review_step)

    elif call.data == 'apply_discount':
        msg = bot.send_message(call.message.chat.id, "Enter the product ID, discount percentage, start date and end date (for example: 10/1/2024-01-01,2024-01-31):")
        bot.register_next_step_handler(msg, process_discount_step)

def process_order_step(message):
    try:
        data = message.text.split(',')
        user_id = int(data[0])
        items = [(int(data[i]), int(data[i+1])) for i in range(1, len(data), 2)]
        delivery_address = "123 mmain St"  
        create_order(user_id, items, delivery_address)
        bot.send_message(message.chat.id, "The order has been created!")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

def process_review_step(message):
    try:
        data = message.text.split(',')
        user_id = int(data[0])
        product_id = int(data[1])
        rating = int(data[2])
        comment = data[3]
        add_review(user_id, product_id, rating, comment)
        bot.send_message(message.chat.id, "Discount applied!")
    except Exception as e:
         bot.send_message(message.chat.id, f"Error: {e}")

def process_discount_step(message):
    try:
        data = message.text.split(',')
        product_id = int(data[0])
        discount_percentage = float(data[1])
        start_date = data[2]
        end_date = data[3]
        apply_discount(product_id, discount_percentage, start_date, end_date)
        bot.send_message(message.chat.id, "Discount applied!")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

if __name__ == "__main__":
    bot.polling()
