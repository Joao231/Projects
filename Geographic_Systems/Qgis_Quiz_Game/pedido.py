import requests
r = requests.get("https://raw.githubusercontent.com/paulojorge99/GamePlugin-GeoQuigiz/main/GEOQUIGIZ.csv")

url_content = r.content
csv_file = open('world_game.csv', 'wb')
csv_file.write(url_content)
csv_file.close()