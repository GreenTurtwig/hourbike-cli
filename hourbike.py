import click
import requests
from geopy.geocoders import GoogleV3
from geopy.distance import distance as distanceCalc
import geopy.exc
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable insecure request warning.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

geolocator = GoogleV3(domain="maps.google.co.uk")
towns = ["lincoln", "liverpool", "reading", "sheffield", "southport"]

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("town")
@click.argument("location")
@click.option("--number", "-n", default=3, help="Number of results to show.")
@click.option("--all", "-a", is_flag=True, help="Show all stations.")
def run(town, location, number, all):
    """A CLI for Hourbike schemes across the UK."""
    # Check if input town is supported.
    town = town.lower()
    if town not in towns:
        click.echo("The input town is not supported or not recognised.")
        return
    
    # Handle geocoder exceptions.
    try:
        location = geolocator.geocode(location)
    except geopy.exc.GeocoderServiceError:
        click.echo("Unable to geocode your location at this time, check your internet connection or try again later.")
        return
    except geopy.exc.GeocoderTimedOut:
        click.echo("Geocoder timed out.")
        return

    # Check if input location is real.
    if location is None:
        click.echo("The input location is not recognised.")
        return

    # Request list of bicycle stations from API.
    try:
        stations = requests.get("https://tkhs-{}.cloudapp.net/Services/Api/Location/Map?lang=en".format(town), timeout=30, verify=False).json()["Locations"]
    except requests.exceptions.ReadTimeout:
        click.echo("Request for bikes timed out.")
        return
    
    # Sort station list by distance from input location.
    locationLatLon = (location.latitude, location.longitude)
    for x in range(len(stations)):
        stations[x]["Distance"] = round(distanceCalc(locationLatLon, (stations[x]["Latitude"], stations[x]["Longitude"])).miles, 2)
    stations = sorted(stations, key=lambda k: k["Distance"])

    # If number of stations to show is more than the actual number of stations, set to number of actual stations.
    if number > len(stations):
        number = len(stations)

    # If --all flag is input then set number of stations to show to number of actual stations.
    if all is True:
        number = len(stations)

    # Print out info on stations, sorted by distance.
    for x in range(number):
        click.echo("{} - {} Miles".format(stations[x]["Name"], stations[x]["Distance"]))
        if len(stations[x]["AvailableBikes"]) == 0:
            bikeNum = 0
        else:
            bikeNum = stations[x]["AvailableBikes"][0]["Count"]
        lockNum = stations[x]["TotalLocks"] - bikeNum
        click.echo("Bikes Available: {}    Locks Available: {}".format(bikeNum, lockNum))

        # Print out squares to represent bike docks.
        squares = ""
        for i in range(bikeNum):
            squares = squares + u"\u25A0 "
        for i in range(lockNum):
            squares = squares + u"\u25A1 "
        click.echo(squares)
        
        if x != (number - 1):
            click.echo("\n")

if __name__ == "__main__":
    run()