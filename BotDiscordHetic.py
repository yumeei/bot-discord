# Importations
import discord
from discord.ext import commands
import asyncio
import youtube_dl
import os

token = "Mettre le token du bot ici"

intents = discord.Intents.default()
intents.members = True
intents.typing = True

client = discord.Client(intents = intents)

voice_clients = {}

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}

# Validation que le Bot est bien en route
@client.event
async def on_ready():
    print("Bot prêt à l'action !")

# # Arbre Binaire
# # Chaque Noeud est une classe avec une valeur et un enfant de droite et de gauche
# class Noeud:
#     def __init__(self, valeur):
#         self.valeur = valeur
#         self.enfant_gauche = None
#         self.enfant_droite = None

#     # Définition pour insérer une valeur à l'enfant de droite ou de gauche
#     def insert_gauche(self, valeur):
#         if self.enfant_gauche == None:
#             self.enfant_gauche = Noeud(valeur)
#         else:
#             new_node = Noeud(valeur)
#             new_node.enfant_gauche = self.enfant_gauche
#             self.enfant_gauche = new_node

#     def insert_droite(self, valeur):
#         if self.enfant_droite == None:
#             self.enfant_droite = Noeud(valeur)
#         else:
#             new_node = Noeud(valeur)
#             new_node.enfant_droite = self.enfant_droite
#             self.enfant_droite = new_node

#     # Récupérer la donnée
#     def get_valeur(self):
#         return self.valeur
#     def get_gauche(self):
#         return self.enfant_gauche
#     def get_droite(self):
#         return self.enfant_droite

# # Affcher l'arbre sous forme d'un tuple (fonction récursive)
# def affiche(arbre):
#     if arbre != None:
#         return (arbre.get_valeur())

# # Racine est l'arbre au quel on peut insérer des valeurs
# racine = Noeud('A')
# racine.insert_gauche('B')
# racine.insert_droite('C')
# racine.enfant_gauche.insert_gauche('B1')
# racine.enfant_gauche.insert_droite('B2')
# racine.enfant_droite.insert_gauche('C1')
# racine.enfant_droite.insert_droite('C2')

# print(affiche(racine))

# Arbre général

Node = {"start":
"Bienvenue sur le Wolfy Gang Serveur qui te permettra de jouer au jeu du Loup Garou!\n"
"\n"
"Si tu as besoin d'informations et pour en apprendre plus tape **!info** sur le serveur **Wolfy Gang** dans le channel **sallon-de-wolfy** \n"
"\n"
"Amuse toi bien sur le serveur avec respect, fair-play et joie\n"
"C'était un plaisir pour moi de t'y accueillir\n"
"\n"
"Cordialement,\n"
"\n"
"Wolfy",
"info":
"Bonjour je suis Wolfy, un bot super sympa qui va te guider sur le serveur \n"
"\n"
"Je peux t'aider sur les sujets suivants :\n"
"\n"
"- Les règles du jeu : **!regle**\n"
"- Les rôles : **!role**\n"
"- Les différentes commandes du serveur : **!commande**\n"
"- Autres : **!autre**\n"
"\n"
"Sur quel sujet as-tu besoin d'aide ?",
"regle":
"Dans le jeu, Thiercelieux représente le village où se déroule toute l’action :\n"
"\n"
"**Quand la nuit tombe :** Pour les **villageois**, l’objectif est de démasquer et d’éliminer les bêtes, ils auront pour cela un rôle avec un pouvoir spécifique à chacun pour les aider.\n"
"\n"
"De leur côté, avec leurs crocs bien aiguisés, les **loups-garous** n’ont qu’un seul but : tuer et dévorer tous les villageois qui se trouvent sur leur chemin. Ils désignent une fois par nuit une victime à dévorer\n"
"\n"
"**Quand le jour se lève :** les morts sont révélé ainsi que leur rôle et c'est l'heure du débat pour voter contre la personne que l'on pense être un loup-Garou\n"
"\n"
"Chers Villageois, Chers Loups-Garous, Bonne chance\n"
"\n"
"Tape **!info** pour revenir au menu",
"role":
"Voici les rôles que tu retrouvera en jeu :\n"
"\n"
"Villageois : **!v**\n"
"Loup : **!l**\n"
"Sorcière : **!s**\n"
"Chasseur : **!c**\n"
"Garde : **!g**\n"
"\n"
"Tape **!info** pour revenir au menu ou **!role** pour revenir en arrière",
"v":
"Il n’a aucune compétence particulière. Ses seules armes sont la capacité d’analyse des comportements pour identifier les Loups-Garous, et la force de conviction pour empêcher l’exécution de l’innocent qu’il est.\n"
"\n"
"Tape **!info** pour revenir au menu ou **!role** pour revenir en arrière",
"l":
"Chaque nuit, ils dévorent un Villageois. Le jour, ils essaient de masquer leur identité nocturne pour échapper à la vindicte populaire. Ils sont 1, 2, 3 ou 4 suivant le nombre de joueurs et les variantes appliquées.\n"
"\n"
"Tape **!info** pour revenir au menu ou **!role** pour revenir en arrière",
"s":
"Elle sait concocter 2 potions extrêmement puissantes : une potion de guérison, pour ressusciter le joueur tué par les Loups-Garous, une potion d’empoisonnement, utilisée la nuit pour éliminer un joueur. La Sorcière doit utiliser chaque potion 1 seule fois dans la partie. Elle peut se servir des ses 2 potions la même nuit. Le matin suivant l’usage de ce pouvoir, il pourra donc y avoir soit 0 mort, 1 mort ou 2 morts. La Sorcière peut utiliser les potions à son profit, et donc se guérir elle-même si elle vient d’être attaquée par les Loups-Garous.\n"
"\n"
"Tape **!info** pour revenir au menu ou **!role** pour revenir en arrière",
"c":
"S’il se fait dévorer par les Loups-Garous ou exécuter malencontreusement par les joueurs, le Chasseur doit répliquer avant de rendre l’âme, en éliminant immédiatement n’importe quel autre joueur de son choix.\n"
"\n"
"Tape **!info** pour revenir au menu ou **!role** pour revenir en arrière",
"g":
"Son objectif est de vaincre les Loups-Garous. Chaque nuit, il peut protéger un joueur différent contre une attaque des Loups-Garous. Choisissez un joueur à protéger chaque nuit. Cette personne ne pourra pas être tuée pendant cette nuit et vous serez attaqué à sa place. De plus, votre force vous permet, une seule fois, de survivre à une attaque nocturne.\n"
"\n"
"Tape **!info** pour revenir au menu ou **!role** pour revenir en arrière",
"commande":
"Voici les commandes que tu peux utiliser :\n"
"\n"
"- **!info** : Que tu connais déjà, utile quand tu as besoin d'info, d'aide ou simplement d'un rappel\n"
"- **!jeu** : pour lancer une partie de Loup Garou\n"
"- **!serveur** : Pour voir la carte d'informations du serveur\n"
"- **!role** : Pour les rôles du jeu du Loup Garou\n"
"- **!regle** : Pour les règles du jeu\n"
"- **!autre** : Pour envoyer un petit message à mes concepteurs et leur dire à quel point je suis génial, que eux aussi ou leur avouer ton amour\n"
"- **!musique** : Pour gérer la musique et mettre un peu d'ambiance\n"
"\n"
"Tape **!info** pour revenir au menu",
"autre":
"Ecris ici pour que je contacte un modérateur qui va pouvoir répondre à ta question ou me mettre à jour pour que je puisse traiter ta demande :\n"
"\n"
"Tape **!info** pour revenir au menu",
"musique":
"- **!play** url (lien youtube): Pour mettre ta musique préférée, si tu n'as pas d'idée voici une musique d'ambiance pour le jeu du Loup-Garou \https://www.youtube.com/watch?v=fiiWimz-Q6g&t=2sn\n"
"- **!pause** : Mettre en pause la musique\n"
"- **!resume** : Reprendre la musique que tu as mis en pause\n"
"- **!stop** : Pour arrêter complètement la musique\n"
"\n"
"Tape **!info** pour revenir au menu",
"jeu":
"**🐺** : Rejoins la partie en tant que joueur\n"
"**🚫** : Finalement je ne joue pas\n"
"\n"
"**⚠️Partie en cours de construction⚠️**\n"
"Si tu veux jouer en attendant on te conseille un super site :\n"
"https://wolfy.net/fr"}

# Test Perso Commande
# Event message

@client.event
async def on_member_join(member):
    embed = discord.Embed(title = "Tu as rejoint le serveur du Wolf Gang",description = Node["start"])
    embed.set_thumbnail(url="https://ih1.redbubble.net/image.869439601.9327/bg,f8f8f8-flat,750x,075,f-pad,750x1000,f8f8f8.jpg")
    await member.send(f"Hey hey hey ! <@!{member.id}>")
    await member.send(embed = embed)

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith("!play"): # Pour mettre en route la musique !play + url youtube

        try:
            voice_client = await message.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except:
            print("error")

        try:
            url = message.content.split()[1]

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options, executable="C:\\ffmpeg\\ffmpeg.exe")

            voice_clients[message.guild.id].play(player)

        except Exception as err:
            print(err)

    # Met en pause la musique
    if message.content.startswith("!pause"):
        try:
            voice_clients[message.guild.id].pause()
        except Exception as err:
            print(err)

    # Remise en route de la musique si elle a été mise en pause
    if message.content.startswith("!resume"):
        try:
            voice_clients[message.guild.id].resume()
        except Exception as err:
            print(err)

    # Arrête complètement la musique
    if message.content.startswith("!stop"):
        try:
            voice_clients[message.guild.id].stop()
            await voice_clients[message.guild.id].disconnect()
        except Exception as err:
            print(err)

    message.content = message.content.lower()

    if message.content == "del":
        await message.channel.purge(limit = 2)

    if message.content == "!info":
        embed = discord.Embed(title = "Informations",description = Node["info"])
        embed.set_thumbnail(url="https://ih1.redbubble.net/image.869439601.9327/bg,f8f8f8-flat,750x,075,f-pad,750x1000,f8f8f8.jpg")
        await message.channel.send(embed = embed)
    if message.content == "!musique":
        embed = discord.Embed(title = "Musique",description = Node["musique"])
        embed.set_thumbnail(url="https://touhoppai.moe/theme/img/loupgarou/carte15joueurdeflute.jpg")
        await message.channel.send(embed = embed)
    if message.content == "!regle":
        embed = discord.Embed(title = "Les Règles",description = Node["regle"])
        embed.set_thumbnail(url="https://cdn5.coloritou.com/dessins/peindre/201540/regle-danimation-ecole-68948.jpg")
        await message.channel.send(embed = embed)
    if message.content == "!role":
        embed = discord.Embed(title = "Les Rôles",description = Node["role"])
        embed.set_thumbnail(url="https://i.pinimg.com/736x/cb/f5/d3/cbf5d3a19544893a75dc08441958d576.jpg")
        await message.channel.send(embed = embed)
    if message.content == "!serveur":
        name = "Wolfy Gang"
        description = "La bande de Wolfy s'aggrandit, rejoins la meute et joue au jeu du Loup-Garou"
        owner = "Wolfy GAROU"
        region = "FRANCE"
        member_count = "Vraiment beaucoup"

        embed = discord.Embed(
            title = name,
            description = description,
            color = discord.Color.red()
        )
        embed.set_thumbnail(url = "https://www.rts.ch/2012/10/16/14/18/4353928.image?mw=1280")
        embed.add_field(name = "Propriétaire", value = owner, inline = True)
        embed.add_field(name = "Région", value = region, inline = True)
        embed.add_field(name = "Nombre de membre", value = member_count, inline=True)
        
        await message.channel.send(embed = embed)
    if message.content == "!commande":
        embed = discord.Embed(title = "Les Commandes",description = Node["commande"])
        embed.set_thumbnail(url="https://ih1.redbubble.net/image.869439601.9327/bg,f8f8f8-flat,750x,075,f-pad,750x1000,f8f8f8.jpg")
        await message.channel.send(embed = embed)
    if message.content == "!autre":
        embed = discord.Embed(title = "Autre",description = Node["autre"])
        embed.set_thumbnail(url="https://ih1.redbubble.net/image.869439601.9327/bg,f8f8f8-flat,750x,075,f-pad,750x1000,f8f8f8.jpg")
        await message.channel.send(embed = embed)
    if message.content == "!v":
        embed = discord.Embed(title = "Villageois",description = Node["v"])
        embed.set_thumbnail(url="https://th.bing.com/th/id/OIP.Gt7sRnSp3N464oDzgLjfQQHaHa?pid=ImgDet&rs=1")
        await message.channel.send(embed = embed)
    if message.content == "!l":
        embed = discord.Embed(title = "Loup-Garou",description = Node["l"])
        embed.set_thumbnail(url="https://th.bing.com/th/id/OIP.7llS3Isn6e61ft0ZkTUwGgAAAA?pid=ImgDet&w=340&h=340&rs=1")
        await message.channel.send(embed = embed)
    if message.content == "!s":
        embed = discord.Embed(title = "Sorcière",description = Node["s"])
        embed.set_thumbnail(url="https://i.pinimg.com/736x/c7/7a/d5/c77ad50deeeb81720a8a807b696d9945.jpg")
        await message.channel.send(embed = embed)
    if message.content == "!c":
        embed = discord.Embed(title = "Chasseur",description = Node["c"])
        embed.set_thumbnail(url="https://data.topquizz.com/distant/question/big/6/1/8/5/935816_dd7aa547a1.jpg")
        await message.channel.send(embed = embed)
    if message.content == "!g":
        embed = discord.Embed(title = "Garde",description = Node["g"])
        embed.set_thumbnail(url="https://img.freepik.com/vektoren-kostenlos/handgezeichnete-vintage-axt-und-schild-der-wikinger_147266-45.jpg?size=338&ext=jpg")
        await message.channel.send(embed = embed)
    if message.content == "!jeu":
        embed = discord.Embed(title = "Jeu",description = Node["jeu"])
        embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT53Hn7xPQ_efgi-EJniw0rY26bgN9MJGq6wsVHw0Re4qtbPHNukUOzOl0boncCwib6gdI&usqp=CAU")
        temp = await message.channel.send(embed = embed)
        await temp.add_reaction("🐺")
        await temp.add_reaction("🚫")
        
    def checkEmoji(reaction, user):
        List_emoji = ["🐺","🚫"]
        return message.id == reaction.message.id and ((reaction.emoji) in List_emoji)

    reaction, user = await client.wait_for("reaction_add", check=checkEmoji)

    if reaction.emoji == "🐺":
        member = message.author
        role = discord.utils.get(message.guild.roles, name="Joueur")
        await member.add_roles(role)
        await message.channel.send(f'{member} à obtenue le role : {role}')
    elif reaction.emoji == "🚫":
        member = message.author
        role = discord.utils.get(message.guild.roles, name="Joueur")
        await member.remove_roles(role)
        await message.channel.send(f'{member} à perdu le role : {role}')

# @client.command()
# async def clear(ctx, nombre : int):
#     messages = await ctx.channel.history(limit = nombre + 1).flatten()
#     for message in messages:
#         await message.delete()

# Mettre en route le Bot
client.run(token)