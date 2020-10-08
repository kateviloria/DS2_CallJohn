# -*- coding: utf-8 -*-

import json

from flask import Flask, request
from jinja2 import Environment

app = Flask(__name__)
environment = Environment()


def jsonfilter(value):
    return json.dumps(value)

environment.filters["json"] = jsonfilter

with open('call_john/contacts.json', "r") as json_file:
    CONTACTS = json.load(json_file)

CONTACTS["contact_john"]["mobile"] = "0701234567"
CONTACTS["contact_john"]["work"] = "0736582934"
CONTACTS["contact_john"]["home"] = "031122363"

CONTACTS["contact_lisa"]["mobile"] = "0709876543"
CONTACTS["contact_lisa"]["work"] = "0763559230"
CONTACTS["contact_lisa"]["home"] = "031749205"

CONTACTS["contact_mary"]["mobile"] = "0706574839"
CONTACTS["contact_mary"]["work"] = "0784736475"
CONTACTS["contact_mary"]["home"] = "031847528"

# CONTACTS["contact_andy"]["mobile"] = None 

# don't need dump like in time dds?

def error_response(message):
    response_template = environment.from_string("""
    {
      "status": "error",
      "message": {{message|json}},
      "data": {
        "version": "1.0"
      }
    }
    """)
    payload = response_template.render(message=message)
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


def query_response(value, grammar_entry):
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.1",
        "result": [
          {
            "value": {{value|json}},
            "confidence": 1.0,
            "grammar_entry": {{grammar_entry|json}}
          }
        ]
      }
    }
    """)
    payload = response_template.render(value=value, grammar_entry=grammar_entry)
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


def validator_response(is_valid):
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.0",
        "is_valid": {{is_valid|json}}
      }
    }
    """)
    payload = response_template.render(is_valid=is_valid)
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/dummy_query_response", methods=['POST'])
def dummy_query_response():
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.1",
        "result": [
          {
            "value": "dummy",
            "confidence": 1.0,
            "grammar_entry": null
          }
        ]
      }
    }
     """)
    payload = response_template.render()
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/action_success_response", methods=['POST'])
def action_success_response():
    response_template = environment.from_string("""
   {
     "status": "success",
     "data": {
       "version": "1.1"
     }
   }
   """)
    payload = response_template.render()
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response



@app.route("/make_call", methods=['POST'])
def make_call():
    payload = request.get_json()

    #with open('call_john/contacts.json', "r") as json_file:
    #  CONTACTS = json.load(json_file)

    person_to_call = payload["context"]["facts"]["person_to_call"]["value"]
    number_type_to_call = payload["context"]["facts"]["number_type_to_call"]["value"]
    
    contact_number = CONTACTS[person_to_call][number_type_to_call]

    return action_success_response()
    

@app.route("/number_of_contact", methods=['POST'])
def number_of_contact():
    payload = request.get_json()

    person_to_call = payload["context"]["facts"]["person_to_call"]["value"]
    number_type_to_call = payload["context"]["facts"]["number_type_to_call"]["value"]

    contact_number = CONTACTS[person_to_call][number_type_to_call]

    return query_response(value=contact_number, grammar_entry=None) 