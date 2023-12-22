import requests
from bs4 import BeautifulSoup
import discord #py-cord

# dba scraper
class Opslag:

    def __init__(self, beskrivelse, link, pris, imgLink):
        self.beskrivelse = beskrivelse
        self.link = link
        self.pris = pris
        self.imgLink = imgLink


def GetTopResultsForKeyword(keyword:str):
    grundURL = "https://www.dba.dk/soeg/?soeg={}"

    sesh = requests.session()
    soup = BeautifulSoup(sesh.get(grundURL.format(keyword)).content, "html.parser")

    resultsTable = soup.find("table", attrs={"class":"search-result searchResults srpListView"}).find("tbody")
    allListings = resultsTable.findAll("tr")[3::]

    doneListings = []
    antal = 0
    for listing in allListings:
        # error handling
        if listing["class"][0] != "adslot-intermingle":

            pictureTD = listing.find("td",attrs = {"class": "pictureColumn"})

            mainTD = listing.find("td",attrs={"class": "mainContent"})

            # get picture link
            try:
                picLink = pictureTD.find("div").find("a").find("img")["src"]
            except:
                picLink = "https://tenor.com/view/samorost3-samorost-gnome-cry-about-it-gif-25471201"

            # get listing link
            mainATag = mainTD.find("a")
            listingLink = mainATag["href"]

            # get description
            listingDeskrip = mainATag.find("span",attrs={"class": "text"}).text

            listingPrice = mainATag.find("span",attrs={"class": "price"}).text

            # create new "opslag" object
            doneListings.append(Opslag(listingDeskrip,listingLink,listingPrice,picLink))

    return doneListings


# discord bot:



bot = discord.Bot()

@bot.event
async def on_ready():
    print(r"""
Dedan Skecy's
__/\\\\\\\\\\\\________/\\\\\\\\\\\\___________________/\\\\\\\______________________/\\\\\\\\\____        
 _\/\\\////////\\\____/\\\//////////__________________/\\\/////\\\__________________/\\\\\\\\\\\\\__       
  _\/\\\______\//\\\__/\\\____________________________/\\\____\//\\\________________/\\\/////////\\\_      
   _\/\\\_______\/\\\_\/\\\____/\\\\\\\__/\\/\\\\\\\__\/\\\_____\/\\\__/\\/\\\\\\___\/\\\_______\/\\\_     
    _\/\\\_______\/\\\_\/\\\___\/////\\\_\/\\\/////\\\_\/\\\_____\/\\\_\/\\\////\\\__\/\\\\\\\\\\\\\\\_    
     _\/\\\_______\/\\\_\/\\\_______\/\\\_\/\\\___\///__\/\\\_____\/\\\_\/\\\__\//\\\_\/\\\/////////\\\_   
      _\/\\\_______/\\\__\/\\\_______\/\\\_\/\\\_________\//\\\____/\\\__\/\\\___\/\\\_\/\\\_______\/\\\_  
       _\/\\\\\\\\\\\\/___\//\\\\\\\\\\\\/__\/\\\__________\///\\\\\\\/___\/\\\___\/\\\_\/\\\_______\/\\\_ 
        _\////////////______\////////////____\///_____________\///////_____\///____\///__\///________\///__

Den Grønne Avis:
- DBA scraper discord bot
-----------------------------------------------------------------------------------------------------------------""")

    print("Den Grønne Avis er ONLINE")

@bot.slash_command(name = "gettopresult", description = "Get top result from keyword search")
async def gettopresult(ctx, keyword:str, placering:int):

    print("søger efter: "+keyword)
    try:
        opslagAll = GetTopResultsForKeyword(keyword)
    except:
        print("Der er sket en fejl med søgning: keyword={0} placering={1}".format(keyword,placering))
        await ctx.respond("Der er sket en fejl med søgning: keyword={0} placering={1}".format(keyword,placering))
        return
    if len(opslagAll) == 0:
        await ctx.respond("der er **INGEN** opslag for søgeordet: **{}**".format(keyword))
        return
    elif (placering <0 or placering > len(opslagAll)):
        await ctx.respond("Så mange opslag er der ikke for søge ordet **{1}**! Prøv et tal mellem **0 og {0}**".format(len(opslagAll)-1, keyword))
        return
    opslag = opslagAll[placering]
    embed = discord.Embed(
        title="Søgeord: "+keyword+" Placering på listen: "+str(placering),
        color=discord.Colour.blurple(),
        description="top resultat for \""+keyword+"\""
    )
    embed.set_image(url=opslag.imgLink)
    embed.add_field(name="pris:", value=opslag.pris)
    embed.add_field(name="beskrivelse:", value=opslag.beskrivelse)
    embed.add_field(name="link til opslag:", value=opslag.link)



    await ctx.respond("her er dit opslag du ledte efter", embed=embed)
token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
bot.run(token) # run the bot with the token


