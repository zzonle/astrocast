import os
from typing import Any, Dict

import requests


API_URL = os.getenv(
    "NODE_NASA_API_URL",
    "https://nasa-private.vercel.app/api/probabilities/forecast",  # default
)


class WeatherServiceError(Exception):
    """Error de alto nivel al consumir el servicio de clima/NASA."""
    pass


def clean_json(response_json: Dict[str, Any]) -> Dict[str, Any]:
    cleaned = {}
    categories = None

    # Predicted categories
    try:
        categories = response_json["comparison"]["categories"]
        cleaned["predicted"] = {
            "veryHot": categories["veryHot"]["predictedProbability"],
            "veryCold": categories["veryCold"]["predictedProbability"],
            "veryWindy": categories["veryWindy"]["predictedProbability"],
            "veryWet": categories["veryWet"]["predictedProbability"],
            "veryUncomfortable": categories["veryUncomfortable"]["predictedProbability"],
        }
    except KeyError:
        cleaned["predicted"] = {}

    # Observed results
    observed = {}
    try:
        for cat, data in categories.items():
            observed[cat] = {
                "actualOutcome": data.get("actualOutcome"),
                "brierScore": data.get("brierScore"),
            }
        cleaned["observed"] = observed
        cleaned["meanBrierScore"] = response_json["comparison"].get("meanBrierScore")
    except (KeyError, AttributeError):
        cleaned["observed"] = {}
        cleaned["meanBrierScore"] = None

    # Query context and thresholds
    query = response_json.get("query", {})
    cleaned["query"] = {
        "latitude": query.get("latitude"),
        "longitude": query.get("longitude"),
        "targetDate": query.get("targetDate"),
        "thresholds": query.get("thresholds", {}),
    }

    # External observations
    external = response_json.get("externalObservations", [{}])
    cleaned["externalErrors"] = external[0].get("error") if external else None

    return cleaned


def get_weather(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calls the private Node/NASA forecast service and returns a cleaned response.
    """

    if not API_URL:
        raise WeatherServiceError("NODE_NASA_API_URL is not configured in .env")

    payload = {
        "latitude": params["latitude"],
        "longitude": params["longitude"],
        "targetDate": params["targetDate"].isoformat(),
        "trainingStartYear": 1990,
        "trainingEndYear": 2020,
    }

    try:
        resp = requests.post(
            API_URL,
            json=payload,
            timeout=200,
        )
        resp.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise WeatherServiceError("Could not connect to the weather service.")
    except requests.exceptions.Timeout:
        raise WeatherServiceError(
            "The weather service took too long to respond. Please try again."
        )
    except requests.RequestException as exc:
        raise WeatherServiceError(
            f"Unknown error while contacting the weather service: {exc}"
        )

    try:
        raw_json = resp.json()
    except ValueError:
        raise WeatherServiceError("The weather service response is not valid JSON.")

    return clean_json(raw_json)