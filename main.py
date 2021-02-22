import json
from flask import Flask, jsonify, request
from analysis_guild import analysisGuild

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/guild-data-analysis', methods=['POST'])
def main():
    request_data = request.get_json()
    print(request_data)
    df = analysisGuild(request_data)
    return jsonify(df)

app.run(port=5000)