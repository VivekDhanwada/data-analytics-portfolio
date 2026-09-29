import os
from dotenv import load_dotenv

load_dotenv()

AUTH_HEADER = os.environ.get("FUELCHECK_AUTH_HEADER")
API_KEY = os.environ.get("FUELCHECK_API_KEY")

TOKEN_URL = "https://api.onegov.nsw.gov.au/oauth/client_credential/accesstoken?grant_type=client_credentials"
PRICES_URL = "https://api.onegov.nsw.gov.au/FuelPriceCheck/v1/fuel/prices"
REFDATA_URL = "https://api.onegov.nsw.gov.au/FuelCheckRefData/v1/fuel/lovs"

EXCLUDED_BRANDS = {"AGL", "Chargefox", "Evie Networks", ""}
