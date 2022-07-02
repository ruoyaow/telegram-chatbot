import random

import requests
from flask import Flask
from flask import request
from flask import Response

from typing import Optional

from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config

import time
import json

import sqlite3

# Open connection to DB
conn = sqlite3.connect('food.db')

# Create a cursor
c = conn.cursor()
# drop table
c.execute("DROP TABLE IF EXISTS foods")
# create foods table
c.execute(
    "CREATE TABLE IF NOT EXISTS foods(name varchar(50), price float, energy float, fat float,carbon float, protein float, sweet int, spicy int, drinks int)")
# insert food data including name, price, energy, fat, carbon, protein, sweet, spicy, drinks
c.execute(
    "INSERT INTO foods (name, price, energy, fat, carbon, protein, sweet, spicy, drinks) VALUES ('Hotdog', 4, 250, 15, 18.4, 10.6, 0, 0, 0);")
c.execute(
    "INSERT INTO foods (name, price, energy, fat, carbon, protein, sweet, spicy, drinks) VALUES ('Tuna Sandwich', 8, 272, 10, 35, 11.5, 0, 0, 0);")
c.execute(
    "INSERT INTO foods (name, price, energy, fat, carbon, protein, sweet, spicy, drinks) VALUES ('Ham and Cheese Sandwich', 12, 224, 9, 25, 10.5, 0, 0, 0);")
c.execute(
    "INSERT INTO foods (name, price, energy, fat, carbon, protein, sweet, spicy, drinks) VALUES ('Chicken curry', 6, 70, 3.5, 5, 5, 0, 1, 0);")
c.execute(
    "INSERT INTO foods (name, price, energy, fat, carbon, protein, sweet, spicy, drinks) VALUES ('Vegetable salad', 2, 39, 1.4, 6, 1, 0, 0, 0);")
c.execute(
    "INSERT INTO foods (name, price, energy, fat, carbon, protein, sweet, spicy, drinks) VALUES ('Turkey', 12, 115, 2, 0.2, 23, 0, 0, 0);")
c.execute(
    "INSERT INTO foods (name, price, energy, fat, carbon, protein, sweet, spicy, drinks) VALUES ('Hot chocolate', 3, 20, 21, 9, 3, 1, 0, 1);")
c.execute(
    "INSERT INTO foods (name, price, energy, fat, carbon, protein, sweet, spicy, drinks) VALUES ('Lemon Cheesecake', 7, 264, 10, 30, 12.5, 1, 0, 0);")
c.execute(
    "INSERT INTO foods (name, price, energy, fat, carbon, protein, sweet, spicy, drinks) VALUES ('Egg tart', 1, 376, 21, 41, 4, 1, 0, 0);")
c.execute(
    "INSERT INTO foods (name, price, energy, fat, carbon, protein, sweet, spicy, drinks) VALUES ('Donut', 2, 365, 20, 40, 6.5, 1, 0, 0);")
c.execute(
    "INSERT INTO foods (name, price, energy, fat, carbon, protein, sweet, spicy, drinks) VALUES ('Chocolate Pie', 8, 425, 18, 70, 4.5, 1, 0, 0);")
c.execute(
    "INSERT INTO foods (name, price, energy, fat, carbon, protein, sweet, spicy, drinks) VALUES ('Tomato Pasta', 8, 141, 3.8, 24, 4, 0, 0, 0);")
c.execute(
    "INSERT INTO foods (name, price, energy, fat, carbon, protein, sweet, spicy, drinks) VALUES ('Caramel Latte', 3, 17, 0, 0.5, 0.3, 1, 0, 1);")
c.execute(
    "INSERT INTO foods (name, price, energy, fat, carbon, protein, sweet, spicy, drinks) VALUES ('latte', 4, 14, 3, 4.5, 3.1, 0, 0, 1);")
c.execute(
    "INSERT INTO foods (name, price, energy, fat, carbon, protein, sweet, spicy, drinks) VALUES ('Cappuccino', 4, 13, 1.8, 3, 2, 0, 0, 1);")
c.execute(
    "INSERT INTO foods (name, price, energy, fat, carbon, protein, sweet, spicy, drinks) VALUES ('Cola', 1, 15, 0, 3.5, 0, 1, 0, 1);")
c.execute(
    "INSERT INTO foods (name, price, energy, fat, carbon, protein, sweet, spicy, drinks) VALUES ('Milk', 2, 16, 5, 5.3, 4, 0, 0, 1);")
c.execute(
    "INSERT INTO foods (name, price, energy, fat, carbon, protein, sweet, spicy, drinks) VALUES ('Steak Wellington', 18, 286, 20.5, 19, 7, 0, 0, 0);")
c.execute(
    "INSERT INTO foods (name, price, energy, fat, carbon, protein, sweet, spicy, drinks) VALUES ('Beef Pizza', 13, 249, 13, 21, 11, 0, 0, 0);")
c.execute(
    "INSERT INTO foods (name, price, energy, fat, carbon, protein, sweet, spicy, drinks) VALUES ('Hawaiian Pizza', 10, 279, 9, 36, 13, 0, 0, 0);")
c.execute(
    "INSERT INTO foods (name, price, energy, fat, carbon, protein, sweet, spicy, drinks) VALUES ('Cream of Mushroom Soup', 8, 154, 13, 6, 3, 0, 0, 1);")
# commit to database
c.execute("commit")

# Create a trainer that uses this config
trainer = Trainer(config.load("config_spacy.yml"))
training_data = load_data('food-rasa.json')
interpreter = trainer.train(training_data)

# rule of conditions
condition_rules = {
    ('type', 'food'): "drinks=0",
    ('type', 'drinks'): "drinks=1",
    ('energy', 'high'): "energy>90",
    ('energy', 'low'): "energy<=90",
    ('sweet', '1'): "sweet=1",
    ('sweet', '0'): "sweet=0",
    ('fat', 'high'): "fat>15",
    ('fat', 'low'): "fat<=15",
    ('price', 'high'): "price>5",
    ('price', 'low'): "price<=5",
    ('spicy', '1'): "sweet=1",
    ('spicy', '0'): "sweet=0",
    ('protein', '1'): "protein=1",
    ('protein', '0'): "protein=0",
    ('carbon', '1'): "carbon>20",
    ('carbon', '0'): "carbon<=20",
}


class Food:
    def __init__(self, name, price, energy, fat, carbon, protein, sweet, spicy, drinks) -> None:
        super().__init__()
        self.name = name
        self.price = price
        self.energy = energy
        self.fat = fat
        self.carbon = carbon
        self.protein = protein
        self.sweet = sweet
        self.spicy = spicy
        self.drinks = drinks

    def __str__(self) -> str:
        flavors = []
        if self.sweet:
            flavors.append('sweet')
        if self.spicy:
            flavors.append('spicy')
        if flavors:
            return f'{self.name}({",".join(flavors)}) ${self.price:.2f} (Energy: {self.energy}, ' \
                   f'Fat: {self.fat}, Carbon: {self.carbon}, Protein: {self.protein})'
        else:
            return f'{self.name} ${self.price:.2f} (Energy: {self.energy}, Fat: {self.fat}, ' \
                   f'Carbon: {self.carbon}, Protein: {self.protein})'

    def __repr__(self) -> str:
        return str(self)


def find_food(conditions):
    wheresql = ' AND '.join(conditions)
    if len(conditions) > 0:
        sql = f'select * from foods where {wheresql}'
    else:
        sql = 'select * from foods'
    conn = sqlite3.connect("food.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    foods = []
    for item in cursor.fetchall():
        food = Food(*item)
        foods.append(food)
    return foods


def find_food_build_condition(params):
    conditions = []
    if params:
        for k, v in params.items():
            condition_key = (k, v)
            if condition_key in condition_rules:
                condition = condition_rules[condition_key]
                conditions.append(condition)
    return conditions


STATUS_INIT = 0
STATUS_RECOMMEND = 1
STATUS_CHANGE = 2


class Conversation:
    recommend_food: Optional[Food]

    def __init__(self) -> None:
        super().__init__()
        self.recommend_food = None
        self.last_recommend_foods = []
        self.buy_cart = []
        self.payed = False
        self.status = STATUS_INIT

    def reset(self):
        self.recommend_food = None
        self.last_recommend_foods = []
        self.buy_cart = []
        self.payed = False

    def show_bill(self):
        total = 0
        resp = []
        for item in self.buy_cart:
            total += item.price
            resp.append(str(item))
        resp.append(f"Total: {total}")
        return '\n'.join(resp)

    def match_status(self, status, intent):
        if status == STATUS_INIT:
            if intent == 'greet':
                return True
            if intent == 'find_food':
                return True
        elif status == STATUS_RECOMMEND:
            if intent == 'find_food':
                return True
            if intent == 'change':
                return True
            if intent == 'affirm':
                return True
            if intent == 'pay':
                return True
            if intent == 'goodbye':
                return True
        elif status == STATUS_CHANGE:
            if intent == 'find_food':
                return True
            if intent == 'change':
                return True
            if intent == 'affirm':
                return True
            if intent == 'pay':
                return True
            if intent == 'goodbye':
                return True
        return False

    def match_and_response(self, intent, params):
        if not self.match_status(self.status, intent['name']):
            return None
        if intent['name'] == 'find_food':
            self.status = STATUS_RECOMMEND
            if len(params) == 0:
                return 'There are have many food and drink on our menu, can you be more specific?' \
                       ' Maybe some thing to eat or something to drink?'
            else:
                conditions = find_food_build_condition(params)
                foods = find_food(conditions)
                self.last_recommend_foods = foods
                if foods:
                    food = random.choice(foods)
                    self.recommend_food = food
                    return f'what about this: ({food})'
                else:
                    self.recommend_food = None
                    return "There is no such food"
        elif intent['name'] == 'affirm':
            if self.recommend_food is not None:
                self.buy_cart.append(self.recommend_food)
                self.recommend_food = None
                return 'Ok, add it to list!'
            else:
                return "I don't know what you mean."
        elif intent['name'] == 'greet':
            return 'Welcome to our restaurant, we have delicious food and cool drinks, what do you need?'
        elif intent['name'] == 'change':
            self.status = STATUS_CHANGE
            if 'change_price' in params:
                food = self.change_price(params['change_price'])
                if food:
                    self.recommend_food = food
                    return f'what about this: ({self.recommend_food})'
                else:
                    return 'There is no such item!'
        elif intent['name'] == 'pay':
            bill = self.show_bill()
            self.payed = True
            return bill
        elif intent['name'] == 'goodbye':
            self.status = STATUS_INIT
            if self.payed or len(self.buy_cart) == 0:
                self.reset()
                return 'Bye!'
            else:
                self.reset()
                return "Hey, you didn't pay the bill! Security!!!"

    def respond(self, message):
        # Extract the entities
        result = interpreter.parse(message)
        intent = result['intent']
        entities = result["entities"]
        # Initialize an empty params dictionary
        params = {}
        # Fill the dictionary with entities
        for ent in entities:
            params[ent["entity"]] = str(ent["value"])
        if result['intent_ranking']:
            for intent in result['intent_ranking']:
                cur_resp = self.match_and_response(intent, params)
                if cur_resp is not None:
                    return cur_resp
        return "I don't know what you mean."

    def change_price(self, direction):
        if self.recommend_food:
            cur_price = self.recommend_food.price
            if direction == 'low':
                self.last_recommend_foods.sort(key=lambda x: -x.price)
                if self.last_recommend_foods:
                    for food in self.last_recommend_foods:
                        if food.price < cur_price:
                            return food
            elif direction == 'high':
                self.last_recommend_foods.sort(key=lambda x: x.price)
                if self.last_recommend_foods:
                    for food in self.last_recommend_foods:
                        if food.price > cur_price:
                            return food


token = '5035134369:AAEHBhxviOSx2I9qShhlkFfgvdhIkYGRrzU'
app = Flask(__name__)

chat_conversation_dict = {}


def parse_msg(message):
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    return chat_id, txt


def send_message(chat_id, messages=[]):
    url = 'https://api.telegram.org/bot' + token + '/sendMessage'
    if messages:
        for message in messages:
            payload = {'chat_id': chat_id, 'text': message}
            requests.post(url, json=payload)
    return True


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id, message = parse_msg(msg)
        if chat_id not in chat_conversation_dict:
            chat_conversation_dict[chat_id] = Conversation()
        conversation = chat_conversation_dict[chat_id]
        response_messages = [conversation.respond(message)]
        send_message(chat_id, response_messages)
        return Response('ok', status=200)
    else:
        return '<h1>HELLO</h1>'


def get_last_id():
    api = f'https://api.telegram.org/bot{token}/getUpdates'
    r = requests.get(api)
    if r.status_code == 200:
        content = r.content.decode('utf-8')
        resp = json.loads(content)
        if resp['result']:
            last = resp['result'][-1]
            update_id = last['update_id']
            return update_id


def get_next_messages(last_update_id):
    if last_update_id is None:
        r = requests.get(api)
        print(r.status_code)
        if r.status_code == 200:
            content = r.content.decode("utf-8")
            resp = json.loads(content)
            if resp['result']:
                result = []
                for item in resp['result']:
                    if not item['message']['from']['is_bot']:
                        result.append(item)
                last = resp['result'][-1]
                update_id = last['update_id']
                return result, update_id
    else:
        r = requests.get(f"{api}?offset={last_update_id + 1}")
        print(r.status_code)
        if r.status_code == 200:
            content = r.content.decode("utf-8")
            resp = json.loads(content)
            if resp['result']:
                result = []
                for item in resp['result']:
                    if not item['message']['from']['is_bot']:
                        result.append(item)
                last = resp['result'][-1]
                update_id = last['update_id']
                return result, update_id
    return [], last_update_id


if __name__ == '__main__':
    conversation = Conversation()
    msgs = [
        'hi',
        "may i order some delicious food, i'm hungry",
        "recommend me some  high energy food and cheap please",
        "more cheaper please",
        "ok",
        "and give me a cup of drink",
        "more expensive please",
        "ok",
        "show me the bill",
        "byebye",
    ]
    for msg in msgs:
        print(f'User: {msg}')
        ans = conversation.respond(msg)
        print(f'Bot: {ans}')

    api = f'https://api.telegram.org/bot{token}/getUpdates'

    last_update_id = get_last_id()

    while True:
        messages, new_update_id = get_next_messages(last_update_id)
        if messages:
            last_update_id = new_update_id
        for item in messages:
            update_id = item['update_id']
            chat_id = item['message']['chat']['id']
            txt = item['message']['text']
            rr = conversation.respond(txt)
            send_message(chat_id, [rr])
        time.sleep(1)
