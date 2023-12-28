from flask import Flask
from flask import url_for, render_template, request, redirect

from collections import Counter
import pandas as pd
from statistics import mean
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

from collections import defaultdict


app = Flask(__name__)


def stats_calc(data):
    number = data.shape[0]  # сколько людей прошло
    ages = round(mean(list(data['age'])), 2) # средний возраст прошедших опрос

    mean_values_list = []
    for column in data.columns.values.tolist()[2:]:
        mean_values_list.append(mean(list(data[column])))

    fig, ax = plt.subplots()
    plt.title('Общая статистика')
    food = ['Чернослив', 'Халва', 'Оливье', 'Холодец', 'Маслины', 'Грибы', 'Печёнка', 'Пицца с ананасами',
            'Томатный сок', 'Чипсы с крабом', 'Чайный гриб', 'Майонез', 'Айран', 'Лакрица', 'Куринные сердечки',
            'Шпинат', 'Сырный соус', 'Кисель', 'Квашеная капуста', 'Брокколи']
    ax.bar(food, mean_values_list, color="r")
    plt.xticks(rotation=90)
    plt.tight_layout()
    fig.savefig('static/img/my_plot.png')

    holodets = list(zip(data['age'], data['holod']))
    sorted_holodets = sorted(holodets, key=lambda tup: tup[0])
    output = defaultdict(int)
    number_of_appearances = Counter(p[0] for p in sorted_holodets)
    for k, v in sorted_holodets:
        output[k] += v / number_of_appearances[k]
    sorted_holodets_without_rep = list(output.items())

    fig, ax = plt.subplots()
    plt.title('Динамика в оценке холодца')
    plt.plot(*zip(*sorted_holodets_without_rep))
    plt.xlabel('Возраст')
    fig.savefig('static/img/my_plot_holodets.png')

    masliny = list(zip(data['age'], data['masli']))
    sorted_masliny = sorted(masliny, key=lambda tup: tup[0])
    output = defaultdict(int)
    number_of_appearances = Counter(p[0] for p in sorted_masliny)
    for k, v in sorted_masliny:
        output[k] += v / number_of_appearances[k]
    sorted_masliny_without_rep = list(output.items())

    fig, ax = plt.subplots()
    plt.title('Динамика в оценке маслин')
    plt.plot(*zip(*sorted_masliny_without_rep))
    plt.xlabel('Возраст')
    fig.savefig('static/img/my_plot_masliny.png')

    return number, ages


@app.route('/')
@app.route('/enter')
def enter():
    return render_template("enter.html")


@app.route('/info')
def info():
    return render_template("info.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route("/process_results", methods=["get"])
def process_results():
    if not request.args:
        return redirect(url_for("questionnaire"))
    gender = request.args.get("gender")
    age = request.args.get("age")

    chern = request.args.get("chern")
    halva = request.args.get("halva")
    salat = request.args.get("salat")
    holod = request.args.get("holod")
    masli = request.args.get("masli")
    griby = request.args.get("griby")
    peche = request.args.get("peche")
    pizza = request.args.get("pizza")
    tomat = request.args.get("tomat")
    chips = request.args.get("chips")
    chayn = request.args.get("chayn")
    mayon = request.args.get("mayon")
    ayran = request.args.get("ayran")
    lakri = request.args.get("lakri")
    kurin = request.args.get("kurin")
    shpin = request.args.get("shpin")
    syrny = request.args.get("syrny")
    kisel = request.args.get("kisel")
    kvash = request.args.get("kvash")
    brocc = request.args.get("brocc")

    df = pd.DataFrame(columns=['Возраст', 'Гендер', 'Чернослив', 'Халва', 'Оливье', 'Холодец', 'Маслины', 'Грибы',
                               'Печёнка', 'Пицца с ананасами', 'Томатный сок', 'Чипсы с крабом', 'Чайный гриб',
                               'Майонез', 'Айран', 'Лакрица', 'Куринные сердечки', 'Шпинат', 'Молочная пенка',
                               'Кисель', 'Квашеная капуста', 'Брокколи'])
    df.loc[len(df.index)] = [gender, age, chern, halva, salat, holod, masli, griby, peche, pizza, tomat, chips,
                             chayn, mayon, ayran, lakri, kurin, shpin, syrny, kisel, kvash, brocc]
    df.to_csv('data.csv', mode='a', header=False, index=False)
    return render_template("process_results.html")


@app.route("/questionnaire")
def questionnaire():
    return render_template("questionnaire.html")


@app.route('/stats')
def stats():
    data = pd.read_csv('data.csv')
    data_to_show = stats_calc(data)
    return render_template("stats.html", stats=data_to_show)


if __name__ == '__main__':
    app.run(debug=True)
