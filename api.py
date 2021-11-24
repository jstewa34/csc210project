from flask import Flask, flash, redirect, render_template, session, url_for, jsonify
from app import create_app, db, login_manager
from models import User, Castaway, CastawayTeam
import json


def getAllUsers():
    get_users = User.query.all()
    users = [];
    for user in get_users:
        users.append(user.serialize())
    return jsonify({"user": users})

def getUserById(id):
    get_user = User.query.get(id)
    return jsonify({"user": get_user.serialize()})