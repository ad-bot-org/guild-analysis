import json
from flask import Flask, jsonify, request
from analysis_guild import analysisGuild

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/guild-data-analysis', methods=['POST'])
def main():
    request_data = request.get_json()
    df = analysisGuild(request_data)
    return jsonify(df)

app.run(host='0.0.0.0', port=5000)