# Campus Routing PoC Framework

A lightweight network test automation framework built to validate BGP and VLAN configurations on Arista EOS devices.

## What it does

- Runs automated health checks against network devices (or mock data)
- Compares actual device state against expected values defined in YAML
- Returns structured PASS/FAIL results via REST API
- (Optional) Uses Gemini AI to generate a plain-English network health summary

## How to run

```bash
pip install -r requirements.txt
python app.py
```

Then run a test:
```bash
curl -X POST http://127.0.0.1:5000/run/bgp_check
```

## Project structure

```
test_cases/        # YAML files defining what to check
mock_devices/      # Simulated device responses (JSON)
app.py             # Flask API
```

## Tech used

Flask · YAML · NAPALM (mock driver) · LangChain · Gemini API
