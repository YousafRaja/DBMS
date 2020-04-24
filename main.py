import mysql.connector
from flask import Flask

mydb = mysql.connector.connect(
    host='localhost',
    user='admin',
    password='1234',
    database='471')

mycursor = mydb.cursor()
app = Flask(__name__)


def replyFromProc(name, args):
    try:
        mycursor.callproc(name,args)
        results = [r.fetchall() for r in mycursor.stored_results()]
        response = "Status 200"
        mydb.commit()
        for row in results:
            response += str(row) + " "
        return response
    except mysql.connector.Error as err:
        print(err)
        print("Error Code:", err.errno)
        print("SQLSTATE", err.sqlstate)
        print("Message", err.msg)
        return err.msg

@app.route("/User/<uid>",methods=['GET'])
def e1(uid): return replyFromProc('e1', (uid[1:-1],))

@app.route("/User/Friend_of_Friend",methods=['GET'])
def e2():return replyFromProc('e2', ())

@app.route("/User/<uid>",methods=['POST'])
def e3(uid):return replyFromProc('e3', (uid[1:-1],0,0,0,0,0,))

@app.route("/User/<uid>",methods=['PUT'])
def e4(uid): return replyFromProc('e4',(uid[1:-1],0,0,))

@app.route("/User/Offerer",methods=['GET'])
def e5(): return replyFromProc('e5',())

@app.route("/User/Requester",methods=['GET'])
def e6(): return replyFromProc('e6',())

@app.route("/Item/<itemId>/<uid>",methods=['POST'])
def e7(itemId, uid): return replyFromProc('e7',(itemId[1:-1],'2020/08/12',0,0,uid[1:-1],0,0,))

@app.route("/Item",methods=['GET'])
def e8(): return replyFromProc('e8',())

@app.route("/Item/<ItemId>",methods=['DELETE'])
def e9(ItemId): return replyFromProc('e9',(ItemId[1:-1],))

@app.route("/Item/Profile/User",methods=['GET'])
def e10(): return replyFromProc('e10',())

@app.route("/Admin/Manages/User",methods=['GET'])
def e11(): return replyFromProc('e11',())


@app.route("/Pictures/<ItemId>/<pUrl>",methods=['POST'])
def e12(ItemId,pUrl): return replyFromProc('e12',(ItemId[1:-1],pUrl[1:-1]))

@app.endpoint
def g2():
    return "1"

@app.route("/", methods=['GET', 'POST'])
def g():
    return "Response from our database"




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    # NOTE: This sends the requests to the internal port, the external port will still need to be forwarded from the router. We used 80 as the internal and 471 as the external port during testing.

#-------------------------------------------