"""Deliverable1"""
import json
from methods import Token, Restricted
from convert import CidrMaskConvert, IpValidate
from flask_lambda import FlaskLambda
from flask import request


app = FlaskLambda(__name__)
convert = CidrMaskConvert()
login = Token()
validate = IpValidate()
protected = Restricted()


@app.route("/")
def url_root():
    """Just a health check"""
    return "OK"


@app.route("/health")
def url_health():
    """Just a health check"""
    data= {
        "message": "hola mundo"
    }
    return (
        json.dumps(data),
        200,
        {'Content-Type': 'application/json'}
    )


@app.route("/login", methods=['POST'])
def url_login():
    """Generates token for a given user/password"""
    username = request.form['username']
    password = request.form['password']
    result = login.generate_token(username, password)
    if result:
        response = {"data": result}
        return (
            json.dumps(response), 
            200,
            {'Content-Type': 'application/json'}
        )   
    response = {"data": "invalid username or password"}
    return (
        json.dumps(response),
        401,
        {'Content-Type': 'application/json'}
    )       


@app.route("/cidrtomask")
def url_cidr_to_mask():
    """With token authentication, receives cidr and returns equivalent mask value"""
    cidr = request.args.get('value')
    header = request.headers.get('Authorization')
    if not protected.access_data(header):
        response = {
            "Authentication": "Failed, Invalid Token"
        }
        return (json.dumps(response),
            401,
            {'Content-Type': 'application/json'}
        )   
    if not convert.cidr_to_mask(cidr):
        response = {
            "function": "maskToCidr",
            "input": cidr,
            "output": "Invalid cidr"
        }
        return (
            json.dumps(response),
            400,
            {'Content-Type': 'application/json'}
        )   
    response = {
        "function": "maskToCidr",
        "input": cidr,
        "output": convert.cidr_to_mask(cidr)
    }
    return(
        json.dumps(response),
        200,
        {'Content-Type': 'application/json'}
    )     

@app.route("/masktocidr")
def url_mask_to_cidr():
    """With token authentication, receives mask and returns equivalent cidr value"""
    netmask = request.args.get('value')
    header = request.headers.get('Authorization')
    if not protected.access_data(header):
        response = {
            "Authentication": "Failed, Invalid Token"
        }
        return (
            json.dumps(response),
            401,
            {'Content-Type': 'application/json'}
        )   
    if not convert.mask_to_cidr(netmask):
        response = {
            "function": "maskToCidr",
            "input": netmask,
            "output": "Invalid netmask"
        }
        return (
            json.dumps(response),
            400,
            {'Content-Type': 'application/json'}
        )   
    response = {
        "function": "maskToCidr",
        "input": netmask,
        "output": convert.mask_to_cidr(netmask)
    }
    return (
        json.dumps(response),
        200,
        {'Content-Type': 'application/json'}
    )   
