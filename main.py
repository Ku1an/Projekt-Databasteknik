from flask import Flask, render_template,request,redirect,url_for,session,flash
import modules as sql
import mysqlx

app = Flask(__name__)
app.secret_key = "kulan"

@app.before_request
def make_session_permanent():
    session.permanent = False

@app.route("/")
def mainPage():
    return render_template("index.html")


# All coursebooks
@app.route("/databas", methods=["POST","GET"])
def databasPage():
    if request.method == "POST":
    ## Session, save to cart
        flash("Tillagt i varukorg!", "info")
        if "1" in session:
            session["1"] += 1
        else:
            session["1"] = 1

    data = sql.getBook(1)
    return render_template("/productpage/databas.html",produktnamn=data[0],author=data[1],price=data[2],isbn=data[3],coursename=data[4])


@app.route("/datorteknik", methods=["POST","GET"])
def datorteknikPage():
    if request.method == "POST":
    ## Session, save to cart
        flash("Tillagt i varukorg!", "info")
        if "5" in session:
            session["5"] += 1
        else:
            session["5"] = 1

    data = sql.getBook(2)
    return render_template("/productpage/datorteknik.html",produktnamn=data[0],author=data[1],price=data[2],isbn=data[3],coursename=data[4])


@app.route("/endimensionellanalys", methods=["POST","GET"])
def endimensionellPage():
    if request.method == "POST":
    ## Session, save to cart
        flash("Tillagt i varukorg!", "info")
        if "3" in session:
            session["3"] += 1
        else:
            session["3"] = 1

    data = sql.getBook(3)
    return render_template("/productpage/endimensionellanalys.html",produktnamn=data[0],author=data[1],price=data[2],isbn=data[3],coursename=data[4])


@app.route("/programmeringipython", methods=["POST","GET"])
def programmeringpythonPage():
    if request.method == "POST":
    ## Session, save to cart
        flash("Tillagt i varukorg!", "info")
        if "2" in session:
            session["2"] += 1
        else:
            session["2"] = 1

    data = sql.getBook(4)
    return render_template("/productpage/programmeringpython.html",produktnamn=data[0],author=data[1],price=data[2],isbn=data[3],coursename=data[4])


@app.route("/industriellekonomi", methods=["POST","GET"])
def industriellekonomiPage():
    if request.method == "POST":
    ## Session, save to cart
        flash("Tillagt i varukorg!", "info")
        if "4" in session:
            session["4"] += 1
        else:
            session["4"] = 1

    data = sql.getBook(5)
    return render_template("/productpage/industriellekonomi.html",produktnamn=data[0],author=data[1],price=data[2],isbn=data[3],coursename=data[4])  
       

@app.route("/welcome")
def welcomePage():
    return render_template("welcome.html")


@app.route("/cart", methods=["POST","GET"])
def cartPage():
    cartDict, totalCost = sql.getCartData(session)

    if request.method == "POST":
        if request.form['action'] == 'Köp':
            return redirect(url_for("buyPage"))
        else:
            session.clear()
            return redirect(url_for("mainPage"))
    return render_template("cart.html",invoice=totalCost,cartDict=cartDict)


@app.route("/buyform", methods=["POST","GET"])
def buyPage():
    if request.method == "POST":
        costumerLst = []

        for key,value in request.form.items():
            costumerLst.append(value)
            
        customerID = sql.storeCostumer(costumerLst)
        orderID = sql.storeOrder(session,customerID)

        return redirect(url_for("thanksPage",ordNr=orderID))
    return render_template("buyform.html")
            


@app.route("/thanksORDERNummer=<ordNr>", methods=["POST","GET"])
def thanksPage(ordNr):
    session.clear()
    return render_template("thanks.html",orderNr=ordNr)
            
@app.route("/topplista")
def bestsellerPage():
    bestSellerLst = sql.getTopList()
    donated = sql.getDonatedMoney()
    return render_template("bestseller.html",sellerLst=bestSellerLst,donated=donated)




@app.route("/<name>")
def user(name):
    return f"Hej! Du har nog hamnat fel!"


if __name__ == "__main__":
    app.run()
    sql.closeSession()
