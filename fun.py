from flask import jsonify, Blueprint

auth = Blueprint('auth',__name__)

@auth.route('/armstrong/<int:n>')
def armstrong(n):
    sum=0
    order=len(str(n))
    nn=n
    while(n>0):
        digit=n%10
        sum+=digit**order
        n=n/10

    if(sum==nn):
        print(f"{nn} is an Armstrong Number")
        result={
            "Number": nn,
            "Armstrong": True
        }

    else:
        print(f"{nn} isn't an Armstrong Number")
        result={
            "Number": nn,
            "Armstrong": False
        }

    return jsonify(result)