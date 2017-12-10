# Kolbeinn Ingólfsson
# 10.12.2017
# Verkefni 12 - VEF

from bottle import *
from pymysql import *
from beaker.middleware import SessionMiddleware
from sys import argv


"""
1 Free hosting: manneskja hostar síðu ókeypis
2 Shared hosting: Margar síður eru á einum server
3 Virtual hosting: Það er hostað mörg domain á einum server og geta skipts á
4 Dedicated hosting: Notandi fær server og getur stjórnað honum með mikið fleiri úrræðum
5 Collocated hosting: Þú leigir pláss fyrir server
6 Ecommerce hosting: Vef hostinn býður upp á tól til að hjálpa að setja upp og hýsa vefsíðuna


1. Það er gott að skrá notendurnar með lykilorðum og notendanafni svo þeir geta skráð sig inn. Einnig hjálpar að vera með e-mail notenda

2. Hún að lýta vel út gg þarf að hafa einfalt nafn svo sé létt að muna eftir henni, vefsíðan þarf að vera einföld og "fool-proof" svo það veldur ekki pirring við notkun
"""

db = Connect(host="tsuts.tskoli.is", user="0908002640", password="mypassword", db="0908002640_vef2verk12")
cursor = db.cursor()
cursor.execute("select * from vorur")
numrows = int(cursor.rowcount)
vorur = {}
karfa = []
asd = []

for x in range(numrows):
    row = cursor.fetchone()
    asd.append(row)


@error(404)
def index():
    return "Villa, síða ekki til"

@error(500)
def index():
    return "Villa"


@route('/static/<filepath>')
def static(filepath):
    return static_file(filepath, root='./static')

@route('/static/css/<filepath>')
def static(filepath):
    return static_file(filepath, root='./static/css')

sess = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(app(), sess)




@route('/')
def index():
    s = request.environ.get('beaker.session')
    s['test'] = s.get('test', 0) + 1
    s.save()
    return template('index.tpl', asd=asd, teljari=s['test'])

@route('/karfa')
def karfan():
    session = request.environ.get('beaker.session')
    verdK = 0
    karfa = []
    for x in range(numrows+1):
        if session.get(x):
            vara = session.get(x)
            karfa.append(vara)
    for x in karfa:
        for i in range(len(asd)):
            if x == asd[i][1]:
                verdK += asd[i][2]

    return template('karfa.tpl', karfa=karfa, verd=verdK)

@route('/karfa/baeta/<id:int>')
def baeta_i_korfu(id):
    for x in range(len(asd)):
        """if id == x:
            print("asd")
            session = request.environ.get('beaker.session')
            session[id] = 'Vara '+str(id)
            session.save()
            return redirect('/karfa')"""

        if id in asd[x]:
            session = request.environ.get('beaker.session')
            session[x] = asd[x][1]
            session.save()
            return redirect('/')


@route('/karfa/eyda')
def eyda_ur_korfu():
    session = request.environ.get('beaker.session')
    session.delete()
    global verdK
    verdK = 0
    return redirect('/karfa')


@route("/karfa/<name>")
def index(name):
    flag = True
    session = request.environ.get('beaker.session')
    karfa = []
    for x in range(numrows + 1):
        if session.get(x):
            vara = session.get(x)
            karfa.append(vara)
    if name in karfa:
        for x in asd:
            if name == x[1]:
                flag = True
                global u
                u = str(x[3]).replace("\r", "").split("\n")
                global a
                a = x[1]
                break
            else:
                flag = False
    else:
        flag = False
    if not flag:
        return redirect("/")

    return template("uppl", a=a, u=u)


run(host="0.0.0.0", port=argv[1], app=app)

