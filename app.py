from flask import Flask, request, render_template
import phonenumbers
from phonenumbers.geocoder import description_for_number, region_code_for_number
from phonenumbers.carrier import name_for_number
from phonenumbers.timezone import time_zones_for_number
from phonenumbers import number_type, PhoneNumberType

app = Flask(__name__)

def get_location_details(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)

        # Validasi nomor
        is_valid = phonenumbers.is_valid_number(parsed_number)
        is_possible = phonenumbers.is_possible_number(parsed_number)

        if not is_valid or not is_possible:
            return {"error": "Nomor tidak valid atau tidak mungkin ada."}

        location = description_for_number(parsed_number, "en")
        country_code = region_code_for_number(parsed_number)
        carrier = name_for_number(parsed_number, "en")
        timezones = time_zones_for_number(parsed_number)
        number_type_info = number_type(parsed_number)

        number_type_str = {
            PhoneNumberType.MOBILE: "Mobile",
            PhoneNumberType.FIXED_LINE: "Fixed Line",
            PhoneNumberType.TOLL_FREE: "Toll-Free",
            PhoneNumberType.PREMIUM_RATE: "Premium Rate",
            PhoneNumberType.SHARED_COST: "Shared Cost",
            PhoneNumberType.VOIP: "VoIP",
            PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
            PhoneNumberType.PAGER: "Pager",
            PhoneNumberType.UAN: "UAN",
            PhoneNumberType.UNKNOWN: "Unknown"
        }.get(number_type_info, "Unknown")

        return {
            "Valid Mobile Number": is_valid,
            "Possible Number": is_possible,
            "Location": location,
            "Country Code": country_code,
            "Carrier": carrier,
            "Time Zones": timezones,
            "Number Type": number_type_str
        }

    except phonenumbers.phonenumberutil.NumberParseException:
        return {"error": "Format nomor tidak dikenali, harap masukkan nomor yang benar."}

@app.route("/", methods=["GET", "POST"])
def index():
    details = None
    if request.method == "POST":
        phone_number = request.form.get("phone_number")
        details = get_location_details(phone_number)
    return render_template("index.html", details=details)

if __name__ == "__main__":
    app.run(debug=True)