import logging

from geopy.geocoders import Nominatim

logger = logging.getLogger(__name__)


class Helper:

    @staticmethod
    def get_address_from_coordinates(coords) -> dict:
        geolocator = Nominatim(user_agent="civic-issue-app")
        location = geolocator.reverse(f"{coords}", language="en", zoom=18)
        if not location:
            return {"error": "Address not found"}

        addr = location.raw.get("address", {})

        return {
            "address": location.address,
            "city": addr.get("city") or addr.get("town"),
            "state": addr.get("state"),
            "country": addr.get("country"),
            "postcode": addr.get("postcode")
        }