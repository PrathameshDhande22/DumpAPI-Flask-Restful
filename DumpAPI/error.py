from flask import jsonify


def errorpage(e):
    return jsonify({"message": "Wrong method"}), 404


def errorpage1(e):
    return jsonify({"message": "Something Wrong Happen At our End"}), 500


def error400(e):
    return jsonify({"message": "Please Provide the Required Data in the Post Body in JSON Format"})
