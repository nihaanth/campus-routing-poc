from flask import Flask, jsonify, request
import yaml
import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def load_test_case(test_id):
    path = f'test_cases/{test_id}.yaml'
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return yaml.safe_load(f)

def get_device_data(device_name,data_source):
    path = f'mock_devices/{device_name}/{data_source}.json'
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)

def run_checks(test_case):
    device = test_case['device']
    results = []

    for check in test_case['checks']:
        data = get_device_data(device,check['data_source'])

        actual = data
        for key in check['path']:
            if isinstance(actual,dict):
                actual= actual.get(key)
            else:
                actual = None

        passed = str(actual) == str(check['expected'])
        results.append({
                "name":     check["name"],
                "expected": check["expected"],
                "actual":   actual,
                "result":   "PASS" if passed else "FAIL"
            })

    return results

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')    

# def analyze_results(test_id,checks):
#     llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash')

#     summary = '\n'.join([f"c['name'] {c['result']}" for c in checks])
#     prompt = f"Network test results for {test_id}:\n{summary}\nWrite a 2-sentence plain-English health summary."
#     return llm.invoke(prompt).content


@app.route('/tests',methods=['GET'])
def list_tests():
    return jsonify({'tests':['bgp_check','vlan_check']})

@app.route('/run/<test_id>', methods=['POST'])
def run_test(test_id):
    test_case = load_test_case(test_id)
    if not test_case:
        return jsonify({
            'error':f'Test "{test_id}" not found'
        }),404



    checks = run_checks(test_case)
    # ai_summary = analyze_results(test_id, checks)
    passed = sum(1 for c in checks if c["result"] == "PASS")

    return jsonify({
        "test_id": test_id,
        "passed":  passed,
        "failed":  len(checks) - passed,
        "checks":  checks,
        # "ai summary": ai_summary
    })

@app.route('/report/<test_id>', methods=['GET'])
def get_report(test_id):
    return jsonify({"test": test_id, "result": "pass"})

if __name__ == '__main__':
    app.run(debug=True)