# VulnX Crimeathon

VulnX is a focused security assessment platform for the supplied Crimeathon simulation and controlled local website checks.

## Quick start

1. Create a virtual environment.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Start the mock API in vulnerable or hardened mode:
   `python data/crimeathon/simulation/mock_api_server.py --mode vulnerable`
4. Run the assessment engine:
   `python -m pytest tests/test_core_engine.py`
5. Explore the API with the Flask app:
   `python app.py`

## Included milestone

This repository includes the first working milestone: VulnX Core Engine v1.0.

It can:
- communicate with the local mock API,
- compare vulnerable vs hardened behavior,
- run controlled security checks,
- preserve evidence and findings in structured JSON.

## Important

This local simulation is intentionally a training tool, not a real external system.
