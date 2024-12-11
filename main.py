import discord
from typing import Union
import asyncio
import os
import json
import pytz
import socket
import random
import warnings
import matplotlib.pyplot as plt  
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from datetime import datetime, timedelta
from discord.ext import commands, tasks
from discord import Embed
from discord import app_commands
from flask import Flask, Response
import subprocess
import aiohttp

intents = discord.Intents.all()
intents.guild_messages = True

bot = commands.Bot(command_prefix='?', intents=intents, help_command=None)

with open('token.json') as token_file:
    data = json.load(token_file)
    bot_token = data['token']

def ignore_tight_layout_warning(message, category, filename, lineno, file=None, line=None):
    return 'The figure layout has changed to tight' in str(message)

warnings.filterwarnings('ignore', category=UserWarning, message='The figure layout has changed to tight')

#####################################################################################################################
#                                                                                                                   #
#                                                                                                                   #
#                                                COMMANDES CORE : V3                                                #
#                                               PAR PILOTE PRODUCTION                                               #
#                                                                                                                   #
#####################################################################################################################

@bot.command()
async def ping(ctx):
    api_ping = round(bot.latency * 1000)
    
    before = discord.utils.utcnow()
    async with aiohttp.ClientSession() as session:
        async with session.get("https://modded.pilotestudio.com/api/getIP.php") as response:
            after = discord.utils.utcnow()
            bot_ping = round((after - before).total_seconds() * 1000 - api_ping)
            await ctx.send(content=f":ping_pong: Ping de l'API Discord: **{api_ping} ms**\n:robot: Ping du bot: **{bot_ping} ms**")
    

@bot.hybrid_group(name="help", description="Affiche la commande d'aide")
async def help_group(ctx):
    if ctx.invoked_subcommand is None:
        embed = discord.Embed(title="Catégories de commandes", description="Utilisez l'une des sous-commandes suivantes pour obtenir de l'aide sur une catégorie spécifique :", color=discord.Color.blue())
        embed.add_field(name="Économie <a:money:1118983615418728508>", value="`/duel`: Défie un autre joueur dans un duel\n`/trio`: Défie deux autres joueurs dans un trio.\n`/work`: Travaille pour de l'argent\n`/gamble`: Joue ton argent\nPlus d'information sur les commandes de l'économie via la commande `/help economie` !", inline=False)
        embed.add_field(name="Niveaux <a:star:1112807470470021150>", value="`/levels`: Affiche ton niveau\n`/leaderboard`: Affiche le tableau des personnes les plus haut niveau", inline=False)
        embed.add_field(name="Utilitaire <a:dancingrgb:1112807461905240098>", value="`/invite`: Invite le robot sur ton propre serveur\n`/support`: Affiche le lien du support du bot\n`/pilote`: Affiche les personnes qui ont .gg/PILOTE dans le status personnalisé", inline=False)
        embed.add_field(name="Évenement <a:tadaglowing:1112807453566976112>", value="`/ticket free`: Obtiens un ticket gratuitement\n`/ticket pay` Obtiens un ticket en payant\n`/ticket roulette`: Lance la roulette", inline=False)
        embed.add_field(name="Administration & modération <:mod:1112807479986880622> ", value="`/warn add`: Averti un utilisateur\n`/warn remove`: Retire un avertissement\n`/warn show`: Affiche le nombre d'avertissements d'un utilisateur\n`/warn list`: Affiche la liste des avertissements d'un utilisateur\n`/warn reset`: Reset les averissement d'un utilisateur\n\n`/addrole`: Ajoute le rôle demandé à l'utilisateur mentionné\n`/removerole`: Supprime le rôle demandé à l'utilisateur mentionné\n`/lock`: Verouille le salon demandé\n`/unlock`: Déverouille le salon demandé\n\n(Arrive bientôt)\n`/scan` Execute un scan de sécurité sur le serveur\n`/blacklist on/off`: Active l'expulsion automatique des utilisateurs présent dans la Blacklist de notre robot", inline=False)
        embed.add_field(name="Options de control <:mod:1112807479986880622> ", value="`/help control`: Affiche la liste des commmandes disponbiles", inline=False)
        await ctx.send(embed=embed)
@help_group.command(name="economie", description="Liste des commandes disponibles pour la catégorie Économie")
async def help_economie(ctx):
    embed = discord.Embed(title="Commande sur l'Économie :star:", description="Commande de la partie économie du robot", color=discord.Color.blue())
    embed.add_field(name="Tutoriel", value="Vous êtes nouveau sur le serveur ? utilisez la commande `/tutoriel start` qui explique tout le système d'économie !", inline=False)
    embed.add_field(name="Commandes principales", value="`/balance`: Affiche le solde de ton compte\n`/pay [utilisateur] [montant]`: Envoi de l'argent\n`/leaderboard money`: Affiche le top\n`/work`: Travail pour de l'argent\n`/steal [utilisateur]`: Vole de l'argent à d'autres utilisateurs\n`/tirage`: Gagne de l'argent (VIP)\n`/loan loan [montant]`: Fait un prêt à la banque\n`/daily claim`: Réclamme ta récompense journalière\n`/bank`: Gère ta banque\n`/rewards`: Affiche les récompenses disponibles\n`/boutique`: Affiche la boutique", inline=False)
    embed.add_field(name="Commandes fun", value="`/duel` Défie un autre joueur\n`/trio`: Défi deux autres joueurs\n`/gamble`: Joue ton argent\n`/speedy`: Rapide ?\n`/roulette`: Joue à la roulette", inline=False)
    embed.add_field(name="Commandes (commandes)", value="`/payout`: Retire de l'argent en argent IRL\n`/payout payout`: Retrait avec le taux actuel\n`/order`: Récupère ta commande ou vérifie son statut", inline=False)
    embed.add_field(name="Les mineurs", value="`/mineurs`: Affiche ton solde de minerais et le niveau de chaque minerai que tu possèdes.\n`/mineurs list`: Affiche les niveaux achetables pour chaque minerai.\n`/mineurs buy [minerai]`: Achète et met à niveau un niveau de minerai spécifié.\n`/mineurs sell [minerai]/(all) (quantité)`: Vend des minerais contre de l'argent.\n`/mineurs sellout`: Affiche le taux de vente des pièces rouges en pièces et permet de vendre des pièces rouges.\n`/mineurs balance`: Affiche ton solde actuel en pièces rouges.\n`/mineurs upgrade`: Améliore la limite de ton minage.", inline=False)
    await ctx.send(embed=embed)

@help_group.command(name="control")
async def help_control(ctx):
    embed = discord.Embed(title="Catégorie de commande : Control Panel", description="Commandes pour les administrateurs de serveur", color=discord.Color.yellow())
    embed.add_field(name="Vide.", value="C'est bien triste ici, malheuresement aucune commande lié au développement n'est disponible pour le moment")
    await ctx.send(embed=embed)

async def send_status():
    url = "https://status.pilotia.cloud/api/push/rSKCyO8sp9?status=up&msg=OK&ping="
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    pass
                else:
                    pass
        await asyncio.sleep(90)
        
@bot.event
async def on_ready():
    os.makedirs("data", exist_ok=True)
    bot.loop.create_task(update_payout())
    """bot.loop.create_task(update_UTC())
    bot.loop.create_task(update_LTC())
    bot.loop.create_task(update_PLT())"""
    bot.loop.create_task(mine_on_seconds())
    bot.loop.create_task(send_status())
    bot.loop.create_task(give_coins_on_voice_activity())
    bot.loop.create_task(loop_send_message())
    await bot.tree.sync()
    while True:
        server_id = 1103936072989278279
        server = bot.get_guild(server_id)
        if server is not None:
            member_count = server.member_count
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{len(bot.guilds)} serveurs'))
            await asyncio.sleep(30)
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'/help pour obtenir de l\'aide !'))
            await asyncio.sleep(30)
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'Membres: {member_count}'))
            await asyncio.sleep(30)
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'.gg/PILOTE'))
            await asyncio.sleep(30)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            message = "Vous n'avez pas les permissions nécessaires pour exécuter cette commande."
        elif isinstance(error, commands.CommandOnCooldown):
            message = f"La commande est en cooldown. Veuillez réessayer dans {round(error.retry_after)} secondes."
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f"Argument manquant. Utilisation correcte : `{ctx.prefix}{ctx.command.name}`"
        else:
            message = f"Une erreur s'est produite lors de l'exécution de la commande : {str(error)}"

        embed = discord.Embed(
            title="Erreur",
            description=message,
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        print(f"Erreur : {str(error)}")
    else:
        raise error

async def check_tutorial_completion(user_id):
    try:
        with open(f"data/tutoriel/{user_id}.json", "r") as file:
            data = json.load(file)
            return data.get("tutorial", False)
    except FileNotFoundError:
        return False

async def give_coins_on_voice_activity():
    server_id = '1103936072989278279'
    vocal_argent_channel_id = 1138829737029013585
    notification_channel_id = 1138820990898544683
    print("✅ | Démarrage des salons vocaux.")
    while True:
        try:
            guild = bot.get_guild(int(server_id))
            if guild:
                vocal_argent_channel = guild.get_channel(vocal_argent_channel_id)
                notification_channel = guild.get_channel(notification_channel_id)
                if vocal_argent_channel and notification_channel:
                    for member in vocal_argent_channel.members:
                        user_id = str(member.id)
                        server_path = f"data/server/{server_id}/{user_id}.json"

                        user_data = load_user_money(server_id, user_id)
                        user_balance = user_data.get("balance", 0)
                        user_balance += 1000
                        user_data["balance"] = user_balance
                        save_user_money(server_id, user_id, user_data)

                        await notification_channel.send(f"{member.mention} a gagné 1000 pièces pour être resté actif dans le salon Vocal Argent !")
                else:
                    print("Personne connectée")
            else:
                print("Guild introuvable")
        except Exception as e:
            print(f"Erreur dans give_coins_on_voice_activity : {e}")
        await asyncio.sleep(60*10)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id == 1138820990898544683 and not await check_tutorial_completion(message.author.id):
        if not message.content.startswith('?tutoriel start'):
            embed = discord.Embed(
                    title="Erreur",
                    description="Vous devez d'abord suivre le tutoriel avec la commande `/tutoriel start` ou passe le tutoriel avec la commande `/tutoriel skip`.",
                    color=discord.Color.red()
                )
            await message.channel.send(embed=embed)
            return

    if message.channel.id == 1138820990898544683 and not await check_tutorial_completion(message.author.id):
        if not message.content.startswith('?tutoriel start'):
            embed = discord.Embed(
                    title="Erreur",
                    description="Vous devez d'abord suivre le tutoriel avec la commande `/tutoriel start`.",
                    color=discord.Color.red()
                )
            await message.channel.send(embed=embed)
            return

    if not message.author.guild_permissions.administrator:
        file_path = f"server/{message.guild.id}/{message.author.id}.json" 
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                json.dump([], f)

        if any(member.id == 97285029289275392 for member in message.mentions):
            """embed = discord.Embed(
                title="BigBrother - Avertissement",
                description="Les mentions inutiles d'administrateurs sont sanctionnées. Assurez-vous que votre mention est nécessaire et pertinente. Cette mention a été enregistrée par le Système BigBrother et sera traitée en cas de mention inutile.",
                color=discord.Color.red()
            )"""
            mentioned_user = message.mentions[0]
            mentioner = message.author
            print(f"Utilisateur mentionné : {mentioned_user.name} (ID: {mentioned_user.id}), Mentionneur : {mentioner.name} (ID: {mentioner.id})")
            """sended = await message.channel.send(embed=embed)"""

            user = message.author

            with open(file_path, "r") as f:
                warnings = json.load(f)
            
            reason = "Mention Administrateur (Automatique)"
            
            warnings.append({"reason": reason, "timestamp": str(datetime.now())})
            with open(file_path, "w") as f:
                json.dump(warnings, f)
            
            embed = discord.Embed(title="Avertissement", description=f"Attention {user.mention}, les mentions administrateurs sont interdits par le règlement. Vous avez donc reçu un avertissement et votre message à été **supprimé**.", color=0xFF5733)
            await message.channel.send(embed=embed)
            await message.delete()

            try:
                embed = discord.Embed(title="Avertissement", description=f"{user.mention}\nVous avez reçu un avertissement pour la raison suivante : {reason}", color=0xFF5733)
                await user.send(embed=embed)
            except discord.Forbidden:
                print(f"Impossible d'envoyer un message privé à {user} car ses messages privés sont désactivés.")
            
            channel = bot.get_channel(1103936074805420065)
            if channel:
                embed = discord.Embed(
                    title="BigBrother - AntiMention",
                    description=f"Nouvelle mention de {mentioner.name} (ID: {mentioner.id}) a été enregistrée par le Système BigBrother\nMessage envoyé : {message.content}",
                    color=discord.Color.green()
                )

                await channel.send(embed=embed)
            else:
                print("Salon introuvable.")
            
        with open(file_path, "r") as f:
            warnings = json.load(f)

        if len(warnings) >= 3:
            user = message.author

            with open(file_path, "w") as f:
                json.dump([], f)

            embed = discord.Embed(
                title="Sanction automatique",
                description=f"{user.mention}, vous allez être mis en timeout pour une durée de 24 heures en raison d'avoir reçu trois avertissements. Cette sanction sera active d'ici quelques minutes.\n\nAstuce : Assurez-vous de respecter le règlement du serveur lors de vos prochaines interactions.\n\n",
                color=0xFF5733
            )
            await message.channel.send(embed=embed)

            channel = bot.get_channel(1103936074805420065)
            if channel:
                embed = discord.Embed(
                    title="Trop d'avertissement",
                    description=f"L'utilisateur {user.name} (ID: {user.id}) doit être bannis 24 heures suite à 3 avertissements.",
                    color=discord.Color.green()
                )

                await channel.send("<@97285029289275392>", embed=embed)
            else:
                print("Salon introuvable.")


    if not message.author.guild_permissions.administrator:
        file_path = f"server/{message.guild.id}/{message.author.id}.json" 
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                json.dump([], f)

    server_id = str(message.guild.id)
    user_id = str(message.author.id)
    
    level_data = get_user_level(message.guild.id, message.author.id)
    message_length = len(message.content)
    level_data["xp"] += message_length
    xp_for_next_level = xp_for_level(level_data["level"])
    if level_data["xp"] >= xp_for_next_level:
        level_data["level"] += 1
        level_data["xp"] -= xp_for_next_level
        user_data = load_user_money(str(message.guild.id), str(message.author.id))
        win = level_data['level'] * 1000
        user_data["balance"] += win
        embed = discord.Embed(title="<a:tadaglowing:1112807453566976112> Nouveau niveau atteint ! <a:tadaglowing:1112807453566976112>", description=f"Félicitations {message.author.mention}, vous avez atteint le niveau {level_data['level']} !\n Vous avez gagné : {win} <a:money:1118983615418728508> !", color=0xFF69B4)
        embed.set_image(url="https://pilotestudio.com/upload_web/uploads/levelup.gif")
        await message.channel.send(embed=embed)

        save_user_money(str(message.guild.id), str(message.author.id), user_data)

    save_user_level(message.guild.id, message.author.id, level_data)
    
    amount = 1
    user_data = load_user_money(str(message.guild.id), str(message.author.id))
    user_data["balance"] += amount
    save_user_money(str(message.guild.id), str(message.author.id), user_data)
    
    if user_data["balance"] < 0:
        user_data["balance"] = 0
        embed = discord.Embed(title="Avertissement", description="Votre solde est devenu négatif. Votre balance a été réinitialisée à zéro.", color=discord.Color.red())
        await message.channel.send(embed=embed)
        save_user_money(str(message.guild.id), str(message.author.id), user_data)
    
    if isinstance(user_data["balance"], float):
        rounded_balance = round(user_data["balance"])

        user_data["balance"] = rounded_balance
        save_user_money(str(message.guild.id), str(message.author.id), user_data)
        embed = discord.Embed(title="Avertissement", description="Votre solde est devenu à virgule. Votre balance a été corrigé avec succès.", color=discord.Color.red())
        await message.channel.send(embed=embed)

    user_data_bank = load_user_bank(server_id, user_id)
    balance = user_data["balance"]
    level = user_data_bank["level"]
    max_balance = level * 85000

    if balance > max_balance:
        if not message.author.guild_permissions.administrator:
            embed = discord.Embed(title="Ajustement de Solde", description=f"Votre solde a été ajusté à {max_balance} <a:money:1118983615418728508> car votre banque est de niveau {level}.\nPour améliorer votre banque, faites `/bank upgrade`.", color=discord.Color.orange())
            sended = await message.channel.send(embed=embed)
            max_balance -= 150
            user_data["balance"] = max_balance
            save_user_money(server_id, user_id, user_data)
            await asyncio.sleep(10)
            await sended.delete()

        
    await bot.process_commands(message)

def load_user_bank(server_id, user_id):
    filename = f"data/bank/{server_id}/{user_id}.json"
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        os.makedirs(f"data/bank/{server_id}", exist_ok=True)
        data = {"level": 1}
        with open(filename, "w") as file:
            json.dump(data, file)
    return data

def save_user_bank(server_id, user_id, data):
    os.makedirs(f"data/bank/{server_id}", exist_ok=True)
    filename = f"data/bank/{server_id}/{user_id}.json"
    with open(filename, "w") as file:
        json.dump(data, file)

def check_user_ban_status(server_id, user_id):
    banned_list_path = f"data/ban/{server_id}/{user_id}.json"
    
    if not os.path.exists(banned_list_path):
        return None
    
    with open(banned_list_path, "r") as file:
        banned_data = json.load(file)
    
    reason = banned_data["reason"]
    admin_id = banned_data["admin_id"]
    
    return reason, admin_id

def add_user_to_banlist(server_id, admin_id, user_id, reason):
    banned_list_dir = f"data/ban/{server_id}"
    os.makedirs(banned_list_dir, exist_ok=True)
    banned_list_path = f"{banned_list_dir}/{user_id}.json"
    
    if os.path.exists(banned_list_path):
        return False
    
    banned_data = {
        "admin_id": admin_id,
        "reason": reason
    }
    
    with open(banned_list_path, "w") as file:
        json.dump(banned_data, file, indent=4)
    
    return True

def remove_user_from_banlist(server_id, user_id):
    banned_list_path = f"data/ban/{server_id}/{user_id}.json"
    
    if not os.path.exists(banned_list_path):
        return False
    
    os.remove(banned_list_path)
    return True

def load_user_money(server_id, user_id):
    filename = f"data/money/{server_id}/{user_id}.json"
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        os.makedirs(f"data/money/{server_id}", exist_ok=True)
        data = {"balance": 0}
        with open(filename, "w") as file:
            json.dump(data, file)
    return data

def save_user_money(server_id, user_id, data):
    os.makedirs(f"data/money/{server_id}", exist_ok=True)  
    filename = f"data/money/{server_id}/{user_id}.json"
    with open(filename, "w") as file:
        json.dump(data, file)

USERS_FOLDER = "data/daily/"

def check_users_folder():
    if not os.path.exists(USERS_FOLDER):
        os.makedirs(USERS_FOLDER)

def load_user_data_daily(user_id):
    check_users_folder()
    file_path = f"{USERS_FOLDER}{user_id}.json"
    try:
        with open(file_path, "r") as file:
            user_data = json.load(file)
            if "last_daily" in user_data and user_data["last_daily"] is not None:
                user_data["last_daily"] = datetime.strptime(user_data["last_daily"], "%Y-%m-%d %H:%M:%S")
    except (FileNotFoundError, json.JSONDecodeError):
        user_data = {"last_daily": None, "daily_streak": 0}
    return user_data

def save_user_data_daily(user_id, user_data):
    check_users_folder()
    file_path = f"{USERS_FOLDER}{user_id}.json"
    if "last_daily" in user_data and user_data["last_daily"] is not None:
        user_data["last_daily"] = user_data["last_daily"].strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, "w") as file:
        json.dump(user_data, file, default=str)

def load_ticket_data(server_id, user_id=None):
    path = f'data/ticket/{server_id}/{user_id}.json'
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as file:
            json.dump({}, file)
    with open(path, 'r') as file:
        data = json.load(file)
    return data

def save_ticket_data(server_id, user_id, data):
    path = f'data/ticket/{server_id}/{user_id}.json'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as file:
        json.dump(data, file)

def load_settings(server_id):
    config_file = f"data/config/{server_id}.json"
    if not os.path.exists(config_file):
        with open(config_file, "w") as f:
            default_settings = {"economy": False}
            json.dump(default_settings, f)

    with open(config_file, "r") as f:
        server_settings = json.load(f)
    return server_settings

def save_settings(server_id, server_settings):
    config_file = f"data/config/{server_id}.json"
    with open(config_file, "w") as f:
        json.dump(server_settings, f, indent=4)

async def check_settings(server_id, user_id):
    server_settings = load_settings(server_id)

    ban_info = check_user_ban_status(server_id, user_id)
    if ban_info is not None:
        reason, admin_id = ban_info
        admin = bot.get_user(admin_id)
        embed = discord.Embed(
            title="Compte Monétaire suspendu",
            description=f"Votre compte monétaire a été suspendu pour la raison suivante : `{reason}`.\n Vous avez été banni par {admin.mention}.\nSi vous souhaitez contester cette sanction, veuillez contacter le support du serveur.",
            color=discord.Color.red()
        )
        return embed

    if not server_settings.get("economy", False):
        embed = discord.Embed(
            title="Erreur",
            description="L'économie n'est pas activée sur ce serveur. Veuillez contacter l'administrateur du serveur pour plus d'informations.",
            color=discord.Color.red()   
        )
        return embed

    return None

@bot.hybrid_group(name='setup', description="Configurer les fonctionnalités du bot.", invoke_without_command=True)
async def setup(ctx):
    if ctx.invoked_subcommand is None:
        server_id = str(ctx.guild.id)
        
        server_settings = load_settings(server_id)
        
        economy = server_settings.get("economy", False)
        economy_status = "Activée" if economy else "Désactivée"
        economy_emote = "✅" if economy else "❌"

        embed = discord.Embed(
            title="Paramètres du serveur",
            description=f"**Économie**: {economy_emote} {economy_status}",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

@setup.command(name='toggle', description="Activer ou désactiver une fonctionnalité.")
@commands.has_permissions(administrator=True)
async def toggle(ctx, feature: str):
    feature = feature.lower()
    if feature == "economy":
        server_id = str(ctx.guild.id)

        server_settings = load_settings(server_id)
        
        economy = server_settings.get("economy", False)
        server_settings["economy"] = not economy
    
        save_settings(server_id, server_settings)

        status = "activée" if not economy else "désactivée"
        await ctx.send(f"L'économie a été {status} avec succès.")

    else:
        await ctx.send("Fonctionnalité invalide. Les fonctionnalités disponibles sont: economy.")

@bot.event
async def on_member_join(member):
    user_id = str(member.id)
    server_id = str(member.guild.id)
    
    server_settings = load_settings(server_id)

    if not server_settings.get("economy", False):
        return

    user_money = load_user_money(server_id, user_id)
    user_money['balance'] += 1000
    save_user_money(server_id, user_id, user_money)

    embed = discord.Embed(
        title='Bienvenue',
        description=f"Vous avez rejoint le serveur et vous avez reçu **1000** <a:money:1118983615418728508> \n Vous pouvez faire ?help economie pour plus d'information sur l'économie du serveur !"
    )
    await member.send(embed=embed)

payout_value = 1050000
payout_history = [(datetime.now(), payout_value)]


#####################################################################################################################
#                                                                                                                   #
#                                                                                                                   #
#                                                   LOTERIE : V1                                                    #
#                                               PAR PILOTE PRODUCTION                                               #
#                                                                                                                   #
#####################################################################################################################

def load_lottery_data(server_id):
    os.makedirs("data/loterie", exist_ok=True)
    file_path = f"data/loterie/{server_id}.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    else:
        return {"prize": 0, "tickets": {}}

def save_lottery_data(server_id, data):
    os.makedirs("data/loterie", exist_ok=True)
    file_path = f"data/loterie/{server_id}.json"
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

@bot.hybrid_group()
async def loterie(ctx):
    server_id = str(ctx.guild.id)
    data = load_lottery_data(server_id)
    prize = data["prize"]
    participants = len(data["tickets"])
    
    embed = discord.Embed(title="Loterie en cours", color=0x00ff00)
    embed.add_field(name="Lot à gagner", value=f"{prize} pièces", inline=False)
    embed.add_field(name="Nombre de participants", value=f"{participants} utilisateurs", inline=False)
    
    await ctx.send(embed=embed)

@loterie.command(name='buy')
async def loterie_buy(ctx, number_of_tickets: int):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)
    cost_per_ticket = 25000
    total_cost = number_of_tickets * cost_per_ticket
    
    user_money = load_user_money(server_id, user_id)
    user_balance = user_money.get("balance", 0)
    
    if user_balance < total_cost:
        embed = discord.Embed(title="Erreur", description=f"{ctx.author.mention} Vous n'avez pas assez d'argent pour acheter {number_of_tickets} tickets.", color=0xff0000)
        await ctx.send(embed=embed)
        return
    
    user_balance -= total_cost
    user_money["balance"] = user_balance
    save_user_money(server_id, user_id, user_money)
    
    data = load_lottery_data(server_id)
    if user_id in data["tickets"]:
        data["tickets"][user_id] += number_of_tickets
    else:
        data["tickets"][user_id] = number_of_tickets
    save_lottery_data(server_id, data)
    
    embed = discord.Embed(title="Achat de tickets", description=f"{ctx.author.mention} Vous avez acheté {number_of_tickets} tickets de loterie pour {total_cost} pièces.", color=0x00ff00)
    await ctx.send(embed=embed)

@loterie.command(name='create')
@commands.has_permissions(administrator=True)
async def loterie_create(ctx, prize: int):
    server_id = str(ctx.guild.id)
    data = load_lottery_data(server_id)
    data["prize"] = prize
    data["tickets"] = {}
    save_lottery_data(server_id, data)
    
    embed = discord.Embed(title="Loterie créée", description=f"Loterie créée avec un prix de {prize} pièces.", color=0x00ff00)
    await ctx.send(embed=embed)

@loterie.command(name='draw')
@commands.has_permissions(administrator=True)
async def loterie_draw(ctx):
    server_id = str(ctx.guild.id)
    data = load_lottery_data(server_id)
    
    if not data["tickets"]:
        embed = discord.Embed(title="Erreur", description="Aucun participant dans la loterie.", color=0xff0000)
        await ctx.send(embed=embed)
        return
    
    total_tickets = sum(data["tickets"].values())
    winning_ticket = random.randint(1, total_tickets)
    
    current_ticket = 0
    winner_id = None
    for user_id, tickets in data["tickets"].items():
        current_ticket += tickets
        if current_ticket >= winning_ticket:
            winner_id = user_id
            break
    
    if winner_id:
        winner_money = load_user_money(server_id, winner_id)
        winner_money["balance"] += data["prize"]
        save_user_money(server_id, winner_id, winner_money)
        
        embed = discord.Embed(title="Tirage au sort", description=f"Félicitations <@{winner_id}>! Vous avez gagné {data['prize']} pièces.", color=0x00ff00)
        await ctx.send(embed=embed)
        
        data["prize"] = 0
        data["tickets"] = {}
        save_lottery_data(server_id, data)
    else:
        embed = discord.Embed(title="Erreur", description="Erreur lors du tirage au sort.", color=0xff0000)
        await ctx.send(embed=embed)

@loterie.command(name='balance')
async def loterie_balance(ctx):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)
    data = load_lottery_data(server_id)
    total_tickets = sum(data["tickets"].values())
    user_tickets = data["tickets"].get(user_id, 0)
    user_spent = user_tickets * 25000
    if total_tickets > 0:
        winning_chance = (user_tickets / total_tickets) * 100
    else:
        winning_chance = 0.0
    
    embed = discord.Embed(title="Votre balance de loterie", color=0x00ff00)
    embed.add_field(name="Nombre de tickets", value=f"{user_tickets} tickets", inline=False)
    embed.add_field(name="Montant dépensé", value=f"{user_spent} pièces", inline=False)
    embed.add_field(name="Chance de gagner", value=f"{winning_chance:.2f}%", inline=False)
    
    await ctx.send(embed=embed)
#####################################################################################################################
#                                                                                                                   #
#                                                                                                                   #
#                                                 AUTOMATISATIONS : V1                                              #
#                                               PAR PILOTE PRODUCTION                                               #
#                                                                                                                   #
#####################################################################################################################

def load_automations(server_id):
    os.makedirs("data/automations", exist_ok=True)
    file_path = f"data/automations/{server_id}.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    else:
        return []

def save_automations(server_id, automations):
    os.makedirs("data/automations", exist_ok=True)
    file_path = f"data/automations/{server_id}.json"
    with open(file_path, "w") as file:
        json.dump(automations, file, indent=4)

@bot.group(invoke_without_command=True)
async def automation(ctx):
    await ctx.send("Veuillez utiliser l'une des sous-commandes : create, event.")

@automation.command()
@commands.has_permissions(administrator=True)
async def create(ctx, name):
    automations = load_automations(str(ctx.guild.id))
    for automation in automations:
        if automation["name"] == name:
            await ctx.send("Le nom de l'automatisation doit être unique.")
            return

    await ctx.send("À quelle heure souhaitez-vous que le message soit envoyé ? (format: HH:MM)")
    try:
        response = await bot.wait_for("message", timeout=60, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        time_str = response.content
        send_time = datetime.strptime(time_str, "%H:%M") - timedelta(hours=2)
        await ctx.send("Quel est le contenu du message à envoyer ?")
        message_content = (await bot.wait_for("message", timeout=60, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)).content

        automations.append({
            "name": name,
            "type": "message",
            "send_time": send_time.strftime("%H:%M"),
            "content": message_content,
            "last_executed": None,
            "channel_id": ctx.channel.id
        })
        save_automations(str(ctx.guild.id), automations)

        await ctx.send(f"L'automatisation '{name}' a été créée avec succès !")
    except asyncio.TimeoutError:
        await ctx.send("Temps écoulé, veuillez réessayer.")

@automation.command()
@commands.has_permissions(administrator=True)
async def event(ctx, name):
    automations = load_automations(str(ctx.guild.id))
    for automation in automations:
        if automation["name"] == name:
            await ctx.send("Le nom de l'automatisation doit être unique.")
            return

    await ctx.send("À quelle heure souhaitez-vous que l'événement soit programmé ? (format: HH:MM)")
    try:
        response = await bot.wait_for("message", timeout=60, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        time_str = response.content
        send_time = datetime.strptime(time_str, "%H:%M") - timedelta(hours=2)
        await ctx.send("Combien de récompenses voulez-vous offrir ?")
        amount = int((await bot.wait_for("message", timeout=60, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)).content)
        await ctx.send("Combien de personnes peuvent gagner ?")
        people_amount = int((await bot.wait_for("message", timeout=60, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)).content)

        automations.append({
            "name": name,
            "type": "event",
            "send_time": send_time.strftime("%H:%M"),
            "amount": amount,
            "people_amount": people_amount,
            "last_executed": None,
            "channel_id": ctx.channel.id
        })
        save_automations(str(ctx.guild.id), automations)

        await ctx.send("L'événement a été créé avec succès !")
    except asyncio.TimeoutError:
        await ctx.send("Temps écoulé, veuillez réessayer.")

async def loop_send_message():
    print("✅ | Les automatisations ont bien été démarrées.")
    while True:
        await asyncio.sleep(10)
        for guild in bot.guilds:
            automations = load_automations(str(guild.id))
            for automation in automations:
                send_time_str = automation["send_time"]
                send_time = datetime.strptime(send_time_str, "%H:%M")
                current_time = datetime.utcnow()
                last_executed = automation["last_executed"]
                if (current_time.hour == send_time.hour and current_time.minute == send_time.minute) or (last_executed is not None and current_time - datetime.strptime(last_executed, "%Y-%m-%d %H:%M:%S") < timedelta(minutes=15)):
                    if last_executed is not None and current_time - datetime.strptime(last_executed, "%Y-%m-%d %H:%M:%S") < timedelta(minutes=15):
                        continue
                    channel_id = automation["channel_id"]
                    channel = bot.get_channel(channel_id)
                    if channel:
                        if automation["type"] == "message":
                            await channel.send(automation["content"])
                            print("1 message envoyé")
                        elif automation["type"] == "event":
                            await drop_event(guild, channel, automation["amount"], automation["people_amount"])
                            print("1 événement exécuté")
                        automation["last_executed"] = current_time.strftime("%Y-%m-%d %H:%M:%S")
                        save_automations(str(guild.id), automations)
                    else:
                        print("Impossible de trouver le canal avec l'ID :", channel_id)

async def drop_event(guild, channel, amount, people_amount):
    embed = discord.Embed(title="Récompenses journalières (AUTOMATIQUE)", description=f"Les {people_amount} premières personnes qui réagissent à ce message avec la réaction <a:money:1118983615418728508> gagneront {amount} <a:money:1118983615418728508>.")
    message = await channel.send(embed=embed)
    await message.add_reaction("<a:money:1118983615418728508>")

    def check(reaction, user):
        return user != bot.user and str(reaction.emoji) == "<a:money:1118983615418728508>"

    try:
        reacted_users = []
        while len(reacted_users) < people_amount:
            reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
            if not user.bot and user not in reacted_users:
                reacted_users.append(user)
    except asyncio.TimeoutError:
        await channel.send("Temps écoulé, nombre insuffisant de personnes ayant réagi.")
    else:
        winners = []
        for user in reacted_users:
            user_data = load_user_money(str(guild.id), str(user.id))
            user_data["balance"] += amount
            save_user_money(str(guild.id), str(user.id), user_data)
            winners.append(user.mention)
        
        winners_text = "\n".join(winners)
        await channel.send(f"Les {people_amount} premières personnes ont gagné {amount} <a:money:1118983615418728508>:\n{winners_text}")

@bot.command()
async def time(ctx):
    current_time = datetime.now().strftime("%H:%M:%S")
    await ctx.send(f"L'heure actuelle est : {current_time}")

#####################################################################################################################
#                                                                                                                   #
#                                                                                                                   #
#                                                 RÉFÉRENCEMENT : V1                                                #
#                                               PAR PILOTE PRODUCTION                                               #
#                                                                                                                   #
#####################################################################################################################

@bot.group(name="referrals", description="Affiche les références de l'utilisateur.")
async def referrals(ctx):
    if ctx.guild.id != 1103936072989278279:
        return

    if ctx.invoked_subcommand is None:
        await ctx.send("Veuillez spécifier une sous-commande\n`/referrals show`\n`/referrals invite user_id`")

@referrals.command(name="show", description="Affiche les références de l'utilisateur.")
async def show_referrals(ctx):
    if ctx.guild.id != 1103936072989278279:
        return

    user_id = ctx.author.id
    referrals_id = str(user_id)
    user_invited_id_list = []
    referred_by = None
    counted = 0

    file_path = f"data/referrals/{user_id}.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            if data:
                referrals_id = data.get("referrals_id", str(user_id))
                user_invited_id_list = data.get("user_invited_id_list", [])
                referred_by = data.get("referred_by")
                counted = data.get("counted", 0)

    embed = discord.Embed(title="Références de l'utilisateur", color=discord.Color.blue())
    embed.add_field(name="Votre code personnel", value=referrals_id, inline=False)
    embed.add_field(name="Personnes invitées", value=counted, inline=False)
    if referred_by:
        embed.add_field(name="Référé par", value=referred_by, inline=False)
    await ctx.send(embed=embed)

@referrals.command(name="invite", description="Permet à un utilisateur référé d'inviter un autre utilisateur.")
async def invite_user(ctx, user_id: int):
    if ctx.guild.id != 1103936072989278279:
        return

    invited_id = ctx.author.id
    
    invited_filename = f"data/referrals/{invited_id}.json"
    if os.path.exists(invited_filename):
        with open(invited_filename, "r") as file:
            invited_data = json.load(file)
            if invited_data and invited_data.get("referred_by"):
                await ctx.send("Désolé, vous avez déjà mis le code de référence d'une autre personne.")
                return

    try:
        invited_member = await ctx.guild.fetch_member(user_id)
    except discord.NotFound:
        await ctx.send("L'utilisateur spécifié n'existe pas.")
        return

    inviter_filename = f"referrals/{user_id}.json"
    inviter_data = {"counted": 0, "user_invited_id_list": []}
    if os.path.exists(inviter_filename):
        with open(inviter_filename, "r") as file:
            inviter_data = json.load(file)
    inviter_data["counted"] += 1
    inviter_data["user_invited_id_list"].append(user_id)
    with open(inviter_filename, "w") as file:
        json.dump(inviter_data, file)

    invited_data = {}
    invited_data["referred_by"] = invited_member.display_name
    with open(invited_filename, "w") as file:
        json.dump(invited_data, file)

    await ctx.send(f"L'utilisateur {ctx.author.display_name} a été référé avec succès par {invited_member.display_name}.")

@referrals.command(name="claim", description="Réclame une récompense pour avoir invité des personnes.")
async def claim_reward(ctx):
    user_id = ctx.author.id

    file_path = f"data/referrals/{user_id}.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            counted = data.get("counted", 0)
            if counted < 3:
                await ctx.send("Désolé, vous devez inviter au moins 3 personnes pour réclamer la récompense.")
                return
            
            server_id = ctx.guild.id
            user_money = load_user_money(server_id, user_id)
            user_balance = user_money.get("balance", 0)
            user_balance += 100000
            user_money["balance"] = user_balance
            save_user_money(server_id, user_id, user_money)
            
            data["counted"] -= 3
            with open(file_path, "w") as file:
                json.dump(data, file)
            
            embed = discord.Embed(
                title="Récompense pour invitations",
                description="Vous avez réclamé avec succès la récompense pour avoir invité 3 personnes ! Vous avez reçu 100 000 pièces.",
                color=discord.Color.gold()
            )
            await ctx.send(embed=embed)
    else:
        await ctx.send("Désolé, vous devez inviter au moins 3 personnes pour réclamer la récompense.")



#####################################################################################################################
#                                                                                                                   #
#                                                                                                                   #
#                                                   TUTORIEL : V1                                                   #
#                                               PAR PILOTE PRODUCTION                                               #
#                                                                                                                   #
#####################################################################################################################

@bot.hybrid_group()
async def tutoriel(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Commande invalide. Utilisez `/tutoriel start` pour commencer le tutoriel.")

@tutoriel.command(name="start", description="Commence le tutoriel pour l'économie")
async def start_tutoriel(ctx):
    if not await check_tutorial_completion(ctx.author.id):
        await ctx.send("Bienvenue sur l'économie de Pilote Studio ! Commençons par les bases :\nLa commande ?balance permet de voir votre solde actuel en pièces rouges.")

        await asyncio.sleep(0.5)
        await mark_tutorial_complete(ctx.author.id)

        await ctx.send("Pour voir votre solde, essayez la commande maintenant : **?balance**\nAttention, les commandes avec les slashs commands ne sont pas comptabilisées pour le moment. Utilisez les commandes avec le préfixe ? à la place.")

        def check(m):
            return m.content.startswith('?balance') and m.channel == ctx.channel and m.author == ctx.author

        try:
            msg = await bot.wait_for('message', timeout=90.0, check=check)
            if not msg.content.startswith('?balance'):
                await ctx.send("Vous devez exécuter la commande ?balance pour continuer.")
                await mark_tutorial_unfinished(ctx.author.id)
                return

            await asyncio.sleep(1)
            await ctx.send("Parfait ! Vous pouvez voir que vous avez environ **1000 pièces !** Il s'agit de l'argent attribué lorsque vous rejoignez le serveur.")
            await ctx.send("Maintenant, nous allons commencer à gagner de l'argent. Il existe plusieurs méthodes, notamment celles dites actives, qui permettent de gagner de l'argent assez rapidement. Pour continuer ce tutoriel, exécutez la commande **?work**. Ensuite cliquez sur une des différentes réactions disponible sur le message renvoyé par le robot.")

            await bot.wait_for('message', timeout=90.0, check=lambda m: m.content.startswith('?work') and m.channel == ctx.channel and m.author == ctx.author)
            await asyncio.sleep(5)
            await ctx.send("Parfait ! Vous venez d'obtenir de l'argent en travaillant.")
            await ctx.send("Maintenant, nous allons commencer à gagner de l'argent autrement. Pour continuer ce tutoriel, exécutez la commande **?mineurs**.")

            await bot.wait_for('message', timeout=90.0, check=lambda m: m.content.startswith('?mineurs') and m.channel == ctx.channel and m.author == ctx.author)
            await asyncio.sleep(3)
            await ctx.send("Parfait ! Vous pouvez probablement comprendre le fonctionnement des mineurs en cliquant [ici](https://discord.com/channels/1103936072989278279/1138820990898544683/1232774300420014171).")
            await ctx.send("Il existe d'autres méthodes pour gagner de l'argent. Pour continuer ce tutoriel, exécutez la commande **?help economie**.")

            await bot.wait_for('message', timeout=90.0, check=lambda m: m.content.startswith('?help economie') and m.channel == ctx.channel and m.author == ctx.author)
            await asyncio.sleep(5)
            await ctx.send("Maintenant, vous avez tous les outils pour réussir sur notre système d'économie.")
            await ctx.send("Vous pouvez gagner des récompenses dans la vie réelle en utilisant la commande **?payout** ou d'autres récompenses en utilisant la commande **?rewards**.")
            await ctx.send("Comme vous avez terminé le tutoriel, voici votre récompense :")

            server_id = ctx.guild.id
            user_id = ctx.author.id
            user_money = load_user_money(server_id, user_id)
            user_balance = user_money.get("balance", 0)
            work_amount = random.randint(0, 15000)
            user_balance += work_amount
            user_money["balance"] = user_balance
            save_user_money(server_id, user_id, user_money)

            embed = discord.Embed(
                title="Récompense tutoriel",
                description=f"Vous avez fait le tutoriel et nous vous offrons {work_amount} <a:money:1118983615418728508> pour le début de votre aventure !",
                color=discord.Color.gold()
            )
            await ctx.send(embed=embed)
            await ctx.send("Bon jeu sur Pilote Community !")

            await mark_tutorial_complete(ctx.author.id)

        except asyncio.TimeoutError:
            await ctx.send("Le tutoriel a expiré. Le tutoriel est annulé.")
            await mark_tutorial_unfinished(ctx.author.id)
    else:
        await ctx.send("Vous avez déjà terminé le tutoriel.")
    

@tutoriel.command(name="skip", description="Passe le tutoriel (pour les utilisateurs avancés)")
async def skip_tutoriel(ctx):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)
    try:
        with open(f"data/tutoriel/{user_id}.json", "r") as file:
            data = json.load(file)
            data["tutorial"] = True
        with open(f"data/tutoriel/{user_id}.json", "w") as file:
            json.dump(data, file)
        await ctx.send(f"Vous avez passé le tutoriel. :(")
    except FileNotFoundError:
        data = {"tutorial": True}
        with open(f"data/tutoriel/{user_id}.json", "w") as file:
            json.dump(data, file)
    await ctx.send(f"Vous avez passé le tutoriel. :(")

@tutoriel.command(name="set")
async def set_tutorial(ctx, action=None, user: discord.User = None):
    if ctx.author.guild_permissions.administrator:
        if action == "finished":
            await mark_tutorial_complete(user.id)
            await ctx.send(f"Le tutoriel pour {user.mention} a été marqué comme terminé.")
        elif action == "unfinished":
            await mark_tutorial_unfinished(user.id)
            await ctx.send(f"Le tutoriel pour {user.mention} a été marqué comme non terminé.")
        else:
            await ctx.send("Commande invalide. Utilisez `/tutoriel set finished user` ou `/tutoriel set unfinished user`.")
    else:
        await ctx.send("Vous n'avez pas les autorisations nécessaires pour utiliser cette commande.")

async def mark_tutorial_complete(user_id):
    try:
        os.makedirs("tutoriel", exist_ok=True)
        with open(f"data/tutoriel/{user_id}.json", "r") as file:
            data = json.load(file)
            data["tutorial"] = True
        with open(f"data/tutoriel/{user_id}.json", "w") as file:
            json.dump(data, file)
    except FileNotFoundError:
        data = {"tutorial": True}
        with open(f"data/tutoriel/{user_id}.json", "w") as file:
            json.dump(data, file)

async def mark_tutorial_unfinished(user_id):
    try:
        os.makedirs("tutoriel", exist_ok=True)
        with open(f"data/tutoriel/{user_id}.json", "r") as file:
            data = json.load(file)
            data["tutorial"] = False
        with open(f"data/tutoriel/{user_id}.json", "w") as file:
            json.dump(data, file)
    except FileNotFoundError:
        data = {"tutorial": False}
        with open(f"data/tutoriel/{user_id}.json", "w") as file:
            json.dump(data, file)

#####################################################################################################################
#                                                                                                                   #
#                                                                                                                   #
#                                                     MINEURS : V1                                                  #
#                                               PAR PILOTE PRODUCTION                                               #
#                                                                                                                   #
#####################################################################################################################

def server_members(server_id):
    guild = bot.get_guild(int(server_id))
    return guild.members

def get_total_normal_money(server_id):
    total_normal_money = 0
    for member in server_members(server_id):
        user_money_normal = load_user_money(server_id, str(member.id))
        user_balance_normal = user_money_normal.get("balance", 0)
        total_normal_money += user_balance_normal
    return total_normal_money

def get_total_red_money(server_id):
    total_red_money = 0
    for member in server_members(server_id):
        user_money_red = load_user_earning_money(server_id, str(member.id))
        user_balance_red = user_money_red.get("balance", 0)
        total_red_money += user_balance_red
    return total_red_money

def load_user_earning_money(server_id, user_id):
    filename = f"data/mineurs/red/{server_id}/{user_id}.json"
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        os.makedirs(f"data/mineurs/red/{server_id}", exist_ok=True)
        data = {"balance": 0}
        with open(filename, "w") as file:
            json.dump(data, file)
    return data

def save_user_earning_money(server_id, user_id, data):
    os.makedirs(f"data/mineurs/red/{server_id}", exist_ok=True)  
    filename = f"data/mineurs/red/{server_id}/{user_id}.json"
    with open(filename, "w") as file:
        json.dump(data, file)

def load_user_earning(server_id, user_id):
    filename = f"data/mineurs/{server_id}/{user_id}.json"
    try:
        with open(filename, "r") as file:
            if os.path.getsize(filename) == 0:
                raise FileNotFoundError
            data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        os.makedirs(f"data/mineurs/{server_id}", exist_ok=True)
        data = {
            "stone_ore": 0, "stone_level": 2,
            "andesite_ore": 0, "andesite_level": 0,
            "coal_ore": 0, "coal_level": 0,
            "iron_ore": 0, "iron_level": 0,
            "platinium_ore": 0, "platinium_level": 0,
            "gold_ore": 0, "gold_level": 0,
            "titanium_ore": 0, "titanium_level": 0,
            "palladium_ore": 0, "palladium_level": 0,
            "ruby_ore": 0, "ruby_level": 0,
            "emerald_ore": 0, "emerald_level": 0,
            "diamond_ore": 0, "diamond_level": 0,
            "uranium_ore": 0, "uranium_level": 0,
            "radium_ore": 0, "radium_level": 0,
            "pilodium_ore": 0, "pilodium_level": 0,
            "pilodium_unlocked": 0, "*": 1
        }
        with open(filename, "w") as file:
            json.dump(data, file)
    new_minerals = {"max_ore": 1}
    for mineral, default_value in new_minerals.items():
        if mineral not in data:
            data[mineral] = default_value
    return data

def save_user_earning(server_id, user_id, data):
    os.makedirs(f"data/mineurs/{server_id}", exist_ok=True)  
    filename = f"data/mineurs/{server_id}/{user_id}.json"
    with open(filename, "w") as file:
        json.dump(data, file)

async def mine_on_seconds():
    print("✅ | Les mineurs ont été démarrés.")
    while True:
        for server_id in os.listdir("data/mineurs"):
            if not server_id.isdigit():
                continue
            server_path = os.path.join("data/mineurs", server_id)
            guild = bot.get_guild(int(server_id))
            if guild is None:
                continue
            for user_file in os.listdir(server_path):
                if user_file.endswith('.json'):
                    user_id = user_file[:-5]
                    if user_id.isdigit():
                        member = guild.get_member(int(user_id))
                        """if member is None or member.status == discord.Status.offline:
                            continue"""
                        user_data = load_user_earning(server_id, user_id)
                        minerals = {
                            "stone": {"base_probability": 0.01, "level_factor": 1.05},
                            "andesite": {"base_probability": 0.01, "level_factor": 1.05},
                            "coal": {"base_probability": 0.008, "level_factor": 1.05},
                            "iron": {"base_probability": 0.007, "level_factor": 1.05},
                            "platinium": {"base_probability": 0.006, "level_factor": 1.04},
                            "gold": {"base_probability": 0.005, "level_factor": 1.03},
                            "titanium": {"base_probability": 0.004, "level_factor": 1.02},
                            "palladium": {"base_probability": 0.003, "level_factor": 1.01},
                            "ruby": {"base_probability": 0.002, "level_factor": 1.008},
                            "emerald": {"base_probability": 0.001, "level_factor": 1.005},
                            "diamond": {"base_probability": 0.0009, "level_factor": 1.005},
                            "uranium": {"base_probability": 0.00075, "level_factor": 1.005},
                            "radium": {"base_probability": 0.0005, "level_factor": 1.001},
                            "pilodium": {"base_probability": 0.0003, "level_factor": 1.0001}
                        }
                        for mineral, params in minerals.items():
                            level = user_data.get(f"{mineral}_level", 0)
                            if level > 0:
                                probability_factor = 0.01
                                if level > 1:
                                    base_probability = params["base_probability"]
                                    level_factor = params["level_factor"] ** (level - 1)
                                    probability_factor = base_probability * level_factor
                                if probability_factor >= 1:
                                    num_ore = int(probability_factor)
                                    extra_chance = probability_factor - num_ore

                                    for _ in range(num_ore):
                                        ore_amount = user_data.get(f"{mineral}_ore", 0)
                                        user_data[f"{mineral}_ore"] = ore_amount + 1
                                    if random.random() < extra_chance:
                                        ore_amount = user_data.get(f"{mineral}_ore", 0)
                                        user_data[f"{mineral}_ore"] = ore_amount + 1
                                else:
                                    if random.random() < probability_factor:
                                        ore_amount = user_data.get(f"{mineral}_ore", 0)
                                        user_data[f"{mineral}_ore"] = ore_amount + 1

                            if level == 1:
                                user_data[f"{mineral}_level"] = 2
                                print(f"User {user_id} on server {server_id} upgraded from level 1 to level 2.")

                            max_ore = user_data.get(f"max_ore", 0)
                            max_ore *= 100
                            if user_data.get(f"{mineral}_ore", 0) > max_ore:
                                user_data[f"{mineral}_ore"] = max_ore

                        save_user_earning(server_id, user_id, user_data)
        await asyncio.sleep(3)

@bot.hybrid_group(description="Affiche ton solde de minerais", invoke_without_command=True)
async def mineurs(ctx, user: discord.User = None):
    if user is None:
        user = ctx.author
    
    user_id = user.id
    server_id = str(ctx.guild.id)
    
    settings_embed = await check_settings(server_id, user_id)
    if settings_embed is not None:
        await ctx.send(embed=settings_embed)
        return
    
    user_data = load_user_earning(str(ctx.guild.id), str(user.id))
    
    max_ore = user_data.get("max_ore", 0)
    max_ore *= 100
    total_ore = 0
    unlocked_minerals_count = 0

    embed = discord.Embed(title="Vos minerais ⛏️", description=f"{user.mention} a actuellement :\n")

    emojis = {
        "stone": "🪨",
        "andesite": "⛏️",
        "coal": "⚫",
        "iron": "🪛",
        "platinium": "🏅",
        "gold": "🥇",
        "titanium": "⚙️",
        "palladium": "💽",
        "ruby": "❤️",
        "emerald": "💚",
        "diamond": "💎",
        "uranium": "☢️",
        "radium": "☢️",
        "pilodium": "✨"
    }

    minerals = {
        "stone": {"base_probability": 0.01, "level_factor": 1.05},
        "andesite": {"base_probability": 0.01, "level_factor": 1.05},
        "coal": {"base_probability": 0.008, "level_factor": 1.05},
        "iron": {"base_probability": 0.007, "level_factor": 1.05},
        "platinium": {"base_probability": 0.006, "level_factor": 1.04},
        "gold": {"base_probability": 0.005, "level_factor": 1.03},
        "titanium": {"base_probability": 0.004, "level_factor": 1.02},
        "palladium": {"base_probability": 0.003, "level_factor": 1.01},
        "ruby": {"base_probability": 0.002, "level_factor": 1.008},
        "emerald": {"base_probability": 0.001, "level_factor": 1.005},
        "diamond": {"base_probability": 0.0009, "level_factor": 1.005},
        "uranium": {"base_probability": 0.00075, "level_factor": 1.005},
        "radium": {"base_probability": 0.0005, "level_factor": 1.001},
        "pilodium": {"base_probability": 0.0003, "level_factor": 1.0001}
    }

    for mineral, params in minerals.items():
        ore_amount = user_data.get(f"{mineral}_ore", 0)
        level = user_data.get(f"{mineral}_level", 0)
        
        if mineral == "stone" or user_data.get(f"{list(minerals.keys())[list(minerals.keys()).index(mineral) - 1]}_level", 0) >= (5 + (list(minerals.keys()).index(mineral) - 1) * 5):
            if level > 0:
                base_probability = params["base_probability"]
                level_factor = params["level_factor"] ** (level - 1)
                efficiency_percentage = base_probability * level_factor / params["base_probability"] * 100

                inventory_status = ""
                if ore_amount >= max_ore:
                    inventory_status = "**INVENTAIRE PLEIN**"
                
                total_ore += ore_amount
                unlocked_minerals_count += 1
                
                embed.add_field(
                    name=f"{emojis[mineral]} {mineral.capitalize()} (niveau {level})",
                    value=f"{ore_amount} minerais\nEfficacité: {efficiency_percentage:.2f}%\n{inventory_status}",
                    inline=True
                )
        else:
            if ore_amount > 0:
                inventory_status = ""
                if ore_amount >= max_ore:
                    inventory_status = "**INVENTAIRE PLEIN**"
                
                total_ore += ore_amount

                if level > 0:
                    efficiency_percentage = base_probability * level_factor / params["base_probability"] * 100
                    embed.add_field(
                        name=f"{emojis[mineral]} {mineral.capitalize()} (niveau {level}) **NON-DÉBLOQUÉ**",
                        value=f"{ore_amount} minerais\nEfficacité: {efficiency_percentage:.2f}%\nMinerais non débloqué, bien joué c'est très rare.\n{inventory_status}",
                        inline=True
                    )
                else:
                    embed.add_field(
                        name=f"{emojis[mineral]} {mineral.capitalize()} (niveau {level}) **NON-DÉBLOQUÉ**",
                        value=f"{ore_amount} minerais\nMinerais non débloqué, bien joué c'est très rare.\n{inventory_status}",
                        inline=True
                    )

    if unlocked_minerals_count > 0:
        usage_percentage = (total_ore / (max_ore * unlocked_minerals_count)) * 100
    else:
        usage_percentage = 0

    embed.description = f"Vous utilisez actuellement `{total_ore}/{max_ore * unlocked_minerals_count} ({usage_percentage:.2f}%)` minerais\n{embed.description}"

    advice = random.choice([
        "Investissez dans l'amélioration de vos mines pour augmenter vos revenus passifs ! 💰",
        "Explorez de nouvelles opportunités commerciales en achetant des niveaux de minerais ! ⛏️",
        "Gardez un œil sur le marché pour vendre vos minerais au meilleur prix ! 📈",
        "📈: Si Pilote Production est le plus fort, c'est à cause de son charisme ! ❤️"
    ])
    
    embed.add_field(name="Conseil du jour", value=advice, inline=False)

    await ctx.send(embed=embed)


@mineurs.command(name="upgrade", description="Améliore le nombre maximal de minerais que vous pouvez posséder.")
async def upgrade(ctx):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)
    user_data = load_user_earning(server_id, user_id)

    max_ore = user_data.get("max_ore", 1)
    cost = max_ore * 1000

    user_money = load_user_earning_money(server_id, user_id)
    balance = user_money.get("balance", 0)
    
    if balance >= cost:
        balance -= cost
        user_money["balance"] = balance 
        user_data["max_ore"] += 1

        save_user_earning_money(server_id, user_id, user_money)
        save_user_earning(server_id, user_id, user_data)
        
        max_ore_multiplier = max_ore * 100
        embed = discord.Embed(
            title="Amélioration réussie !",
            description=f"Félicitations {ctx.author.mention}, votre capacité maximale de minerais a été augmentée à {max_ore_multiplier + 100} pour {cost} <a:redmoney:1253303769698140272>.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Échec de l'amélioration",
            description=f"Désolé {ctx.author.mention}, vous n'avez pas assez d'argent pour améliorer. Il vous faut {cost} <a:redmoney:1253303769698140272>.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)


@mineurs.command(name='list', description="Affiche les niveaux achetables pour chaque minerai.")
async def upgrade_list(ctx):
    user_data = load_user_money(str(ctx.guild.id), str(ctx.author.id))
    user_data_earning = load_user_earning(str(ctx.guild.id), str(ctx.author.id))
    embed = discord.Embed(title="Niveaux achetables ⛏️", description="Voici les niveaux de minerais achetables :", color=discord.Color.blue())
    minerals_prices = {
        "stone": 75,
        "andesite": 150,
        "coal": 200,
        "iron": 7500,
        "platinium": 15000,
        "gold": 20000,
        "titanium": 25000,
        "palladium": 30000,
        "ruby": 40000,
        "emerald": 50000,
        "diamond": 75000,
        "uranium": 100000,
        "radium": 150000,
        "pilodium": 200000
    }
    for mineral, price in minerals_prices.items():
        current_level = user_data_earning.get(f"{mineral}_level", 0)
        if mineral == "stone" or user_data_earning.get(f"{list(minerals_prices.keys())[list(minerals_prices.keys()).index(mineral) - 1]}_level", 0) >= (5 + (list(minerals_prices.keys()).index(mineral) - 1) * 5):
            next_level_price = price + (current_level + 1) * 1000
            embed.add_field(name=f"{mineral.capitalize()} Level {current_level + 1}", value=f"Prix : {next_level_price}", inline=False)
    await ctx.send(embed=embed)

@mineurs.command(name='buy', description="Achète et met à niveau un niveau de minerai spécifié.")
async def upgrade_buy(ctx, mineral: str):
    user_data = load_user_money(str(ctx.guild.id), str(ctx.author.id))
    user_data_earning = load_user_earning(str(ctx.guild.id), str(ctx.author.id))
    minerals_prices = {
        "stone": 75,
        "andesite": 150,
        "coal": 200,
        "iron": 7500,
        "platinium": 15000,
        "gold": 20000,
        "titanium": 25000,
        "palladium": 30000,
        "ruby": 40000,
        "emerald": 50000,
        "diamond": 75000,
        "uranium": 100000,
        "radium": 150000,
        "pilodium": 200000
    }
    if mineral not in minerals_prices:
        await ctx.send("Minerai invalide.")
        return
    
    current_level = user_data_earning.get(f"{mineral}_level", 0)
    if mineral != "stone":
        previous_mineral = list(minerals_prices.keys())[list(minerals_prices.keys()).index(mineral) - 1]
        previous_level = user_data_earning.get(f"{previous_mineral}_level", 0)
        previous_level_req = 5 + (list(minerals_prices.keys()).index(mineral) - 1) * 5
        if previous_level < previous_level_req:
            await ctx.send(f"Vous devez débloquer le niveau {previous_level_req} de {previous_mineral.capitalize()} avant de pouvoir acheter ce niveau.")
            return
    
    next_level_price = minerals_prices[mineral] + (current_level + 1) * 1000
    if user_data["balance"] >= next_level_price:
        user_data["balance"] -= next_level_price
        user_data_earning[f"{mineral}_level"] = current_level + 1
        save_user_money(str(ctx.guild.id), str(ctx.author.id), user_data)
        save_user_earning(str(ctx.guild.id), str(ctx.author.id), user_data_earning)
        await ctx.send(f"Vous avez acheté avec succès le niveau {current_level + 1} de {mineral.capitalize()} !")
    else:
        await ctx.send("Vous n'avez pas assez d'argent pour acheter ce niveau.")


@mineurs.command(name='sell', description="Vend des minerais contre de l'argent")
async def sell_minerals(ctx, mineral: str = None, quantity: str = None):
    if mineral == "all":
        await sell_all_minerals(ctx)
    else:
        await sell_minerals(ctx, mineral, quantity)


@mineurs.command(name='set', description="Pour les administrateurs")
async def set_mine_value(ctx, quantity: str = None):
    if ctx.author.guild_permissions.administrator:
        global mine_value
        mine_value = float(quantity)
        await ctx.send(f"La valeur de vente à bien été définie à {quantity}")

async def sell_minerals(ctx, mineral, quantity):
    user_data_earning_money = load_user_earning_money(str(ctx.guild.id), str(ctx.author.id))
    user_data_earning = load_user_earning(str(ctx.guild.id), str(ctx.author.id))
    global mine_value

    mineral_prices = {
        "stone": 1,
        "andesite": 2,
        "coal": 5,
        "iron": 8,
        "platinium": 10,
        "gold": 20,
        "titanium": 25,
        "palladium": 30,
        "ruby": 42,
        "emerald": 45,
        "diamond": 50,
        "uranium": 75,
        "radium": 500,
        "pilodium": 1000
    }
    
    if mineral not in mineral_prices:
        await ctx.send("Minerai invalide. ⛏️ `/mineurs list`")
        return

    if f"{mineral}_ore" not in user_data_earning:
        await ctx.send("Vous ne possédez pas ce type de minerai.")
        return

    if user_data_earning[f"{mineral}_ore"] < int(quantity):
        await ctx.send("Vous n'avez pas suffisamment de minerais de ce type.")
        return

    price_per_unit = mineral_prices[mineral]
    total_price = price_per_unit * int(quantity)
    mine_value += total_price * 0.00005

    if mine_value > 5:
        mine_value = 5

    user_data_earning[f"{mineral}_ore"] -= int(quantity)
    user_data_earning_money["balance"] += total_price

    save_user_earning_money(str(ctx.guild.id), str(ctx.author.id), user_data_earning_money)
    save_user_earning(str(ctx.guild.id), str(ctx.author.id), user_data_earning)
    
    await ctx.send(f"Vous avez vendu {quantity} {mineral} pour {total_price} <a:redmoney:1253303769698140272>.")



async def sell_all_minerals(ctx):

    global mine_value

    mineral_prices = {
        "stone": 1,
        "andesite": 2,
        "coal": 5,
        "iron": 8,
        "platinium": 10,
        "gold": 20,
        "titanium": 30,
        "palladium": 35,
        "ruby": 40,
        "emerald": 45,
        "diamond": 50,
        "uranium": 75,
        "radium": 500,
        "pilodium": 1000
    }

    user_data_earning_money = load_user_earning_money(str(ctx.guild.id), str(ctx.author.id))
    user_data_earning = load_user_earning(str(ctx.guild.id), str(ctx.author.id))

    total_earnings = 0
    sold_minerals_details = []

    for mineral, price_per_unit in mineral_prices.items():
        if f"{mineral}_ore" in user_data_earning:
            quantity = user_data_earning[f"{mineral}_ore"]

            if quantity > 0:
                total_price = price_per_unit * quantity

                user_data_earning[f"{mineral}_ore"] = 0
                user_data_earning_money["balance"] += total_price

                sold_minerals_details.append(f"{quantity} {mineral} pour {total_price} <a:redmoney:1253303769698140272>")
                total_earnings += total_price

    save_user_earning_money(str(ctx.guild.id), str(ctx.author.id), user_data_earning_money)
    save_user_earning(str(ctx.guild.id), str(ctx.author.id), user_data_earning)

    if sold_minerals_details:
        details_message = "\n".join(sold_minerals_details)
        await ctx.send(f"Vous avez vendu tous vos minerais pour un total de {total_earnings} <a:redmoney:1253303769698140272> :\n{details_message}")
    else:
        await ctx.send("Vous ne possédez aucun minerai à vendre.")

@mineurs.group()
async def sellout(ctx):
    if ctx.invoked_subcommand is None:
        embed = discord.Embed(title="Sous commande invalide", color=discord.Color.blue())
        embed.add_field(name="Tutoriel", value=f"Vous pouvez vendre avec la commande `/mineurs sellout sell NOMBRE` !")
        await ctx.send(embed=embed)

mine_value = 1
mine_history = [(datetime.now(), mine_value)]

@sellout.command(name="sell")
@commands.cooldown(1, 60*5, commands.BucketType.user)
async def sellout_sell(ctx, quantity: int):
    server_id = ctx.guild.id
    user_id = ctx.author.id

    user_money = load_user_money(server_id, user_id)
    user_balance = user_money.get("balance", 0)
    user_money_red = load_user_earning_money(server_id, user_id)
    user_balance_red = user_money_red.get("balance", 0)
    
    if quantity <= 0:
        await ctx.send("La quantité doit être supérieure à zéro.")
        return
    
    if user_balance_red < quantity:
        await ctx.send("Vous n'avez pas assez de pièces à vendre.")
        return
    
    mine_value = random.uniform(0.5, 5)
    total_payout = quantity * mine_value
    
    user_money_red["balance"] -= quantity
    user_money["balance"] += round(total_payout)
    
    save_user_money(server_id, user_id, user_money)
    save_user_earning_money(server_id, user_id, user_money_red)
    
    embed = discord.Embed(title="Vente réussie", color=discord.Color.green())
    embed.add_field(name="Quantité vendue", value=f"{quantity} <a:redmoney:1253303769698140272>")
    embed.add_field(name="Gain total", value=f"{total_payout:.0f} <a:money:1118983615418728508>")
    embed.add_field(name="Taux de vente", value=f"{mine_value:.2f} <a:money:1118983615418728508>/<a:redmoney:1253303769698140272>")
    await ctx.send(embed=embed)


@mineurs.command(name="balance", aliases=["bal"], description="Affiche ton solde actuel")
async def balance_red(ctx, user: discord.User = None):
    if user is None:
        user = ctx.author
    user_id = ctx.author.id
    server_id = str(ctx.guild.id)
    ban_info = check_user_ban_status(server_id, user_id)
    if ban_info is not None:
        reason, admin_id = ban_info
        admin = bot.get_user(admin_id)
        embed = discord.Embed(title="Compte Monétaire suspendu", description=f"Votre compte monétaire à été suspendu.\nRaison : {reason}\nSanction appliquée par : {admin.mention}\n Si vous souhaitez contester cette sanction, [Cliquez-ici](https://discord.com/channels/1103936072989278279/1103936074134339639)", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    amount = "none"
    user_data = load_user_earning_money(str(ctx.guild.id), str(user.id))
    balance = user_data["balance"]
    embed = discord.Embed(title="Balance", description=f"{user.mention} a actuellement **{balance} <a:redmoney:1253303769698140272>**")
    await ctx.send(embed=embed)

@mineurs.command(name="setlevel", hidden=True)
async def set_miner_level(ctx, user: discord.User, mineral: str, level: int):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("Vous n'avez pas les autorisations nécessaires pour utiliser cette commande.")
        return
    
    server_id = str(ctx.guild.id)
    user_id = str(user.id)
    user_data_earning = load_user_earning(server_id, user_id)

    if f"{mineral}_level" not in user_data_earning:
        await ctx.send("Minerai invalide.")
        return

    user_data_earning[f"{mineral}_level"] = level

    save_user_earning(server_id, user_id, user_data_earning)

    await ctx.send(f"Le niveau de {mineral} pour {user.mention} a été défini sur {level}.")

@mineurs.command(name="setminerais", hidden=True)
async def set_minerais(ctx, user: discord.User, mineral: str, quantity: int):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("Vous n'avez pas les autorisations nécessaires pour utiliser cette commande.")
        return
    
    server_id = str(ctx.guild.id)
    user_id = str(user.id)
    user_data_earning = load_user_earning(server_id, user_id)

    if f"{mineral}_ore" not in user_data_earning:
        await ctx.send("Minerai invalide.")
        return

    user_data_earning[f"{mineral}_ore"] = quantity

    save_user_earning(server_id, user_id, user_data_earning)

    await ctx.send(f"La quantité de {mineral} pour {user.mention} a été définie sur {quantity}.")


#####################################################################################################################
#                                                                                                                   #
#                                                                                                                   #
#                                                 ÉVENEMENTS : V1                                                   #
#                                               PAR PILOTE PRODUCTION                                               #
#                                                                                                                   #
#####################################################################################################################

cooldowns_ticket = {}
cooldowns_ticket_pay = {}

@bot.hybrid_group()
async def summer(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Veuillez spécifier une sous-commande valide.")

@summer.command(name="balance", description="Affiche le nombre de tickets de l'utilisateur")
async def ticket_balance(ctx):
    user_id = ctx.author.id
    server_id = str(ctx.guild.id)
    return
    ticket_data = load_ticket_data(server_id, user_id)
    
    ticket_count = ticket_data.get('ticket_count', 0)
    
    embed = discord.Embed(
        title="Balance de tickets - SummerTime !",
        description=f"Vous avez `{ticket_count}` jetons d'été.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@summer.command(name="claim", description="Obtiens un jeton gratuit de l'évenement temporaire")
async def ticket_claim(ctx):
    user_id = ctx.author.id
    server_id = str(ctx.guild.id)
    return
    user_money = load_user_money(server_id, user_id)
    user_balance = user_money.get("balance", 0)
    ticket_data = load_ticket_data(server_id, user_id)
    
    if 'ticket_count' not in ticket_data:
        ticket_data['ticket_count'] = 0
        
    if user_id in cooldowns_ticket:
        cooldown_time = cooldowns_ticket[user_id]
        time_remaining = cooldown_time - datetime.now()

        if time_remaining.total_seconds() > 0:
            embed = discord.Embed(
                title="Erreur - SummerTime !",
                description=f"Vous êtes en cooldown. Veuillez réessayer dans {time_remaining}.",
                color=discord.Color.yellow()
            )
            await ctx.send(embed=embed)
            return

    ticket_data['ticket_count'] += 1
    save_ticket_data(server_id, user_id, ticket_data)
    embed = discord.Embed(
        title="Récupéré - SummerTime !",
        description=f"Vous avez eu `1 jeton d'été`!",
        color=discord.Color.yellow()
    )
    await ctx.send(embed=embed)
    cooldowns_ticket[user_id] = datetime.now() + timedelta(hours=6)

"""    
@summer.command(name="pay", description="Paye des tickets")
async def ticket_pay(ctx, quantity: int):
    user_id = ctx.author.id
    server_id = str(ctx.guild.id)
    
    if ctx.guild.id != 1103936072989278279:
        await ctx.send("La commande n'est pas disponible sur les autres serveurs")
        return
    
    ticket_data = load_ticket_data(server_id, user_id)
    user_money = load_user_money(server_id, user_id)
    user_balance = user_money.get("balance", 0)

    ban_info = check_user_ban_status(server_id, user_id)
    if ban_info is not None:
        reason, admin_id = ban_info
        admin = bot.get_user(admin_id)
        embed = discord.Embed(title="Compte Monétaire suspendu", description=f"Votre compte monétaire à été suspendu.\nRaison : {reason}\nSanction appliquée par : {admin.mention}\n Si vous souhaitez contester cette sanction, [Cliquez-ici](https://discord.com/channels/1103936072989278279/1103936074134339639)", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    if ctx.guild.id != 0:
        await ctx.send("End")
        return
    if 'ticket_count' not in ticket_data:
        ticket_data['ticket_count'] = 0

    if user_balance <= 2500 * quantity:
        embed = discord.Embed(title="Achat - Évenement", description="Vous n'avez pas assez d'argent pour participer !", color=discord.Color.yellow())
        await ctx.send(embed=embed)
        return

    total_cost = 2500 * quantity
    user_balance -= total_cost
    user_money["balance"] = user_balance
    save_user_money(server_id, user_id, user_money)

    embed = discord.Embed(
        title="Évenement",
        description=f"Vous avez reçu **{quantity}** tickets !",
        color=discord.Color.yellow()
    )
    ticket_data['ticket_count'] += quantity
    save_ticket_data(server_id, user_id, ticket_data)
    await ctx.send(embed=embed)
    cooldowns_ticket_pay[user_id] = datetime.now() + timedelta(minutes=30)
"""


@summer.command(name="roulette", description="Lance la roulette évenement")
async def ticket_roulette(ctx, number: int = None):
    global payout_value
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)
    user_money = load_user_money(server_id, user_id)
    user_balance = user_money.get("balance", 0)
    ticket_data = load_ticket_data(server_id, user_id)
    return
    if ctx.guild.id != 1103936072989278279:
        await ctx.send("La commande n'est pas disponible sur les autres serveurs")
        return
        
    ban_info = check_user_ban_status(server_id, user_id)
    if ban_info is not None:
        reason, admin_id = ban_info
        admin = bot.get_user(admin_id)
        embed = discord.Embed(title="Compte Monétaire suspendu", description=f"Votre compte monétaire à été suspendu.\nRaison : {reason}\nSanction appliquée par : {admin.mention}\n Si vous souhaitez contester cette sanction, [Cliquez-ici](https://discord.com/channels/1103936072989278279/1103936074134339639)", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    if 'ticket_count' not in ticket_data:
        ticket_data['ticket_count'] = 0
    save_ticket_data(server_id, user_id, ticket_data)

    if ticket_data['ticket_count'] < 1:
        await ctx.send("Vous n'avez pas de ticket pour jouer à la roulette.")
        return

    ticket_data['ticket_count'] -= 1
    save_ticket_data(server_id, user_id, ticket_data)
    
    message = await ctx.send("Rappel : Les meilleures récompenses sont :\n1. Un Discord Nitro annuel \n2. 1 Discord Nitro Mensuel\n3. Un code de promotion Pilote Shopping\n4. Un grade première classe offert 1 mois\n5. 1 million de pièce.\n6. Des mineurs gratuit\nMais aussi des malus important, alors bon jeu à tous et bonne chance !")
    await asyncio.sleep(2.5)
    await message.delete()

    if user_id == '1245348843982426246' and number is not None:
        result = number
    else:
        result = random.randint(1, 1000)
    

    if result == 1:
        embed = discord.Embed(
            title=f"**0,1%** SummerTime - Discord Nitro 1 an",
            description=f"Bien joué, vous avez gagné : `Discord Nitro 1 an` - {ctx.author.mention}",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)
        await ctx.send("Vous pouvez faire un ticket pour réclamer cette récompense avec un screen !")
    elif result == 2:
        embed = discord.Embed(
            title=f"**0,1%** SummerTime - Discord Nitro 1 mois",
            description=f"Bien joué, vous avez gagné : `Discord Nitro 1 mois` - {ctx.author.mention}",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)
        await ctx.send("Vous pouvez faire un ticket pour réclamer cette récompense avec un screen !")
    elif result in range(3, 13):
        embed = discord.Embed(
            title=f"**1%** SummerTime - Millionaire",
            description=f"Bienvenue au club des millionnaires ! - {ctx.author.mention}",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)
        await ctx.send("Vous pouvez faire un ticket pour réclamer cette récompense avec un screen ! C'est une sécurité pour nous assurez que tu as le niveau de la banque nécessaire !")
    elif result in range(13, 23):
        user_balance_old = user_balance
        user_balance -= user_balance
        user_money["balance"] = user_balance
        save_user_money(server_id, user_id, user_money)
        embed = discord.Embed(
            title=f"**1%** SummerTime - Banqueroute instantanée !",
            description=f"Banqueroute instantanée ! Vous avez perdu : {user_balance_old} pièces... - {ctx.author.mention}",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")
    elif result in range(23, 33):
        embed = discord.Embed(
            title=f"**1%** SummerTime - Grade Première Classe",
            description=f"Première classe, mais ça ne va pas durer ! Vous l'avez uniquement durant le temps de l'évenement. - {ctx.author.mention}",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)
        await ctx.send("Vous pouvez faire un ticket pour réclamer cette récompense avec un screen !")
    elif result in range(33, 183):
        embed = discord.Embed(
            title=f"**15%** SummerTime - RIEN",
            description=f"Vous avez **RIEN** gagné, cheh. - {ctx.author.mention}",
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)
    elif result in range(183, 293):
        user_balance += 5000
        user_money["balance"] = user_balance
        save_user_money(server_id, user_id, user_money)
        embed = discord.Embed(
            title=f"**11%** SummerTime - 5000 pièces",
            description=f"5000 pièces, rien que pour toi ! - {ctx.author.mention}",
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")
    elif result in range(293, 343):
        user_balance -= 10000
        user_money["balance"] = user_balance
        save_user_money(server_id, user_id, user_money)
        embed = discord.Embed(
            title=f"**5%** SummerTime - 10000 pièces",
            description=f"Banqueroute express : -10000 pièces ! - {ctx.author.mention}",
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")
    elif result in range(343, 393):
        embed = discord.Embed(
            title=f"**5%** SummerTime - Boost gamble",
            description=f"24 heures de chance pure ! (Boost gamble) - {ctx.author.mention}",
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)
        await ctx.send("Vous pouvez faire un ticket pour réclamer cette récompense avec un screen !")
    elif result in range(393, 443):
        ticket_data['ticket_count'] += 5
        save_ticket_data(server_id, user_id, ticket_data)
        embed = discord.Embed(
            title=f"**5%** SummerTime - Relance le jeu !",
            description=f"5 jetons, comme par magie ! - {ctx.author.mention}",
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")
    elif result in range(443, 453):
        ticket_data['ticket_count'] += 10
        save_ticket_data(server_id, user_id, ticket_data)
        embed = discord.Embed(
            title=f"**1%** SummerTime - Relance le jeu !",
            description=f"10 jetons, comme par magie ! - {ctx.author.mention}",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")
    elif result in range(453, 473):
        embed = discord.Embed(
            title=f"**2%** SummerTime - Travail encore et encore...",
            description=f"Tire-au-flanc, jamais ! 25 fois au taf ! - {ctx.author.mention}",
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")
        for _ in range(25):
            server_id = ctx.guild.id
            user_id = ctx.author.id
            
            jobs = [
                {"name": "Chômeur (Aka : kaxzera)", "min_earning": 10, "max_earning": 250, "required_level": 0, "emoji": discord.PartialEmoji(name="dancingrgb", id=1112807461905240098, animated=True)},
                {"name": "Mineur", "min_earning": 50, "max_earning": 350, "required_level": 10, "emoji": discord.PartialEmoji(name="pikaMining", id=1245457541350031511, animated=True)},
                {"name": "Farmeur", "min_earning": 10, "max_earning": 450, "required_level": 20, "emoji": discord.PartialEmoji(name="minecraft", id=1112807473494114466, animated=True)},
                {"name": "Chasseur", "min_earning": 10, "max_earning": 550, "required_level": 30, "emoji": discord.PartialEmoji(name="bug_hunter_animated", id=1245458035938300039, animated=True)},
                {"name": "Alchimiste", "min_earning": 10, "max_earning": 1000, "required_level": 40, "emoji": discord.PartialEmoji(name="AlchimistePot", id=1245457073219829940, animated=True)},
                {"name": "Cadre", "min_earning": 10, "max_earning": 1250, "required_level": 50, "emoji": discord.PartialEmoji(name="clefbleu", id=1126754565342105630, animated=False)},
                {"name": "Pilote Production", "min_earning": 10, "max_earning": 2000, "required_level": 60, "emoji": discord.PartialEmoji(name="medal", id=1112807565236125746, animated=True)},
            ]

            level_data = get_user_level(server_id, user_id)
            user_level = level_data.get("level", 1)

            embed = discord.Embed(title="Sélectionnez votre métier", description=f"Votre niveau actuel est : {user_level}")
            for job in jobs:
                if user_level >= job['required_level']:
                    min_earning = job['min_earning'] + (user_level - 1) * 125
                    max_earning = job['max_earning'] + (user_level - 1) * 125
                    embed.add_field(name=f"{job['emoji']} {job['name']}", value=f"Gagnez entre {min_earning} et {max_earning} <a:money:1118983615418728508> (Niveau requis : {job['required_level']})", inline=False)
            
            message = await ctx.send(embed=embed)

            available_jobs = [job for job in jobs if user_level >= job['required_level']]
            for job in available_jobs:
                await message.add_reaction(job['emoji'])

            try:
                reaction, _ = await bot.wait_for('reaction_add', timeout=60.0, check=lambda reaction, user: user == ctx.author and any(job['emoji'] == reaction.emoji for job in available_jobs))
            except asyncio.TimeoutError:
                await ctx.send("Trop tard, après 60 secondes sans réponse de votre part. Le bot a automatiquement annulé cette commande. Le cooldown est toujours actif !")
                return

            selected_job = next((job for job in available_jobs if job['emoji'] == reaction.emoji), None)

            if selected_job:
                work_amount = random.randint(selected_job['min_earning'] + (user_level - 1) * 125, selected_job['max_earning'] + (user_level - 1) * 125)
                user_money = load_user_money(server_id, user_id)
                user_balance = user_money.get("balance", 0)
                user_balance += work_amount

                user_money["balance"] = user_balance
                save_user_money(server_id, user_id, user_money)

                embed = discord.Embed(
                    title="Travail accompli !",
                    description=f"Vous avez travaillé en tant que {selected_job['name']} et gagné {work_amount} <a:money:1118983615418728508> !",
                    color=discord.Color.green()
                )
                await message.edit(embed=embed)
            else:
                await ctx.send("Métier invalide")

            await message.clear_reactions()
    elif result in range(473, 503):
        server_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        user_data = load_user_bank(server_id, user_id)
        user_data_money = load_user_money(server_id, user_id)
        balance = user_data_money["balance"]
        level = user_data["level"]
        level += 1
        user_data_money["balance"] = balance
        user_data["level"] = level
        save_user_bank(server_id, user_id, user_data)
        save_user_money(server_id, user_id, user_data_money)
        embed = discord.Embed(
            title=f"**3%** SummerTime - Amélioration inattendue !",
            description=f"Amélioration inattendue, votre banque à été améliorée gratuitement ! - {ctx.author.mention}",
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")
    elif result in range(503, 533):
        server_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        user_data = load_user_bank(server_id, user_id)
        user_data_money = load_user_money(server_id, user_id)
        balance = user_data_money["balance"]
        level = user_data["level"]
        level += 3
        user_data_money["balance"] = balance
        user_data["level"] = level
        save_user_bank(server_id, user_id, user_data)
        save_user_money(server_id, user_id, user_data_money)
        embed = discord.Embed(
            title=f"**3%** SummerTime - Amélioration inattendue !",
            description=f"Amélioration inattendue, votre banque à été améliorée **X3 FOIS** gratuitement ! - {ctx.author.mention}",
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")
    elif result in range(533, 553):
        await add_protection(ctx, ctx.author, 1)
        embed = discord.Embed(
            title=f"**2%** SummerTime - Bouclier ?",
            description=f"Pouf ! Disparition du bouclier ! - {ctx.author.mention}",
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")
    elif result in range(553, 573):
        await add_protection(ctx, ctx.author, 7 * 24 * 3600)
        embed = discord.Embed(
            title=f"**2%** SummerTime - BOUCLIER !",
            description=f"Semaine en mode forteresse ! - {ctx.author.mention}",
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")
    elif result in range(573, 593):
        await ctx.send("Rien, même pas le message...")
    elif result in range(593, 623):
        embed = discord.Embed(
            title=f"**3%** SummerTime - Cadeauuuuu",
            description=f"Éloge spécial de l'équipe ! - {ctx.author.mention}",
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)
        await ctx.send("Vous pouvez faire un ticket pour réclamer cette récompense avec un screen !")
    elif result in range(623, 643):
        embed = discord.Embed(
            title=f"**2%** SummerTime - Face-à-face risqué !",
            description=f" Force n'importe quel joueur à faire un duel avec toi jusqu’à 10% de la fortune du joueur ciblé ! - {ctx.author.mention}",
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)
        await ctx.send("Vous pouvez faire un ticket pour réclamer cette récompense avec un screen !")
    elif result in range(643, 663):
        role_id = 1103936073043820569
        role = ctx.guild.get_role(role_id)
        if role in ctx.author.roles:
            await ctx.author.remove_roles(role)

            embed = discord.Embed(
                title=f"**2%** SummerTime - Déclassement instantané !",
                description=f"Tu es Première Classe ? Maintenant, plus. - {ctx.author.mention}",
                color=discord.Color.yellow()
            )
            await ctx.send(embed=embed)
            await ctx.send("Votre évenement à été automatiquement distribué !")
        else:
            await ctx.send("Tu n'as pas le rôle Première Classe. Pour information tu aurais perdu le rôle première classe avec cet évenement. ")
    elif result in range(663, 683):
        server_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        
        user_data = load_user_earning(server_id, user_id)
        
        # Liste des minerais
        minerals = [
            "stone", "andesite", "coal", "iron", "platinium", "gold",
            "titanium", "palladium", "ruby", "emerald", "diamond", "uranium", "radium", "pilodium"
        ]
        
        # Améliorer tous les mineurs débloqués
        for mineral in minerals:
            if user_data.get(f"{mineral}_level", 0) > 1:
                user_data[f"{mineral}_level"] += 1
        
        save_user_earning(server_id, user_id, user_data)
        embed = discord.Embed(
            title=f"**2%** SummerTime - Promotion express des mineurs !",
            description=f"Promotion express des mineurs ! - {ctx.author.mention}",
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")
    elif result in range(683, 703):
        server_id = ctx.guild.id
        user_id = ctx.author.id
        user_money = load_user_money(server_id, user_id)
        user_balance = user_money.get("balance", 0)
        win_chance = 0.50
        amount = 10000
        if random.random() < win_chance:
            win_amount = amount
            user_balance += win_amount

            embed = discord.Embed(
                title="Pari réussi",
                description=f"Vous avez gagné {win_amount} pièces ! Votre solde actuel est de {user_balance} pièces.",
                color=discord.Color.green()
            )
        else:
            user_balance -= amount

            embed = discord.Embed(
                title="Pari perdu",
                description=f"Vous avez perdu {amount} pièces. Votre solde actuel est de {user_balance} pièces.",
                color=discord.Color.red()
            )

        user_money["balance"] = user_balance
        save_user_money(server_id, user_id, user_money)

        await ctx.send(embed=embed)
        embed = discord.Embed(
            title=f"**2%** SummerTime - Pari audacieux : 10,000 pièces sur la table !",
            description=f"Pari audacieux : 10,000 pièces sur la table ! - {ctx.author.mention}",
            color=discord.Color.yellow()
        )  
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")
    elif result in range(703, 713):
        server_id = ctx.guild.id
        user_id = ctx.author.id
        user_money = load_user_money(server_id, user_id)
        user_balance = user_money.get("balance", 0)
        win_chance = 0.40
        amount = 100000
        if random.random() < win_chance:
            win_amount = amount
            user_balance += win_amount

            embed = discord.Embed(
                title="Pari réussi",
                description=f"Vous avez gagné {win_amount} pièces ! Votre solde actuel est de {user_balance} pièces.",
                color=discord.Color.green()
            )
        else:
            user_balance -= amount

            embed = discord.Embed(
                title="Pari perdu",
                description=f"Vous avez perdu {amount} pièces. Votre solde actuel est de {user_balance} pièces.",
                color=discord.Color.red()
            )

        user_money["balance"] = user_balance
        save_user_money(server_id, user_id, user_money)

        await ctx.send(embed=embed)
        embed = discord.Embed(
            title=f"**1%** SummerTime - Pari audacieux : 100,000 pièces sur la table !",
            description=f"Pari audacieux : 100,000 pièces sur la table ! - {ctx.author.mention}",
            color=discord.Color.purple()
        )  
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")
    elif result in range(713, 723):
        reason = "SummerTime : Vous avez été bannis pendant 1 heure ! (Si le temps dépasse contactez-nous !)"
        add_user_to_banlist(ctx.guild.id, 1210261910537375826, ctx.author.id, reason)
        embed = discord.Embed(
            title=f"**1%** SummerTime - Pause obligatoire !",
            description=f"Pause obligatoire : 1 heure de bannissement ! (ouvrir un ticket pour le débanissement) - {ctx.author.mention}",
            color=discord.Color.purple()
        )  
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")
    elif result in range(723, 753):
        embed = discord.Embed(
            title=f"**3%** SummerTime - Voleur expert : bouclier ? Quel bouclier ?",
            description=f"Vol n'importe qui, même avec le bouclier ! Alors tu choisis qui ? - {ctx.author.mention}",
            color=discord.Color.yellow()
        )  
        await ctx.send(embed=embed)
        await ctx.send(f"{ctx.author.mention} C'est qui ta cible ? (Attention elle peut toujours annuler le vol !)")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await bot.wait_for('message', check=check, timeout=60.0)
            if len(msg.mentions) == 1:
                target = msg.mentions[0]
                await ctx.send(f"Tu as choisi de voler {target.mention} !")
                server_id = ctx.guild.id
                user_id = ctx.author.id

                if target.id == 97285029289275392:
                    target_mention = "Utilisateur protégé contre les mentions."
                else:
                    target_mention = target.mention

                if target == ctx.author:
                    embed = discord.Embed(title="Erreur", description="Vous ne pouvez pas vous voler vous-même.", color=discord.Color.red())
                    await ctx.send(embed=embed)
                    return

                user_money = load_user_money(server_id, user_id)
                target_money = load_user_money(server_id, target.id)

                user_balance = user_money.get("balance", 0)
                target_balance = target_money.get("balance", 0)

                if ctx.guild.id == 1103936072989278279 and discord.utils.get(ctx.author.roles, id=1235641515263528992):
                    target_mention = "Cible anonyme"

                message_text = f"{target_mention}"
                embed = discord.Embed(
                    title="Vol en cours",
                    description=f"Attention {target_mention} !\nVotre compte est actuellement en train d'être volé par {ctx.author.mention} ! \nCliquez sur la réaction pour prévenir la police.",
                    color=discord.Color.orange()
                )
                message = await ctx.send(message_text, embed=embed)
                await message.add_reaction("⛔")

                try:
                    reaction, _ = await bot.wait_for(
                        "reaction_add",
                        timeout=60, 
                        check=lambda r, u: r.message.id == message.id and u.id == target.id and str(r.emoji) == "⛔"
                    )
                except asyncio.TimeoutError:
                    target_bank = load_user_bank(server_id, target.id)
                    bank_level = target_bank.get("level", 1)
                    max_steal_amount = 2000 + (bank_level * 2500)
                    stolen_amount = random.randint(100, max_steal_amount)
                    
                    if stolen_amount > target_balance:
                        stolen_amount = target_balance
                    
                    embed = discord.Embed(
                        title="Vol réussi",
                        description=f"Voleur : {ctx.author.mention}\nVous avez volé {stolen_amount} pièces sur le compte de {target_mention} !",
                        color=discord.Color.green()
                    )
                    await message.edit(embed=embed)

                    user_balance += stolen_amount
                    target_balance -= stolen_amount

                    user_money["balance"] = user_balance
                    target_money["balance"] = target_balance

                    save_user_money(server_id, user_id, user_money)
                    save_user_money(server_id, target.id, target_money)
                else:
                    fine_amount = random.randint(1000, 5000) 
                    user_balance -= fine_amount
                    target_balance += fine_amount

                    user_money["balance"] = user_balance
                    target_money["balance"] = target_balance

                    if user_balance < 0:
                        embed = discord.Embed(title="Vol annulé", description=f"Votre vol a été annulé.\nUne amende de 0 pièce a été prélevée au compte de {ctx.author.mention}", color=discord.Color.red())
                        await ctx.send(embed=embed)
                        return
                        
                    save_user_money(server_id, user_id, user_money)
                    save_user_money(server_id, target.id, target_money)

                    embed = discord.Embed(
                        title="Vol annulé",
                        description=f"Le vol a été annulé par {target_mention}.\nUne amende de {fine_amount} pièces a été prélevée au compte de {ctx.author.mention} !",
                        color=discord.Color.red()
                    )
                    await message.edit(embed=embed)

                await message.clear_reaction("⛔")
            else:
                await ctx.send(f"{ctx.author.mention}, ce n'est pas une mention valide d'utilisateur. Veuillez réessayer.")
        except asyncio.TimeoutError:
            await ctx.send(f"Désolé {ctx.author.mention}, tu as mis trop de temps à répondre !")

    elif result in range(753, 773):
        embed = discord.Embed(
            title=f"**2%** SummerTime - Cambrioleur sans pitié : vol inévitable !",
            description=f"Vol n'importe qui, même avec le bouclier, même si tu as un cooldown, même si tu as plus de 500000, et plus encore ! Alors tu choisis qui ? - {ctx.author.mention}\n PS: Il ne peux pas annulé le vol alors fait toi plaisir :)",
            color=discord.Color.yellow()
        )  
        await ctx.send(embed=embed)
        await ctx.send(f"{ctx.author.mention} C'est qui ta cible ?")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await bot.wait_for('message', check=check, timeout=60.0)
            if len(msg.mentions) == 1:
                target = msg.mentions[0]
                await ctx.send(f"Tu as choisi de voler {target.mention} !")
                server_id = ctx.guild.id
                user_id = ctx.author.id

                if target.id == 97285029289275392:
                    target_mention = "Utilisateur protégé contre les mentions."
                else:
                    target_mention = target.mention

                if target == ctx.author:
                    embed = discord.Embed(title="Erreur", description="Vous ne pouvez pas vous voler vous-même.", color=discord.Color.red())
                    await ctx.send(embed=embed)
                    return

                user_money = load_user_money(server_id, user_id)
                target_money = load_user_money(server_id, target.id)

                user_balance = user_money.get("balance", 0)
                target_balance = target_money.get("balance", 0)

                if ctx.guild.id == 1103936072989278279 and discord.utils.get(ctx.author.roles, id=1235641515263528992):
                    target_mention = "Cible anonyme"


                message_text = f"{target_mention}"
                embed = discord.Embed(
                    title="Vol en cours",
                    description=f"Attention {target_mention} !\nVotre compte est actuellement en train d'être volé par {ctx.author.mention} ! \nMalheursement, vous ne pouvez rien faire, c'est triste...",
                    color=discord.Color.orange()
                )
                message = await ctx.send(message_text, embed=embed)


                target_bank = load_user_bank(server_id, target.id)
                bank_level = target_bank.get("level", 1)
                max_steal_amount = 2000 + (bank_level * 2500)
                stolen_amount = random.randint(100, max_steal_amount)
                
                if stolen_amount > target_balance:
                    stolen_amount = target_balance
                
                embed = discord.Embed(
                    title="Vol réussi",
                    description=f"Voleur : {ctx.author.mention}\nVous avez volé {stolen_amount} pièces sur le compte de {target_mention} !",
                    color=discord.Color.green()
                )
                await message.edit(embed=embed)

                user_balance += stolen_amount
                target_balance -= stolen_amount

                user_money["balance"] = user_balance
                target_money["balance"] = target_balance

                save_user_money(server_id, user_id, user_money)
                save_user_money(server_id, target.id, target_money)
            else:
                await ctx.send(f"{ctx.author.mention}, ce n'est pas une mention valide d'utilisateur. Veuillez réessayer.")
        except asyncio.TimeoutError:
            await ctx.send(f"Désolé {ctx.author.mention}, tu as mis trop de temps à répondre !")
    elif result in range(773, 793):
        server_id = ctx.guild.id
        user_id = ctx.author.id

        
        settings_embed = await check_settings(server_id, user_id)
        if settings_embed is not None:
            await ctx.send(embed=settings_embed)
            return
        
        user_money = load_user_money(server_id, user_id)
        user_balance = user_money.get("balance", 0)

        work_amount = random.randint(100, 6999)
        user_balance += work_amount

        user_money["balance"] = user_balance

        save_user_money(server_id, user_id, user_money)

        embed = discord.Embed(
            title="Tirage !",
            description=f"Vous avez fait un tirage pour {work_amount} <a:money:1118983615418728508> !",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    elif result in range(793, 813):
        await ctx.send("Loterie d'or : mise libre ! Faire un ticket cette fonctionnalité arrive bientôt.")
    elif result in range(813, 833):
        server_id = ctx.guild.id
        user_id = ctx.author.id
        
        user_money = load_user_money(server_id, user_id)
        user_balance = user_money.get("balance", 0)
        
        reduction_amount = user_balance * 0.10
        new_balance = user_balance - reduction_amount
        
        user_money["balance"] = new_balance
        save_user_money(server_id, user_id, user_money)
        
        embed = discord.Embed(
            title=f"**2%** SummerTime - Solde réduit de 10%",
            description=f"Note salée : Votre solde a été réduit de 10% ! Nouveau solde : {new_balance:.2f} pièces. - {ctx.author.mention}",
            color=discord.Color.yellow()
        )  
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")

    elif result in range(833, 853):
        server_id = ctx.guild.id
        user_id = ctx.author.id
        
        user_money = load_user_money(server_id, user_id)
        user_balance = user_money.get("balance", 0)
        
        reduction_amount = user_balance * 1.10
        new_balance = reduction_amount
        
        user_money["balance"] = new_balance
        save_user_money(server_id, user_id, user_money)
        
        embed = discord.Embed(
            title=f"**2%** SummerTime - Solde augmenté de 10%",
            description=f"Facture surpayée : Votre solde a été augmenté de 10% ! Nouveau solde : {new_balance:.2f} pièces. - {ctx.author.mention}",
            color=discord.Color.yellow()
        )  
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")
    elif result in range(853, 873):
        embed = discord.Embed(
            title=f"**2%** SummerTime - Organisateur de drop",
            description=f"Organise ton propre drop, mais avec ton argent. - {ctx.author.mention}",
            color=discord.Color.yellow()
        )  
        await ctx.send(embed=embed)
        await ctx.send("Merci de faire un ticket, si c'est pas fait, le montant maximal (100% de votre solde) sera distribué.")
    elif result in range(873, 893):
        level_data = get_user_level(ctx.guild.id, ctx.author.id)
        level_data['level'] += 1
        save_user_level(ctx.guild.id, ctx.author.id, level_data)
        embed = discord.Embed(
            title=f"**2%** SummerTime - Ascension instantanée : niveau gratuit !",
            description=f"Ascension instantanée : niveau gratuit ! Tu as gagné 1 niveau. - {ctx.author.mention}",
            color=discord.Color.yellow()
        )  
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")
    elif result in range(893, 903):
        level_data = get_user_level(ctx.guild.id, ctx.author.id)
        level_data['level'] += 10
        save_user_level(ctx.guild.id, ctx.author.id, level_data)
        embed = discord.Embed(
            title=f"**1%** SummerTime - Montée fulgurante : 10 niveaux gratuits !",
            description=f"Montée fulgurante : 10 niveaux gratuits ! Tu as gagné 10 niveau. - {ctx.author.mention}",
            color=discord.Color.purple()
        )  
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")
    elif result in range(903, 913):
        level_data = get_user_level(ctx.guild.id, ctx.author.id)
        level_data['level'] = 1
        save_user_level(ctx.guild.id, ctx.author.id, level_data)
        embed = discord.Embed(
            title=f"**1%** SummerTime - Grand reset : tous les niveaux à zéro !",
            description=f"Grand reset : tous les niveaux à zéro ! Tu es maintenant niveau 1 niveau. - {ctx.author.mention}",
            color=discord.Color.purple()
        )  
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")
    elif result in range(913, 933):
        payout_value += 1000000
        payout_history.append((datetime.now(), payout_value))
        embed = discord.Embed(
            title=f"**1%** SummerTime - Barre de retrait rehaussée : +1 million !",
            description=f"Barre de retrait rehaussée : +1 million ! Maintenant l'argent paypal sera plus si simple, à cause de toi. - {ctx.author.mention}",
            color=discord.Color.purple()
        )  
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")
    elif result in range(933, 943):
        payout_value -= 1000000
        payout_history.append((datetime.now(), payout_value))
        embed = discord.Embed(
            title=f"**1%** SummerTime - Payout simplifié : 1 million de moins à atteindre !",
            description=f"Payout simplifié : 1 million de moins à atteindre ! Maintenant l'argent paypal est si simple, à cause de toi. - {ctx.author.mention}",
            color=discord.Color.purple()
        )  
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")
    elif result in range(943, 963):
        await ctx.send("Erreur, contactez nous pour être remboursé !")
    elif result in range(963, 973):
        server_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        
        user_data = load_user_earning(server_id, user_id)
    
        user_data["pilodium_ore"] = user_data.get("pilodium_ore", 0) + 15
        
        save_user_earning(server_id, user_id, user_data)
        embed = discord.Embed(
            title=f"**1%** SummerTime - Découverte inédite !",
            description=f"Exploration décalée : découverte de 15 pilodium ! - {ctx.author.mention}",
            color=discord.Color.purple()
        )  
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")
    elif result in range(973, 993):
        server_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        
        user_data = load_user_earning(server_id, user_id)
    
        user_data["gold_level"] = 0

        save_user_earning(server_id, user_id, user_data)
        embed = discord.Embed(
            title=f"**2%** SummerTime - Explosion fatale : adieu mineurs d'or !",
            description=f"Explosion fatale : adieu mineurs d'or ! - {ctx.author.mention}",
            color=discord.Color.yellow()
        )  
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")
    elif result in range(993, 1000):
        user_balance += 25000
        user_money["balance"] = user_balance
        save_user_money(server_id, user_id, user_money)
        embed = discord.Embed(
            title=f"**2,8%** SummerTime - 25000 pièces",
            description=f"25000 pièces, rien que pour toi ! - {ctx.author.mention}",
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)
        await ctx.send("Votre évenement à été automatiquement distribué !")



#####################################################################################################################
#                                                                                                                   #
#                                                                                                                   #
#                                                  BANQUES : V1                                                     #
#                                               PAR PILOTE PRODUCTION                                               #
#                                                                                                                   #
#####################################################################################################################
    
@bot.hybrid_group(description="Gestion de la banque avancée")
async def bank(ctx):
    if ctx.invoked_subcommand is None:
        embed = discord.Embed(
            title="Commandes de la Banque",
            description="Utilisation : `/bank view | balance | upgrade`",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

@bank.command(description="Affiche le niveau de votre banque")
async def view(ctx):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)
    user_data = load_user_bank(server_id, user_id)
    embed = discord.Embed(
        title="Niveau de la Banque",
        description=f"Votre niveau de banque : {user_data['level']}",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bank.command(description="Affiche le pourcentage de votre banque utilisé")
async def balance(ctx):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)
    user_data = load_user_bank(server_id, user_id)
    user_data_money = load_user_money(server_id, user_id)
    balance = user_data_money["balance"]
    level = user_data["level"]
    max_balance = level * 100000
    percentage_used = (balance / max_balance) * 100
    embed = discord.Embed(
        title="Balance de la banque",
        description=f"Vous avez utilisé {percentage_used:.2f}% de votre banque niveau {level}",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bank.command(description="Améliore votre banque")
async def upgrade(ctx):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)
    user_data = load_user_bank(server_id, user_id)
    user_data_money = load_user_money(server_id, user_id)
    balance = user_data_money["balance"]
    level = user_data["level"]
    
    upgrade_cost = level * 10000
    if balance < upgrade_cost:
        embed = discord.Embed(
            description=f"Vous n'avez pas assez d'argent pour améliorer votre banque au niveau {level + 1}. Coût : {upgrade_cost} <a:money:1118983615418728508>",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    balance -= upgrade_cost
    level += 1
    user_data_money["balance"] = balance
    user_data["level"] = level
    save_user_bank(server_id, user_id, user_data)
    save_user_money(server_id, user_id, user_data_money)
    
    embed = discord.Embed(
        description=f"Votre banque a été améliorée au niveau {level} pour {upgrade_cost} <a:money:1118983615418728508>",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bank.group(name="admin", invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def bank_admin(ctx):
    if ctx.invoked_subcommand is None:
        embed = discord.Embed(
            title="Commandes Admin de la Banque",
            description="Utilisation : `?bank admin setlevel`",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

@bank_admin.command(name="setlevel")
@commands.has_permissions(administrator=True)
async def set_level(ctx, user: discord.User, level: int):
    if level < 0:
        embed = discord.Embed(
            description="Le niveau ne peut pas être inférieur à 0.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    server_id = str(ctx.guild.id)
    user_id = str(user.id)
    user_data = load_user_bank(server_id, user_id)
    user_data["level"] = level
    save_user_bank(server_id, user_id, user_data)
    
    embed = discord.Embed(
        description=f"Le niveau de la banque de {user.mention} a été défini sur {level}.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)



#####################################################################################################################
#                                                                                                                   #
#                                                                                                                   #
#                                                  ÉCONOMIE : V2                                                    #
#                                               PAR PILOTE PRODUCTION                                               #
#                                                                                                                   #
#####################################################################################################################


@bot.hybrid_command(description="Donne de l'argent à toutes les personnes du serveur.")
@commands.has_permissions(administrator=True)
async def donateall(ctx, amount: int):
    if amount is None:
        embed = discord.Embed(title="Commande : Donateall", description="Donne à tous les membres du serveur le nombre spécifié.", color=discord.Color.blue())
        embed.add_field(name="Utilisation", value="?donateall [amount]")
        embed.add_field(name="Description", value="Donne à tous les membres du serveur la somme spécifiée. Vous devez spécifier le montant.")
        await ctx.send(embed=embed)
        return
    server_id = str(ctx.guild.id)
    member_count = len(ctx.guild.members)
    count = 0
    
    message = await ctx.send(f"Donation en cours à tous les membres <a:parrot_dance:1065603664087093279> ({amount}/{member_count} membres du serveur)")
    
    for member in ctx.guild.members:
        user_id = str(member.id)
        user_data = load_user_money(server_id, user_id)
        user_data["balance"] += amount
        save_user_money(server_id, user_id, user_data)
        count += 1
        
        if count % 10 == 0:
            await message.edit(content=f"<a:loading:1112807489042399333> {count}/{member_count} membres ont reçu {amount} comme demandé.<a:parrot_dance:1065603664087093279>")
    
    await message.edit(content=f"Tous les membres ont reçu {amount} comme demandé.")

@bot.hybrid_command(aliases=["bal"], description="Affiche ton solde actuel")
async def balance(ctx, user: discord.User = None):
    if user is None:
        user = ctx.author
    user_id = ctx.author.id
    server_id = str(ctx.guild.id)
    
    settings_embed = await check_settings(server_id, user_id)
    if settings_embed is not None:
        await ctx.send(embed=settings_embed)
        return
    
    user_data = load_user_money(str(ctx.guild.id), str(user.id))
    user_data_red = load_user_earning_money(str(ctx.guild.id), str(user.id))
    balance = user_data["balance"]
    balance_red = user_data_red["balance"]
    
    embed = discord.Embed(
        title=f"Balance de {user.display_name}",
        description=f"{user.mention} possède :",
        color=discord.Color(0x2ECC71)
    )

    embed.add_field(name="• Pièces :", value=f"{balance} <a:money:1118983615418728508>", inline=True)
    embed.add_field(name="• Pièces rouges :", value=f"{balance_red} <a:redmoney:1253303769698140272>", inline=True)
    embed.set_footer(text=f"{ctx.guild.name} • Aujourd'hui à {ctx.message.created_at.strftime('%H:%M')}")
    
    await ctx.send(embed=embed)


@bot.hybrid_command(description="Paye tes amis en pièce avec cette commande")
async def pay(ctx, user: discord.User = None, amount: int = None):

    user_id = ctx.author.id
    server_id = str(ctx.guild.id)
    settings_embed = await check_settings(server_id, user_id)
    if settings_embed is not None:
        await ctx.send(embed=settings_embed)
        return
    
    loans = load_user_loans(server_id, user_id)
    
    if loans:
        await ctx.send("Vous avez un prêt en cours. Vous ne pouvez pas effectuer cette commande.")
        return
    
    if user is None or amount is None:
        embed = discord.Embed(title="Commande : Pay", description="Paye un utilisateur avec la somme spécifiée.", color=discord.Color.blue())
        embed.add_field(name="Utilisation", value="?pay [user] [amount]")
        embed.add_field(name="Description", value="Paye un utilisateur avec la somme spécifiée. Vous devez spécifier l'utilisateur et le montant.")
        await ctx.send(embed=embed)
        return
    
    if amount <= 0:
        await ctx.send("Le montant doit être supérieur à zéro.")
        return
    
    sender_data = load_user_money(str(ctx.guild.id), str(ctx.author.id))
    receiver_data = load_user_money(str(ctx.guild.id), str(user.id))
    
    
    if sender_data["balance"] < amount:
        await ctx.send("Vous n'avez pas assez d'argent pour effectuer cette transaction.")
        return
    
    if ctx.author.id == user.id:
        await ctx.send("Vous ne pouvez pas vous donner de l'argent à vous-même !")
        return
    else:
        sender_data["balance"] -= amount
    
    save_user_money(str(ctx.guild.id), str(ctx.author.id), sender_data)
    receiver_data["balance"] += amount
    save_user_money(str(ctx.guild.id), str(user.id), receiver_data)
    
    embed = discord.Embed(title="Transaction", description=f"Vous avez payé {amount} <a:money:1118983615418728508> à {user.name}")
    await ctx.send(embed=embed)


@bot.hybrid_group()
@commands.has_permissions(administrator=True)
async def eco(ctx):
    if ctx.invoked_subcommand is None:
        embed = discord.Embed(title="Commande : Eco", description="Commandes pour gérer l'économie du serveur.", color=discord.Color.blue())
        embed.add_field(name="Sous-commandes", value="?eco give [user_id] [amount] - Donne de l'argent à un utilisateur\n?eco reset [user_id] - Réinitialise la balance d'un utilisateur\n?eco remove [user_id] [amount] - Retire de l'argent à un utilisateur\n?eco set [user_id] [amount] - Remplace la balance d'un utilisateur")
        await ctx.send(embed=embed)


@eco.command(description="Donne l'argent pour les boosters de serveur")
@commands.has_permissions(administrator=True)
async def boost(ctx):
    server_id = str(ctx.guild.id)
    boost_role_id = 1112803317630902273

    if ctx.guild.id != 1103936072989278279:
        await ctx.send("Commande indisponible sur ce serveur")
        return

    if boost_role_id not in [role.id for role in ctx.author.roles]:
        await ctx.send("Vous n'avez pas l'autorisation d'utiliser cette commande.")
        return

    boosters = [member for member in ctx.guild.members if boost_role_id in [role.id for role in member.roles]]

    boost_counts = {}

    for booster in boosters:
        boost_counts[booster.name] = boost_counts.get(booster.name, 0) + 1
        user_money = load_user_money(server_id, str(booster.id))
        user_money["balance"] += 10000
        save_user_money(server_id, str(booster.id), user_money)

    embed = discord.Embed(title="Boosteurs récompensés", color=0x8A2BE2)
    embed.set_thumbnail(url="https://media.tenor.com/IxPGomrRTzYAAAAi/booster.gif")

    if boost_counts:
        output = "Liste des boosteurs qui ont reçu 10000 pièces :\n"
        for booster, count in boost_counts.items():
            embed.add_field(name=f"{booster} a reçu {count} récompense(s) :", value="10000 pièces ! Merci pour le boost !", inline=False)
    else:
        output = "Aucun boosteur trouvé."

    await ctx.send(embed=embed)

@eco.command(description="Donne l'argent pour la personne séléctionnée")
@commands.has_permissions(administrator=True)
async def give(ctx, member: discord.Member=None, amount: int = None):
    user_id = member.id
    if user_id is None or amount is None:
        embed = discord.Embed(title="Sous-commande : Eco Give", description="Donne de l'argent à un utilisateur.", color=discord.Color.blue())
        embed.add_field(name="Utilisation", value="?eco give [user_id] [amount]")
        embed.add_field(name="Description", value="Donne la somme spécifiée à l'utilisateur avec l'ID spécifié.")
        await ctx.send(embed=embed)
        return
    if amount <= 0:
        await ctx.send("Le montant doit être supérieur à zéro.")
        return
    
    user_data = load_user_money(str(ctx.guild.id), str(user_id))
    user_data["balance"] += amount
    save_user_money(str(ctx.guild.id), str(user_id), user_data)
    
    embed = discord.Embed(title="Don d'argent", description=f"Vous avez donné {amount} <a:money:1118983615418728508> à l'utilisateur avec l'ID {user_id}")
    await ctx.send(embed=embed)


@eco.command(description="Reset l'argent de la personne seléctionnée")
@commands.has_permissions(administrator=True)
async def reset(ctx, member: discord.Member=None):
    user_id = member.id
    if user_id is None:
        embed = discord.Embed(title="Sous-commande : Eco Reset", description="Réinitialise la balance d'un utilisateur.", color=discord.Color.blue())
        embed.add_field(name="Utilisation", value="?eco reset [user_id]")
        embed.add_field(name="Description", value="Réinitialise la balance de l'utilisateur avec l'ID spécifié.")
        await ctx.send(embed=embed)
        return
    user_data = {"balance": 0}
    save_user_money(str(ctx.guild.id), str(user_id), user_data)
    
    embed = discord.Embed(title="Réinitialisation de la balance", description=f"La balance de l'utilisateur avec l'ID {user_id} a été remise à zéro.")
    await ctx.send(embed=embed)


@eco.command(description="Retire l'argent de la personne séléctionnée")
@commands.has_permissions(administrator=True)
async def remove(ctx, member: discord.Member=None, amount: int = None):
    user_id = member.id
    if user_id is None or amount is None:
        embed = discord.Embed(title="Sous-commande : Eco Remove", description="Retire de l'argent à un utilisateur.", color=discord.Color.blue())
        embed.add_field(name="Utilisation", value="?eco remove [user_id] [amount]")
        embed.add_field(name="Description", value="Retire la somme spécifiée de la balance de l'utilisateur avec l'ID spécifié.")
        await ctx.send(embed=embed)
        return
    if amount <= 0:
        await ctx.send("Le montant doit être supérieur à zéro.")
        return
    
    user_data = load_user_money(str(ctx.guild.id), str(user_id))
    if user_data["balance"] < amount:
        await ctx.send("L'utilisateur n'a pas suffisamment d'argent.")
        return
    
    user_data["balance"] -= amount
    save_user_money(str(ctx.guild.id), str(user_id), user_data)
    
    embed = discord.Embed(title="Retrait d'argent", description=f"Vous avez retiré {amount} <a:money:1118983615418728508> de la balance de l'utilisateur avec l'ID {user_id}")
    await ctx.send(embed=embed)


@eco.command(name ="set", description="Remplace le solde actuel par amount !")
@commands.has_permissions(administrator=True)
async def eco_set(ctx, member: discord.Member=None, amount: int = None):
    user_id = member.id
    if user_id is None or amount is None:
        embed = discord.Embed(title="Sous-commande : Eco Set", description="Remplace la balance d'un utilisateur.", color=discord.Color.blue())
        embed.add_field(name="Utilisation", value="?eco set [user_id] [amount]")
        embed.add_field(name="Description", value="Remplace la balance de l'utilisateur avec l'ID spécifié par la somme spécifiée.")
        await ctx.send(embed=embed)
        return
    if amount < 0:
        await ctx.send("Le montant ne peut pas être négatif.")
        return
    
    user_data = {"balance": amount}
    save_user_money(str(ctx.guild.id), str(member), user_data)
    
    embed = discord.Embed(title="Remplacement de la balance", description=f"La balance de l'utilisateur avec l'ID {user_id} a été remplacée par {amount} <:money:1118983615418728508>")
    await ctx.send(embed=embed)

@bot.group()
@commands.has_permissions(administrator=True)
async def banlist(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Veuillez spécifier une sous-commande valide : add, auto, remove")

@banlist.command(name="add")
async def banlist_add(ctx, user: discord.Member, *, reason: str):
    if add_user_to_banlist(ctx.guild.id, ctx.author.id, user.id, reason):
        embed = Embed(title="Utilisateur ajouté à la liste des bannis", description=f"L'utilisateur {user.mention} a été ajouté à la liste des utilisateurs bannis.\nRaison : {reason}")
        await ctx.send(embed=embed)
    else:
        embed = Embed(title="Erreur", description=f"L'utilisateur {user.mention} est déjà présent dans la liste des utilisateurs bannis.")
        await ctx.send(embed=embed)

@banlist.command(name="auto")
async def banlist_auto(ctx, user: discord.Member, *, reason: str):
    admin_mention = f"<@1210261910537375826>"
    if add_user_to_banlist(ctx.guild.id, 1210261910537375826, user.id, reason):
        embed = Embed(title="Utilisateur ajouté à la liste des bannis", description=f"L'utilisateur {user.mention} a été ajouté à la liste des utilisateurs bannis.\nRaison : {reason}\nLa personne qui a banni est {admin_mention}")
        await ctx.send(embed=embed)
    else:
        embed = Embed(title="Erreur", description=f"L'utilisateur {user.mention} est déjà présent dans la liste des utilisateurs bannis.")
        await ctx.send(embed=embed)

@banlist.command(name="remove")
async def banlist_remove(ctx, user: discord.Member):
    if remove_user_from_banlist(ctx.guild.id, user.id):
        embed = Embed(title="Utilisateur supprimé de la liste des bannis", description=f"L'utilisateur {user.mention} a été supprimé de la liste des utilisateurs bannis.")
        await ctx.send(embed=embed)
    else:
        embed = Embed(title="Erreur", description=f"L'utilisateur {user.mention} n'est pas présent dans la liste des utilisateurs bannis.")
        await ctx.send(embed=embed)

@bot.hybrid_command(description="Travail pour des pièces")
@commands.cooldown(1, 60*60, commands.BucketType.user)
async def work(ctx):
    server_id = ctx.guild.id
    user_id = ctx.author.id

    settings_embed = await check_settings(server_id, user_id)
    if settings_embed is not None:
        await ctx.send(embed=settings_embed)
        return
    
    jobs = [
        {"name": "Chômeur", "min_earning": 10, "max_earning": 250, "required_level": 0, "emoji": discord.PartialEmoji(name="dancingrgb", id=1112807461905240098, animated=True)},
        {"name": "Mineur", "min_earning": 50, "max_earning": 350, "required_level": 5, "emoji": discord.PartialEmoji(name="pikaMining", id=1245457541350031511, animated=True)},
        {"name": "Farmeur", "min_earning": 10, "max_earning": 450, "required_level": 10, "emoji": discord.PartialEmoji(name="minecraft", id=1112807473494114466, animated=True)},
        {"name": "Chasseur", "min_earning": 10, "max_earning": 550, "required_level": 20, "emoji": discord.PartialEmoji(name="bug_hunter_animated", id=1245458035938300039, animated=True)},
        {"name": "Alchimiste", "min_earning": 10, "max_earning": 1000, "required_level": 30, "emoji": discord.PartialEmoji(name="AlchimistePot", id=1245457073219829940, animated=True)},
        {"name": "Cadre", "min_earning": 10, "max_earning": 1250, "required_level": 40, "emoji": discord.PartialEmoji(name="clefbleu", id=1126754565342105630, animated=False)},
        {"name": "Pilote Production", "min_earning": 10, "max_earning": 2000, "required_level": 50, "emoji": discord.PartialEmoji(name="medal", id=1112807565236125746, animated=True)},
    ]

    level_data = get_user_level(server_id, user_id)
    user_level = level_data.get("level", 1)

    embed = discord.Embed(title="Sélectionnez votre métier", description=f"Votre niveau actuel est : {user_level}")
    for job in jobs:
        if user_level >= job['required_level']:
            min_earning = job['min_earning'] + (user_level - 1) * 125
            max_earning = job['max_earning'] + (user_level - 1) * 125
            embed.add_field(name=f"{job['emoji']} {job['name']}", value=f"Gagnez entre {min_earning} et {max_earning} pièces (Niveau requis : {job['required_level']})", inline=False)
    
    message = await ctx.send(embed=embed)

    available_jobs = [job for job in jobs if user_level >= job['required_level']]
    for job in available_jobs:
        await message.add_reaction(job['emoji'])

    try:
        reaction, _ = await bot.wait_for('reaction_add', timeout=60.0, check=lambda reaction, user: user == ctx.author and any(job['emoji'] == reaction.emoji for job in available_jobs))
    except asyncio.TimeoutError:
        await ctx.send("Trop tard, après 60 secondes sans réponse de votre part. Le bot a automatiquement annulé cette commande. Le cooldown est toujours actif !")
        return

    selected_job = next((job for job in available_jobs if job['emoji'] == reaction.emoji), None)

    if selected_job:
        work_amount = random.randint(selected_job['min_earning'] + (user_level - 1) * 125, selected_job['max_earning'] + (user_level - 1) * 125)
        user_money = load_user_money(server_id, user_id)
        user_balance = user_money.get("balance", 0)
        user_balance += work_amount

        user_money["balance"] = user_balance
        save_user_money(server_id, user_id, user_money)

        embed = discord.Embed(
            title="Travail accompli !",
            description=f"Vous avez travaillé en tant que {selected_job['name']} et gagné {work_amount} pièces !",
            color=discord.Color.green()
        )
        await message.edit(embed=embed)
    else:
        await ctx.send("Métier invalide")

    await message.clear_reactions()



@bot.hybrid_command(description="Fonction premium, Tirage d'argent pour les premieres classe")
@commands.cooldown(1, 3*60*60, commands.BucketType.user)
async def tirage(ctx):
    server_id = ctx.guild.id
    user_id = ctx.author.id

    
    settings_embed = await check_settings(server_id, user_id)
    if settings_embed is not None:
        await ctx.send(embed=settings_embed)
        return
    
    user_money = load_user_money(server_id, user_id)
    user_balance = user_money.get("balance", 0)


    if ctx.guild.id != 1103936072989278279:
        ctx.send("Commande indisponible dans votre serveur.")
    else:
        if any(role.id == 1103936073043820569 for role in ctx.author.roles):
            work_amount = random.randint(150, 7000)
        else:
            await ctx.send("Vous n'êtes pas un utilisateur Premium")
            return
    
    user_balance += work_amount

    user_money["balance"] = user_balance

    save_user_money(server_id, user_id, user_money)

    embed = discord.Embed(
        title="Tirage !",
        description=f"Vous avez fait un tirage pour {work_amount} <a:money:1118983615418728508> !",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.hybrid_command()
async def cooldowns(ctx):
    user_id = ctx.author.id
    embed = discord.Embed(title="Liste des temps de recharges", color=discord.Color.gold())

    if user_id in cooldowns_user:
        cooldown_time = cooldowns_user[user_id]
        time_remaining = cooldown_time - datetime.now()
        if time_remaining.total_seconds() > 0:
            embed.add_field(name=f"Commande /steal", value=f"Temps restant : {time_remaining} <a:error:1112807444633092218>", inline=False)
        else:
            embed.add_field(name=f"Commande /steal", value="Pas de cooldown en cours ! <a:Blackandyellowverifed:1112807458507858061> ", inline=False)
    else:
        embed.add_field(name=f"Commande /steal", value="Pas de cooldown en cours ! <a:Blackandyellowverifed:1112807458507858061> ", inline=False)

    if user_id in cooldowns:
        cooldown_time = cooldowns[user_id]
        time_remaining = cooldown_time - datetime.now()
        if time_remaining.total_seconds() > 0:
            embed.add_field(name=f"Protection de la commande /steal", value=f"Temps restant : {time_remaining} ! <a:Blackandyellowverifed:1112807458507858061>", inline=False)
        else:
            embed.add_field(name=f"Protection de la commande /steal", value="Vous n'avez pas de protection ! <a:error:1112807444633092218>", inline=False)
    else:
        embed.add_field(name=f"Protection de la commande /steal", value="Vous n'avez pas de protection ! <a:error:1112807444633092218>", inline=False)

    for command in bot.walk_commands():
        if command.cooldown is not None:
            retry_after = command.get_cooldown_retry_after(ctx)
            if retry_after:
                embed.add_field(name=f"Commande /{command.name}", value=f"Temps restant : {retry_after:.2f} secondes ! <a:error:1112807444633092218>", inline=False)
            else:
                embed.add_field(name=f"Commande /{command.name}", value="Pas de cooldown en cours ! <a:Blackandyellowverifed:1112807458507858061> ", inline=False)

    await ctx.send(embed=embed)

cooldowns = {}
cooldowns_user = {}

LOANS_FOLDER = "data/loans/"
def check_loans_folder(server_id):
    folder_path = f"{LOANS_FOLDER}{server_id}"
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
        except OSError:
            print(f"Erreur lors de la création du dossier des prêts pour l'identifiant du serveur : {server_id}")

def load_user_loans(server_id, user_id):
    file_path = f"{LOANS_FOLDER}{server_id}/{user_id}.json"
    try:
        with open(file_path, "r") as file:
            loans = json.load(file)
    except FileNotFoundError:
        loans = {}
    return loans

def save_user_loans(server_id, user_id, loans):
    loans["date"] = datetime.now().strftime("%d/%m/%Y %H:%M")
    file_path = f"{LOANS_FOLDER}{server_id}/{user_id}.json"
    with open(file_path, "w") as file:
        json.dump(loans, file)


@bot.hybrid_group(name="loan", invoke_without_command=True)
async def loan(ctx):
    embed = discord.Embed(title="Commande ?loan", description="Veuillez spécifier une sous-commande : pay, loan, info")
    await ctx.send(embed=embed)


@loan.command(name="info", description="Affiche vos prêts actifs")
async def info_loan(ctx):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)
    check_loans_folder(server_id)
    loans = load_user_loans(server_id, user_id)

    if not loans:
        embed = discord.Embed(title="Prêt", description="Vous n'avez pas de prêt en cours.")
    else:
        amount = loans.get("amount", 0)
        embed = discord.Embed(title="Prêt", description=f"Montant du prêt : {amount} <a:money:1118983615418728508>.")

    await ctx.send(embed=embed)


def calculate_days_elapsed(loan_date):
    current_date = datetime.now()
    days_elapsed = (current_date - loan_date).days
    return days_elapsed

@loan.command(name="list", description="Liste les prêts actuels sur le serveur")
@commands.has_permissions(administrator=True)
async def list_loan(ctx):
    server_id = str(ctx.guild.id)
    loans_folder = f"{LOANS_FOLDER}{server_id}"
    loan_files = os.listdir(loans_folder)

    if not loan_files:
        embed = discord.Embed(title="Prêt", description="Aucun prêt enregistré.")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Liste des prêts", description="Voici la liste de tous les prêts enregistrés :")

        for loan_file in loan_files:
            user_id = loan_file.split(".")[0]
            user = ctx.guild.get_member(int(user_id))
            if user:
                loan_data = load_user_loans(server_id, user_id)
                loan_date = datetime.strptime(loan_data.get("date"), "%d/%m/%Y %H:%M")
                days_elapsed = calculate_days_elapsed(loan_date)
                if days_elapsed > 6:
                    status = "En retard"
                else:
                    status = "À temps"
                embed.add_field(name="Utilisateur", value=f"**Pseudo :** {user.display_name}\n**ID :** {user.id}\n**Mention :** {user.mention}", inline=False)
                embed.add_field(name="Prêt", value=f"**Date du prêt :** {loan_data['date']}\n**Statut :** {status}\n **Montant :** {loan_data['amount']}", inline=False)

        await ctx.send(embed=embed)

@loan.command(name="pay", description="Paye un prêt avec la valeur amount sélectionné")
async def pay(ctx, amount: int):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)
    check_loans_folder(server_id)
    user_money = load_user_money(server_id, user_id)
    user_balance = user_money.get("balance", 0)
    loans = load_user_loans(server_id, user_id)

    if user_balance < loans.get("amount", 0):
        await ctx.send("Vous n'avez pas assez d'argent pour payer autant !")
        return

    if not loans:
        embed = discord.Embed(title="Prêt", description="Vous n'avez pas de prêt en cours.")
        await ctx.send(embed=embed)
    elif amount >= loans.get("amount", 0):
        user_balance -= amount
        user_money["balance"] = user_balance
        save_user_money(server_id, user_id, user_money)
        os.remove(f"{LOANS_FOLDER}{server_id}/{user_id}.json")
        embed = discord.Embed(title="Prêt", description="Prêt entièrement remboursé.")
        await ctx.send(embed=embed)
    else:
        loans["amount"] -= amount
        user_balance -= amount
        user_money["balance"] = user_balance
        save_user_money(server_id, user_id, user_money)
        save_user_loans(server_id, user_id, loans)
        embed = discord.Embed(title="Prêt", description=f"Vous avez remboursé {amount} <a:money:1118983615418728508> de votre prêt.")
        await ctx.send(embed=embed)


@loan.command(name="loan", description="Faire un prêt d'argent sur le serveur")
async def loan(ctx, amount: int):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)
    check_loans_folder(server_id)
    loans = load_user_loans(server_id, user_id)
    user_money = load_user_money(server_id, user_id)
    user_balance = user_money.get("balance", 0)
        
    if amount <= 10:
        await ctx.send("Vous devez faire un prêt de 10 minimum")
        return
    
    if loans:
        embed = discord.Embed(title="Prêt", description="Vous avez déjà un prêt en cours.")
        await ctx.send(embed=embed)
    elif amount > user_balance * 1.5:
        embed = discord.Embed(title="Prêt", description="Le montant du prêt ne peut pas dépasser x1.5 de votre solde.")
        await ctx.send(embed=embed)
    else:
        loans["amount"] = amount * 11 // 10
        frais = amount // 10
        user_balance += amount
        user_money["balance"] = user_balance
        save_user_money(server_id, user_id, user_money)
        save_user_loans(server_id, user_id, loans)
        embed = discord.Embed(title="Prêt", description=f"Vous avez emprunté {amount} <a:money:1118983615418728508>.\n Les frais sont de 10% soit {frais} !\n Information : Vous avez 6 jours pour rembourser le prêt ou votre compte monétaire sera désactivé.")
        await ctx.send(embed=embed)

@bot.hybrid_command(description="Vole l'argent d'un utilisateur")
async def steal(ctx, target: discord.Member):
    server_id = ctx.guild.id
    user_id = ctx.author.id

    settings_embed = await check_settings(server_id, user_id)
    if settings_embed is not None:
        await ctx.send(embed=settings_embed)
        return
    
    if target.id == 97285029289275392:
        await ctx.send("Utilisateur inéligible.")
        return
    else:
        target_mention = target.mention

    if target == ctx.author:
        embed = discord.Embed(title="Erreur", description="Vous ne pouvez pas vous voler vous-même.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    user_money = load_user_money(server_id, user_id)
    target_money = load_user_money(server_id, target.id)

    user_balance = user_money.get("balance", 0)
    target_balance = target_money.get("balance", 0)

    if user_balance > 500000:
        embed = discord.Embed(title="Erreur", description="Désolé, Vous êtes trop riche pour devenir un voleur ! (Maximum : 500 000 <a:money:1118983615418728508>)", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    if target_balance < 10000:
        embed = discord.Embed(title="Erreur", description="La cible doit avoir un solde d'au moins 10 000 <a:money:1118983615418728508> pour être volée.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    if ctx.guild.id == 1103936072989278279 and discord.utils.get(ctx.author.roles, id=1235641515263528992):
        target_mention = "Cible anonyme"

    if user_id in cooldowns_user:
        cooldown_time = cooldowns_user[user_id]
        time_remaining = cooldown_time - datetime.now()

        if time_remaining.total_seconds() > 0:
            embed = discord.Embed(
                title="Erreur",
                description=f"Vous êtes en cooldown. Veuillez réessayer dans {time_remaining}.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
    
    if target.id in cooldowns:
        cooldown_time = cooldowns[target.id]
        time_remaining = cooldown_time - datetime.now()

        if time_remaining.total_seconds() > 0:
            embed = discord.Embed(
                title="Erreur",
                description=f"La personne cible est en période de protection. Veuillez réessayer dans {time_remaining}.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
    cooldowns[target.id] = datetime.now() + timedelta(seconds=70)
    cooldowns_user[user_id] = datetime.now() + timedelta(seconds=70)

    message_text = f"{target_mention}"
    embed = discord.Embed(
        title="Vol en cours",
        description=f"Attention {target_mention} !\nVotre compte est actuellement en train d'être volé par {ctx.author.mention} ! \nCliquez sur la réaction pour prévenir la police.",
        color=discord.Color.orange()
    )
    message = await ctx.send(message_text, embed=embed)
    await message.add_reaction("⛔")

    try:
        reaction, _ = await ctx.bot.wait_for(
            "reaction_add",
            timeout=60, 
            check=lambda r, u: r.message.id == message.id and u.id == target.id and str(r.emoji) == "⛔"
        )
    except asyncio.TimeoutError:
        user_money = load_user_money(server_id, user_id)
        target_money = load_user_money(server_id, target.id)

        user_balance = user_money.get("balance", 0)
        target_balance = target_money.get("balance", 0)
        target_bank = load_user_bank(server_id, target.id)
        bank_level = target_bank.get("level", 1)
        max_steal_amount = 2000 + (bank_level * 1500)
        stolen_amount = random.randint(100, max_steal_amount)
        
        if stolen_amount > target_balance:
            stolen_amount = target_balance
        
        embed = discord.Embed(
            title="Vol réussi",
            description=f"Voleur : {ctx.author.mention}\nVous avez volé {stolen_amount} pièces sur le compte de {target_mention} !",
            color=discord.Color.green()
        )
        await message.edit(embed=embed)

        user_balance += stolen_amount
        target_balance -= stolen_amount

        user_money["balance"] = user_balance
        target_money["balance"] = target_balance

        save_user_money(server_id, user_id, user_money)
        save_user_money(server_id, target.id, target_money)

        cooldowns[target.id] = datetime.now() + timedelta(hours=3)
        cooldowns_user[user_id] = datetime.now() + timedelta(hours=3)
    else:
        user_money = load_user_money(server_id, user_id)
        target_money = load_user_money(server_id, target.id)

        user_balance = user_money.get("balance", 0)
        target_balance = target_money.get("balance", 0)
        fine_amount = random.randint(1000, 5000) 
        user_balance -= fine_amount
        target_balance += fine_amount

        user_money["balance"] = user_balance
        target_money["balance"] = target_balance

        if user_balance < 0:
            embed = discord.Embed(title="Vol annulé", description=f"Votre vol a été annulé.\nUne amende de 0 pièce a été prélevée au compte de {ctx.author.mention}", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
            
        save_user_money(server_id, user_id, user_money)
        save_user_money(server_id, target.id, target_money)

        embed = discord.Embed(
            title="Vol annulé",
            description=f"Le vol a été annulé par {target_mention}.\nUne amende de {fine_amount} pièces a été prélevée au compte de {ctx.author.mention} !",
            color=discord.Color.red()
        )
        await message.edit(embed=embed)

    await message.clear_reaction("⛔")

@bot.hybrid_command(description="Vole l'argent d'un utilisateur aléatoire éligible")
async def randomsteal(ctx):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    members = [member for member in ctx.guild.members if not member.bot and member != ctx.author]
    eligible_members = []

    for member in members:
        target_money = load_user_money(server_id, member.id)
        target_balance = target_money.get("balance", 0)
        if 10000 <= target_balance and member.id not in cooldowns:
            eligible_members.append(member)
    
    if not eligible_members:
        embed = discord.Embed(title="Erreur", description="Aucun utilisateur éligible à voler.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    target = random.choice(eligible_members)
    await ctx.invoke(bot.get_command("steal"), target=target)



@bot.hybrid_group()
async def daily(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Sous-commande invalide. Utilisez `?daily claim` pour récupérer votre récompense quotidienne. (?daily top pour voir le TOP des daily sur le serveur)")


@daily.command(name='set', description="Réglez le nombre de jours du streak quotidien d'un utilisateur.")
@commands.has_permissions(administrator=True)
async def daily_set(ctx, user: discord.User, days: int):
    user_id = str(user.id)
    server_id = str(ctx.guild.id)

    user_data = load_user_data_daily(user_id)

    settings_embed = await check_settings(server_id, user_id)
    if settings_embed is not None:
        await ctx.send(embed=settings_embed)
        return

    user_data["daily_streak"] = days
    user_data["last_daily"] = datetime.now().date() - timedelta(days=1)

    save_user_data_daily(user_id, user_data)

    embed = discord.Embed(
        title="Streak quotidien mis à jour",
        description=f"Le streak quotidien de {user.mention} a été réglé à {days} jours et la date du dernier daily a été mise à jour.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@daily.command(name='claim', description="Réclamez votre récompense quotidienne tous les jours pour obtenir plus de récompenses")
async def daily_claim(ctx):
    user_id = str(ctx.author.id)
    server_id = str(ctx.guild.id)
    user_data = load_user_data_daily(user_id)
    user_data_balance = load_user_money(server_id, user_id)

    settings_embed = await check_settings(server_id, user_id)
    if settings_embed is not None:
        await ctx.send(embed=settings_embed)
        return
    
    current_date = datetime.now().date()

    if ctx.guild.id != 1103936072989278279:
        await ctx.send("Cette commande n'est pas disponible sur d'autres serveurs")
        return
      
    last_daily = user_data.get("last_daily")
    if last_daily and last_daily.date() == current_date:
        await ctx.send("Vous avez déjà récupéré votre récompense quotidienne aujourd'hui.")
        return
    
    daily_streak = user_data.get("daily_streak", 0)

    if last_daily and (last_daily.date() < current_date - timedelta(days=1) or last_daily.date() != current_date - timedelta(days=1)):
        embed = discord.Embed(
            title="Réinitialisation de la série",
            description="Vous avez manqué un jour de votre série quotidienne, votre série a été réinitialisée.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        user_data["last_daily"] = current_date
        user_data["daily_streak"] = 0
        save_user_data_daily(user_id, user_data)
        return

    user_data = load_user_data_daily(user_id)

    reward_amount = 100 + user_data["daily_streak"] * 50

    user_data_balance = load_user_money(server_id, user_id)
    user_data_balance["balance"] += reward_amount

    save_user_money(server_id, user_id, user_data_balance)
    user_data["last_daily"] = current_date
    user_data["daily_streak"] = daily_streak + 1
    save_user_data_daily(user_id, user_data)
    
    embed = discord.Embed(
        title="Récompense quotidienne récupérée !",
        description=f"Vous avez gagné {reward_amount} <a:money:1118983615418728508>. Cela fait {daily_streak} jours !",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)
"""
@daily.command(name='claim', description="Réclamez votre récompense quotidienne tous les jours pour obtenir plus de récompenses")
async def daily_claim(ctx):
    user_id = str(ctx.author.id)
    server_id = str(ctx.guild.id)
    user_data = load_user_data_daily(user_id)
    user_data_balance = load_user_money(server_id, user_id)
    ticket_data = load_ticket_data(server_id, user_id)

    settings_embed = await check_settings(server_id, user_id)
    if settings_embed is not None:
        await ctx.send(embed=settings_embed)
        return

    current_date = datetime.now().date()

    if ctx.guild.id != 1103936072989278279:
        await ctx.send("Cette commande n'est pas disponible sur d'autres serveurs")
        return

    last_daily = user_data.get("last_daily")
    if last_daily and last_daily.date() == current_date:
        await ctx.send("Vous avez déjà récupéré votre récompense quotidienne aujourd'hui.")
        return

    daily_streak = user_data.get("daily_streak", 0)

    if last_daily and (last_daily.date() < current_date - timedelta(days=1) or last_daily.date() != current_date - timedelta(days=1)):
        embed = discord.Embed(
            title="Réinitialisation de la série",
            description="Vous avez manqué un jour de votre série quotidienne, votre série a été réinitialisée.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        user_data["last_daily"] = current_date
        user_data["daily_streak"] = 0
        save_user_data_daily(user_id, user_data)
        return

    reward_amount = 100 + user_data.get("daily_streak", 0) * 50

    user_data_balance["balance"] += reward_amount

    if 'ticket_count' not in ticket_data:
        ticket_data['ticket_count'] = 0
    ticket_data['ticket_count'] += 1

    save_user_money(server_id, user_id, user_data_balance)
    user_data["last_daily"] = current_date
    user_data["daily_streak"] = daily_streak + 1
    save_user_data_daily(user_id, user_data)
    save_ticket_data(server_id, user_id, ticket_data)

    embed = discord.Embed(
        title="Récompense quotidienne récupérée !",
        description=f"Vous avez gagné {reward_amount} <a:money:1118983615418728508> et 1 jeton d'évenement.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)
"""

@daily.command(name='fix', description="Commande de récupération de la série quotidienne")
async def daily_fix(ctx):
    user_id = str(ctx.author.id)
    server_id = str(ctx.guild.id)
    user_data = load_user_data_daily(user_id)
    user_data_balance = load_user_money(server_id, user_id)
    
    role_id = 1177357509997121576
    user_has_role = any(role.id == role_id for role in ctx.author.roles)

    settings_embed = await check_settings(server_id, user_id)
    if settings_embed is not None:
        await ctx.send(embed=settings_embed)
        return
    
    current_date = datetime.now().date()

    if ctx.guild.id != 1103936072989278279:
        await ctx.send("La commande n'est pas disponible sur les autres serveurs")
        return
    
    loading_message = await ctx.send("Chargement de vos données")
    await asyncio.sleep(1)
    await loading_message.edit(content="Chargement de vos données <a:loading:1112807489042399333>")
    await asyncio.sleep(3)
    await loading_message.delete()

    last_daily = user_data.get("last_daily")
    daily_streak = user_data.get("daily_streak", 0)
    cost = daily_streak * 2500

    if last_daily and last_daily.date() == current_date:
        await ctx.send("Vous avez déjà récupéré votre récompense quotidienne aujourd'hui.")
        return

    if user_data_balance["balance"] < cost:
        await ctx.send(f"Vous n'avez pas assez de pièces pour réparer votre série quotidienne. Vous avez besoin de {cost} pièces.")
        return

    confirmation_message = await ctx.send(f"Voulez-vous acheter la réparation de votre série quotidienne pour {cost} pièces ? Réagissez avec ✅ pour confirmer ou ❌ pour annuler.")
    await confirmation_message.add_reaction("✅")
    await confirmation_message.add_reaction("❌")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == confirmation_message.id

    try:
        reaction, _ = await bot.wait_for("reaction_add", timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("Temps écoulé, la réparation de la série quotidienne a été annulée.")
        return

    if str(reaction.emoji) == "✅":
        user_data_balance["balance"] -= cost
        save_user_money(server_id, user_id, user_data_balance)

        if last_daily and last_daily.date() < current_date - timedelta(days=1):
            await ctx.send("Récupération de votre série en cours.")
        else:
            await ctx.send("Votre série a déjà été récupérée.")

        user_data["last_daily"] = current_date - timedelta(days=1)
        user_data["daily_streak"] = daily_streak + 1
        save_user_data_daily(user_id, user_data)

        await ctx.send(f"Série quotidienne récupérée !")
    else:
        await ctx.send("La réparation de la série quotidienne a été annulée.")

@bot.hybrid_group()
@commands.has_permissions(administrator=True)
async def shield(ctx):
    if ctx.invoked_subcommand is None:
        embed = discord.Embed(
            title="Commande incorrecte",
            description="Utilisez `?shield add/remove/reset/set [MENTION OU USERID] [TEMPS EN SECONDE]` ou `?shield global [TEMPS EN SECONDE]`.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@shield.command(description="Remplace une protection à la personne séléctionnée, temps en secondes")
async def add(ctx, target: discord.Member, time: int):
    if isinstance(target, discord.Member):
        cooldowns[target.id] = datetime.now() + timedelta(seconds=time)
        embed = discord.Embed(
            title="Protection ajoutée",
            description=f"{target.mention} a maintenant une protection supplémentaire de {time} secondes.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Erreur",
            description="Veuillez mentionner un utilisateur valide.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@shield.command(description="Retirer du temps de protection /steal à une personne")
async def remove(ctx, target: discord.Member):
    if target.id in cooldowns:
        del cooldowns[target.id]
        embed = discord.Embed(
            title="Protection supprimée",
            description=f"La protection de {target.mention} a été supprimée.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Erreur",
            description=f"{target.mention} n'a pas de protection active.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@shield.command(description="Retirer toute la protection d'une personne")
async def reset(ctx):
    cooldowns.clear()
    embed = discord.Embed(
        title="Protections réinitialisées",
        description="Toutes les protections ont été réinitialisées.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.hybrid_command(description="Gamble un montant au hasard")
@commands.cooldown(1, 30*3, commands.BucketType.user)
async def gamble(ctx, amount: int):
    server_id = ctx.guild.id
    user_id = ctx.author.id

    user_money = load_user_money(server_id, user_id)
    user_balance = user_money.get("balance", 0)
    
    settings_embed = await check_settings(server_id, user_id)
    if settings_embed is not None:
        await ctx.send(embed=settings_embed)
        return
    
    if amount <= 999:
        embed = discord.Embed(title="Erreur", description="Le montant doit être supérieur à 1000.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    if ctx.guild.id != 1103936072989278279:
        if amount >= 10001:
            embed = discord.Embed(title="Erreur", description="Le montant doit être inferieur ou égal à 10000.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
    else:
        if any(role.id == 1103936073043820569 for role in ctx.author.roles):
            if amount > 20000:
                embed = discord.Embed(title="Erreur", description="Le montant doit être inférieur ou égal à 20000.\n Si vous souhaitez obtenir une limite de mise supérieure, merci de devenir membre du personnel.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return
        elif any(role.id == 1103936073043820571 for role in ctx.author.roles):
            if amount > 50000:
                embed = discord.Embed(title="Erreur", description="Le montant doit être inférieur ou égal à 50000.\n Si vous souhaitez obtenir une limite de mise supérieure, merci de devenir Administrateur.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return
        elif any(role.id == 1103936073043820572 for role in ctx.author.roles):
            if amount > 100000:
                embed = discord.Embed(title="Erreur", description="Le montant doit être inférieur ou égal à 100000.\n Si vous souhaitez obtenir une limite de mise supérieure, merci de devenir Fondateur.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return
        elif any(role.id == 1103936073043820573 for role in ctx.author.roles):
            if amount > 250000:
                embed = discord.Embed(title="Erreur", description="Le montant doit être inférieur ou égal à 250000.\n Si vous souhaitez obtenir une limite de mise supérieure, merci de devenir à rien ducoup.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return
        elif amount > 10000:
            embed = discord.Embed(title="Erreur", description="Le montant doit être inférieur ou égal à 10000.\n Si vous souhaitez obtenir une limite de mise supérieure, faites la commande `?rewards` et achetez le rang Première Classe.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return


    if amount > user_balance:
        embed = discord.Embed(title="Erreur", description="Vous n'avez pas assez d'argent pour effectuer ce pari.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    

    if ctx.guild.id != 1103936072989278279:
        win_chance = 0.40
    
    if ctx.guild.id == 1103936072989278279:  
        if any(role.id == 1127529310564122685 for role in ctx.author.roles):
            win_chance = 0.45
            await ctx.send("Boost de chance appliqué avec succès !")
            await asyncio.sleep(5)
        elif any(role.id == 1145682223912202251 for role in ctx.author.roles):
            win_chance = 0.85
            await ctx.send("Boost de chance appliqué avec succès !")
            await asyncio.sleep(5)
        else:
            win_chance = 0.40

    if random.random() < win_chance:
        win_amount = amount
        user_balance += win_amount

        embed = discord.Embed(
            title="Pari réussi",
            description=f"Vous avez gagné {win_amount} pièces ! Votre solde actuel est de {user_balance} pièces.",
            color=discord.Color.green()
        )
    else:
        user_balance -= amount

        embed = discord.Embed(
            title="Pari perdu",
            description=f"Vous avez perdu {amount} pièces. Votre solde actuel est de {user_balance} pièces.",
            color=discord.Color.red()
        )

    user_money["balance"] = user_balance
    save_user_money(server_id, user_id, user_money)

    await ctx.send(embed=embed)

@bot.hybrid_command(description="La roulette tourne !")
@commands.cooldown(1, 30, commands.BucketType.user)
async def roulette(ctx, nombre: int, mise: int):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)
    
    user_data = load_user_money(server_id, user_id)
    
    settings_embed = await check_settings(server_id, user_id)
    if settings_embed is not None:
        await ctx.send(embed=settings_embed)
        return
    
    if user_data["balance"] < mise:
        await ctx.send("Vous n'avez pas assez d'argent pour miser cette somme.")
        return
    
    if mise <= 5:
        await ctx.send("La mise doit être supérieure à cinq !")
        return
    
    user_data["balance"] -= mise
    save_user_money(server_id, user_id, user_data)
    
    results = [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"]
    
    roulette_message = await ctx.send("<a:offline_status:1129880911106818158> La roulette tourne...")
    
    for _ in range(10):
        await asyncio.sleep(1)
        random_number = random.randint(0, 9)
        result = results[random_number]
        await roulette_message.edit(content=f"<a:offline_status:1129880911106818158> La roulette tourne... Peut-être : {result}")
    
    await asyncio.sleep(1)
    await roulette_message.edit(content="<a:offline_status:1129880911106818158> La roulette ralentit...")
    await asyncio.sleep(1)
    
    random_number = random.randint(0, 9)

    result = results[random_number]
    
    await roulette_message.edit(content=f"Le résultat de la roulette est : {result}")
    
    
    if nombre == random_number:
        gain = mise * 10
        user_data["balance"] += gain
        save_user_money(server_id, user_id, user_data)
        await ctx.send(f"Bravo ! Vous avez gagné {gain} <a:money:1118983615418728508>.")
    else:
        await ctx.send(f"Dommage ! Vous avez perdu {mise} <a:money:1118983615418728508>.")



@bot.hybrid_command(description="Organise un drop d'argent sur ton serveur")
@commands.has_permissions(administrator=True)
async def drop(ctx, amount: int, people_amount: int):
    
    embed = discord.Embed(title="Récompenses journalières", description=f"Les {people_amount} premières personnes qui réagissent à ce message avec la réaction <a:money:1118983615418728508> gagnéont {amount} <a:money:1118983615418728508>.")

    message = await ctx.send(embed=embed)
    await message.add_reaction("<a:money:1118983615418728508>")

    def check(reaction, user):
        return user != bot.user and str(reaction.emoji) == "<a:money:1118983615418728508>"

    try:
        reacted_users = []
        while len(reacted_users) < people_amount:
            reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
            if not user.bot and user not in reacted_users:
                reacted_users.append(user)
    except asyncio.TimeoutError:
        await ctx.send("Temps écoulé, nombre insuffisant de personnes ayant réagi.")
    else:
        winners = []
        for user in reacted_users:
            user_data = load_user_money(str(ctx.guild.id), str(user.id))
            user_data["balance"] += amount
            save_user_money(str(ctx.guild.id), str(user.id), user_data)
            winners.append(user.mention)
        
        winners_text = "\n".join(winners)
        await ctx.send(f"Les {people_amount} premières personnes ont gagné {amount} <a:money:1118983615418728508>:\n{winners_text}")

@bot.hybrid_group()
async def duel(ctx):
    if ctx.invoked_subcommand is None:
        embed = discord.Embed(title="Commande : Duel", description="Défie un autre joueur dans un duel dactylographique ou de question", color=discord.Color.blue())
        embed.add_field(name="Utilisation", value="?duel [dactylo/question] [opponent] [bet]")
        await ctx.send(embed=embed)

duel_in_progress = {}

@duel.command(description="Mini-jeu de question en duo, Génération par IA Incorrecte parfois.")
async def question(ctx, opponent: discord.User, bet: int):
    if opponent is None or bet is None:
        embed = discord.Embed(
            title="Commande : Duel",
            description="Défie un autre joueur dans un duel dactylographique.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Utilisation", value="?duel [opponent] [bet]")
        embed.add_field(
            name="Description", 
            value="Défie un autre joueur dans un duel dactylographique. Vous devez spécifier l'adversaire et la mise."
        )
        await ctx.send(embed=embed)
        return
    
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)
    opponent_id = str(opponent.id)
    
    if opponent_id == user_id:
        await ctx.send("Vous ne pouvez pas jouer contre vous-même.")
        return
    
    settings_embed = await check_settings(server_id, user_id)
    if settings_embed is not None:
        await ctx.send(embed=settings_embed)
        return
    
    ban_info = check_user_ban_status(server_id, opponent_id)
    if ban_info is not None:
        reason, admin_id = ban_info
        admin = bot.get_user(admin_id)
        embed = discord.Embed(title="Compte Monétaire suspendu", description=f"Le compte monétaire de votre adversaire à été suspendu.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    user_data = load_user_money(server_id, user_id)
    opponent_data = load_user_money(server_id, opponent_id)
    
    user_balance = user_data["balance"]
    opponent_balance = opponent_data["balance"]
    
    if bet <= 0:
        await ctx.send("La mise doit être supérieure à zéro.")
        return
    
    if bet > user_balance or bet > opponent_balance:
        await ctx.send("L'un des joueurs n'a pas assez d'argent pour miser cette somme.")
        return
    
    if user_id in duel_in_progress or opponent_id in duel_in_progress:
        await ctx.send("Un duel est déjà en cours entre ces deux joueurs.")
        return
    
    duel_in_progress[user_id] = True
    duel_in_progress[opponent_id] = True
    
    def check_reaction(reaction, user):
        return user == opponent and str(reaction.emoji) == "<a:BlackHD:1112807458507858061>"
    
    def check_message(message):
        return message.author == ctx.author and message.channel == ctx.channel
    
    duel_message = await ctx.send(
        f"{opponent.mention}, vous avez été défié par {ctx.author.mention} pour un duel de **question**."
        f"\nMise : **{bet}** <a:money:1118983615418728508>."
        f"\nCliquez sur <a:BlackHD:1112807458507858061> pour accepter le duel."
    )
    
    await duel_message.add_reaction("<a:BlackHD:1112807458507858061>")
    
    try:
        reaction, _ = await bot.wait_for("reaction_add", timeout=60, check=check_reaction)
    except asyncio.TimeoutError:
        await ctx.send(f"{opponent.mention} n'a pas accepté le duel à temps.")
        duel_in_progress.pop(user_id)
        duel_in_progress.pop(opponent_id)
        return
    
    await duel_message.delete()
    
    questions = [
        ("quel est le président de la Russie ?", "vladimir poutine"),
        ("quel est le nombre de côtés d'un pentagone ?", "5"),
        ("quelle est la capitale de l'inde ?", "new delhi"),
        ("quelle est la plus haute montagne du monde ?", "everest"),
        ("quel est l'instrument de musique le plus populaire ?", "guitare"),
        ("quel est le plus grand pays d'Amérique du Sud ?", "brésil"),
        ("quel est l'animal national de l'Australie ?", "kangourou"),
        ("quel est le pays le plus vaste du monde ?", "russie"),
        ("quel est le plus petit état des États-Unis ?", "rhode island"),
        ("quelle est la capitale de l'Angleterre ?", "londres"),
        ("quel est le symbole chimique du carbone ?", "c"),
        ("quel est le premier président des États-Unis ?", "george washington"),
        ("quel est le plus grand lac d'Afrique ?", "lac victoria"),
        ("quel est le plus petit océan du monde ?", "océan arctique"),
        ("quel est le pays le plus froid du monde ?", "russie"),
        ("quel est le pays le plus peuplé d'Europe ?", "russie"),
        ("quel est l'animal terrestre le plus lourd ?", "éléphant"),
        ("quel est le nombre de joueurs dans une équipe de basketball ?", "5"),
        ("quel est le plus grand parc national du Canada ?", "parc national de Wood Buffalo"),
        ("quel est le pays le plus grand d'Amérique ?", "canada"),
        ("quel est le plus grand lac d'Amérique du Nord ?", "lac supérieur"),
        ("quelle est la capitale de la Chine ?", "pekin"),
        ("quelle est la plus grande ville d'Afrique ?", "Caire"),
        ("quel est le symbole chimique du fer ?", "fe"),
        ("quel est le président de la France ?", "emmanuel macron"),
        ("quel est le plus grand animal marin ?", "baleine bleue"),
        ("quel est le pays le plus proche de l'Antarctique ?", "Australie"),
        ("quel est le résultat de 10 - 5 ?", "5"),
        ("quel est le nombre de lettres dans l'alphabet français ?", "26"),
        ("quelle est la capitale de l'Italie ?", "rome"),
        ("quel est le plus grand pays d'Asie ?", "russie"),
        ("quel est le plus grand océan du monde ?", "océan pacifique"),
        ("quel est le mammifère qui vole ?", "chauve-souris"),
        ("quel est le pays d'origine du sushi ?", "japon"),
        ("quel est le nombre de joueurs dans une équipe de volley-ball ?", "6"),
        ("quelle est la devise des États-Unis ?", "in god we trust"),
        ("quel est le plus grand désert froid du monde ?", "antarctique"),
        ("quel est le symbole chimique du cuivre ?", "cu"),
        ("quel est le président de la Russie ?", "vladimir poutine"),
        ("quel est le plus grand océan de l'Atlantique Sud ?", "océan atlantique"),
        ("quel est le pays le plus montagneux du monde ?", "bhoutan"),
        ("quel est le plus petit pays d'Amérique centrale ?", "salvador"),
        ("quel est le plus grand pays d'Amérique du Nord ?", "les états-unis"),
        ("quelle est la capitale de l'Argentine ?", "buenos aires"),
        ("quel est l'animal le plus rapide du monde ?", "guépard"),
        ("quel est le symbole chimique du calcium ?", "ca"),
        ("quel est le plus grand océan de l'Atlantique Nord ?", "océan atlantique"),
        ("quel est le pays le plus chaud du monde ?", "maroc"),
        ("quel est le plus grand état des États-Unis ?", "alaska"),
        ("quel est le plus petit continent du monde ?", "océanie"),
        ("quel est le nombre de membres dans les Beatles ?", "4"),
        ("quel est le plus grand parc national de France ?", "parc national des Cévennes"),
        ("quel est le pays le plus industrialisé du monde ?", "chine"),
        ("quelle est la capitale du Brésil ?", "brasília"),
        ("quel est le plus grand océan de l'Antarctique ?", "océan antarctique"),
        ("quel est le pays le plus riche du monde ?", "qatar"),
        ("quel est le plus grand désert chaud du monde ?", "sahara"),
        ("quel est le symbole chimique de l'argent ?", "ag"),
        ("quel est le président de la Turquie ?", "recep tayyip erdogan"),
        ("quel est le plus grand lac d'Amérique du Sud ?", "titicaca"),
        ("quel est le plus petit état du monde ?", "vatican"),
        ("quelle est la capitale de l'Égypte ?", "Caire"),
        ("quel est l'instrument de musique le plus ancien ?", "flûte"),
        ("quel est le nombre de membres dans un quatuor à cordes ?", "4"),
        ("quel est le pays le plus démocratique du monde ?", "norvège"),
        ("quel est le plus grand lac d'Amérique ?", "lac supérieur"),
        ("Qui est le meilleur owner de serveur ?", "pilote production"),
        ("quel est le plus grand océan de l'océan Indien ?", "océan indien"),
        ("quel est le président de l'Allemagne ?", "frank-walter steinmeier"),
        ("quel est le plus grand volcan du monde ?", "mauna loa"),
        ("quel est le pays le plus densément peuplé du monde ?", "monaco"),
        ("quel est le plus grand pays d'Amérique du Sud ?", "brésil"),
        ("quelle est la capitale de la Russie ?", "moscou"),
        ("quel est le plus grand lac d'Europe ?", "lac ladoga"),
        ("quel est le plus long fleuve d'Amérique ?", "mississippi"),
        ("quel est le nombre de pattes d'un mille-pattes ?", "1000"),
        ("quel est le symbole chimique du potassium ?", "k"),
        ("quel est le président de l'Espagne ?", "pedro sánchez"),
        ("quel est le plus grand océan de l'océan Atlantique ?", "océan atlantique"),
        ("quel est le pays le plus touristique d'Amérique du Sud ?", "brésil"),
        ("quelle est la capitale de la Grèce ?", "athènes"),
        ("quel est le plus grand désert de glace du monde ?", "antarctique"),
        ("quel est le symbole chimique du magnésium ?", "mg"),
        ("quel est le président du Mexique ?", "andrés manuel lópez obrador"),
        ("quel est le plus grand lac d'Asie ?", "lac baikal"),
        ("quel est le plus petit pays d'Asie ?", "les maldives"),
        ("quel est le plus grand pays d'Amérique centrale ?", "nicaragua"),
        ("quelle est la capitale de la Colombie ?", "bogotá"),
        ("quel est le plus grand océan de l'océan Pacifique ?", "océan pacifique"),
        ("quel est le pays le plus sûr au monde ?", "islande"),
        ("quel est le plus grand désert du continent africain ?", "désert du sahara"),
        ("quel est le symbole chimique du zinc ?", "zn"),
        ("quel est le président de l'Italie ?", "sergio mattarella"),
        ("quel est le plus grand lac d'Océanie ?", "lac eyre"),
        ("quel est le plus grand pays d'Amérique ?", "canada"),
        ("quelle est la capitale de l'Afrique du Sud ?", "pretoria"),
        ("quel est le plus grand océan de l'océan Arctique ?", "océan arctique"),
        ("quel est le pays le plus riche d'Afrique ?", "afrique du sud"),
        ("quel est le plus grand désert du continent européen ?", "désert de tabernas"),
        ("quel est le symbole chimique de l'aluminium ?", "al"),
        ("quel est le président du Canada ?", "justin trudeau"),
        ("quel est le plus grand lac d'Amérique du Nord ?", "lac supérieur"),
        ("quel est le nombre de membres dans un quintette à vent ?", "5"),
        ("quel est le plus grand parc national d'Amérique du Sud ?", "parc national de torres del paine"),
        ("quel est le pays le plus développé d'Amérique ?", "les états-unis"),
        ("quelle est la capitale de l'Arabie saoudite ?", "riyad"),
        ("quel est le plus grand océan de l'océan Austral ?", "océan austral"),
        ("quel est le pays le plus pauvre du monde ?", "burundi"),
        ("quel est le plus grand désert du continent asiatique ?", "désert de gobi"),
        ("quel est le symbole chimique de l'uranium ?", "u"),
        ("quelle est la couleur du ciel ?", "bleu"),
        ("quel animal dit 'meow' ?", "chat"),
        ("quel est le contraire de 'oui' ?", "non"),
        ("quel est le fruit le plus couramment utilisé pour faire de la confiture ?", "fraise"),
        ("combien de mois ont 28 jours ?", "12"),
        ("quel est le légume qui pleure tout le temps ?", "oignon"),
        ("quel est l'animal terrestre le plus rapide ?", "guépard"),
        ("qu'est-ce qui devient plus mouillé lorsqu'il sèche ?", "une serviette"),
        ("quel est le mot le plus long de la langue française ?", "anticonstitutionnellement"),
        ("quel est l'insecte qui produit le miel ?", "abeille"),
        ("quel est le pays le plus peuplé du monde ?", "chine"),
        ("quel est le plus grand océan de la terre ?", "océan pacifique"),
        ("quel est le mont le plus haut du monde ?", "everest"),
        ("quel est le mammifère marin le plus gros ?", "baleine bleue"),
        ("quel est le président des états-unis ?", "joe biden"),
        ("quel est le numéro atomique de l'oxygène ?", "8"),
        ("quelle est la capitale de l'espagne ?", "madrid"),
        ("quelle est la planète la plus proche du soleil ?", "mercure"),
        ("quelle est la devise de la france ?", "liberté, égalité, fraternité"),
        ("qui a peint la joconde ?", "léonard de vinci"),
        ("quel est le plus grand désert du monde ?", "sahara"),
        ("quel est le nombre de pattes d'une araignée ?", "8"),
        ("quel est le symbole chimique de l'or ?", "au"),
        ("quel est le pays d'origine de la pizza ?", "italie"),
        ("quel est le résultat de 2 + 2 ?", "4"),
        ("quel est le personnage principal du livre 'orgueil et préjugés' ?", "elizabeth bennet"),
        ("quel est le plus grand animal terrestre ?", "éléphant"),
        ("quel est le pays le plus petit du monde ?", "vatican"),
        ("quel est l'élément le plus abondant dans l'univers ?", "hydrogène"),
        ("quelle est la capitale du canada ?", "ottawa"),
        ("quel est le plus grand lac du monde ?", "mer caspienne"),
        ("quel est le nombre de joueurs dans une équipe de football ?", "11"),
        ("quelle est la capitale de l'australie ?", "canberra"),
        ("quel est le symbole chimique du sodium ?", "na"),
        ("quel est le continent le plus peuplé ?", "asie"),
        ("quelle est la capitale du japon ?", "tokyo"),
        ("quel est le plus long fleuve du monde ?", "amazone"),
        ("quel est le pays le plus visité au monde ?", "france"),
        ("quel est le plus grand organe du corps humain ?", "peau"),
        ("quelle est la capitale de l'allemagne ?", "berlin"),
        ("quel est le plus grand parc national des états-unis ?", "wrangell-st. elias"),
        ("Quel est le fruit le plus couramment utilisé pour faire de la confiture ?", "fraise"),
        ("Combien de mois ont 28 jours ?", "12"),
        ("Quel est le légume qui pleure tout le temps ?", "oignon"),
        ("Quel est l'animal terrestre le plus rapide ?", "guépard"),
        ("Qu'est-ce qui devient plus mouillé lorsqu'il sèche ?", "serviette"),
        ("Quel est le mot le plus long de la langue française ?", "anticonstitutionnellement"),
        ("Quel est l'insecte qui produit le miel ?", "abeille"),
        ("Quel est le pays le plus peuplé du monde ?", "Chine"),
        ("Quel est le plus grand océan de la Terre ?", "océan Pacifique"),
        ("Quel est le mont le plus haut du monde ?", "Everest"),
        ("Quel est le mammifère marin le plus gros ?", "baleine bleue"),
        ("Quel est le président des États-Unis ?", "Joe Biden"),
        ("Quel est le numéro atomique de l'oxygène ?", "8"),
        ("Quelle est la capitale de l'Espagne ?", "Madrid"),
        ("Quelle est la planète la plus proche du soleil ?", "Mercure"),
        ("Quelle est la devise de la France ?", "Liberté, Égalité, Fraternité"),
        ("Qui a peint la Joconde ?", "Léonard de Vinci"),
        ("Quel est le plus grand désert du monde ?", "Sahara"),
        ("Quel est le nombre de pattes d'une araignée ?", "8"),
        ("Quel est le symbole chimique de l'or ?", "Au"),
        ("Quel est le pays d'origine de la pizza ?", "Italie"),
        ("Quel est le résultat de 2 + 2 ?", "4"),
        ("Quel est le personnage principal du livre 'Orgueil et Préjugés' ?", "Elizabeth Bennet"),
        ("Quel est le plus grand animal terrestre ?", "éléphant"),
        ("Quel est le pays le plus petit du monde ?", "Vatican"),
        ("Quel est l'élément le plus abondant dans l'univers ?", "hydrogène"),
        ("Quelle est la capitale du Canada ?", "Ottawa"),
        ("Quel est le plus grand lac du monde ?", "mer Caspienne"),
        ("Quel est le nombre de joueurs dans une équipe de football ?", "11"),
        ("Quelle est la capitale de l'Australie ?", "Canberra"),
        ("Quel est le symbole chimique du sodium ?", "Na"),
        ("Quel est le continent le plus peuplé ?", "Asie"),
        ("Quelle est la capitale du Japon ?", "Tokyo"),
        ("Quel est le plus long fleuve du monde ?", "Amazone"),
        ("Quel est le pays le plus visité au monde ?", "France"),
        ("Quel est le plus grand organe du corps humain ?", "peau"),
        ("Quelle est la capitale de l'Allemagne ?", "Berlin"),
        ("Quel est le plus grand parc national des États-Unis ?", "Wrangell-St. Elias"),
        ("Qui est le plus beau `Pilote` ou `Peluche`", "pilote"),
    ]
    
    random_question = random.choice(questions)
    question_text = random_question[0]
    answer = random_question[1]
    
    user_balance -= bet
    opponent_balance -= bet

    if bet > user_balance or bet > opponent_balance:
        await ctx.send("L'un des joueurs n'a pas assez d'argent pour miser cette somme.")
        return
    
    if bet > opponent_balance or bet > opponent_balance:
        await ctx.send("L'un des joueurs n'a pas assez d'argent pour miser cette somme.")
        return

    user_data["balance"] = user_balance
    opponent_data["balance"] = opponent_balance
    
    save_user_money(server_id, user_id, user_data)
    save_user_money(server_id, opponent_id, opponent_data)
    
    ready_message = await ctx.send("Prêt ?")
    await asyncio.sleep(random.randint(1, 25))
    await ready_message.delete()
    await ctx.send(f"Voici la question : {question_text}")
    
    def check_message(message):
        return message.author == ctx.author or message.author == opponent
    
    try:
        message = await bot.wait_for("message", timeout=10, check=check_message)
        
        if message.content.lower() == answer.lower():
            if message.author == ctx.author:
                user_balance += bet * 2
                user_data["balance"] = user_balance
                save_user_money(server_id, user_id, user_data)
                await ctx.send(f"{ctx.author.mention} a gagné le duel et remporte {bet * 2} <a:money:1118983615418728508>.")
                duel_in_progress.pop(user_id)
                duel_in_progress.pop(opponent_id)
            else:
                opponent_balance += bet * 2
                opponent_data["balance"] = opponent_balance
                save_user_money(server_id, user_id, user_data)
                await ctx.send(f"{opponent.mention} a gagné le duel et remporte {bet * 2} <a:money:1118983615418728508>.")
                duel_in_progress.pop(user_id)
                duel_in_progress.pop(opponent_id)
        else:
            if message.author == ctx.author:
                opponent_balance += bet * 2
                opponent_data["balance"] = opponent_balance
                save_user_money(server_id, opponent_id, opponent_data)
                await ctx.send(f"{opponent.mention} a gagné le duel et remporte {bet * 2} <a:money:1118983615418728508>.\n {ctx.author.mention} a fait une erreur.\n La réponse était `{answer}`")
                duel_in_progress.pop(user_id)
                duel_in_progress.pop(opponent_id)
            else:
                user_balance += bet * 2
                user_data["balance"] = user_balance
                save_user_money(server_id, user_id, user_data)
                await ctx.send(f"{ctx.author.mention} a gagné le duel et remporte {bet * 2} <a:money:1118983615418728508>. {opponent.mention} a fait une erreur.\n La réponse était `{answer}`")
                duel_in_progress.pop(user_id)
                duel_in_progress.pop(opponent_id)
    except asyncio.TimeoutError:
        await ctx.send(f"Aucun joueur n'a écrit de message à temps. \n La réponse était `{answer}`.")
        opponent_balance += bet 
        user_balance += bet
        user_data["balance"] = user_balance
        opponent_data["balance"] = opponent_balance
        save_user_money(server_id, user_id, user_data)
        save_user_money(server_id, opponent_id, opponent_data)
        duel_in_progress.pop(user_id)
        duel_in_progress.pop(opponent_id)
        return

@duel.command(description="Mini-jeu de rapidité difficile en duo (normalement)")
async def dactylo(ctx, opponent: discord.User, bet: int):
    if opponent is None or bet is None:
        embed = discord.Embed(title="Commande : Duel", description="Défie un autre joueur dans un duel dactylographique.", color=discord.Color.blue())
        embed.add_field(name="Utilisation", value="?duel [opponent] [bet]")
        embed.add_field(name="Description", value="Défie un autre joueur dans un duel dactylographique. Vous devez spécifier l'adversaire et la mise.")
        await ctx.send(embed=embed)
        return
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)
    opponent_id = str(opponent.id)

    if opponent_id == user_id:
        await ctx.send("Vous ne pouvez pas jouer contre vous-même.")
        return
    
    settings_embed = await check_settings(server_id, user_id)
    if settings_embed is not None:
        await ctx.send(embed=settings_embed)
        return
    
    ban_info = check_user_ban_status(server_id, opponent_id)
    if ban_info is not None:
        reason, admin_id = ban_info
        admin = bot.get_user(admin_id)
        embed = discord.Embed(title="Compte Monétaire suspendu", description=f"Le compte monétaire de votre adversaire à été suspendu.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    user_data = load_user_money(server_id, user_id)
    opponent_data = load_user_money(server_id, opponent_id)
    
    user_balance = user_data["balance"]
    opponent_balance = opponent_data["balance"]
    
    if bet <= 0:
        await ctx.send("La mise doit être supérieure à zéro.")
        return
    
    if bet > user_balance or bet > opponent_balance:
        await ctx.send("L'un des joueurs n'a pas assez d'argent pour miser cette somme.")
        return
    
    def check_reaction(reaction, user):
        return user == opponent and str(reaction.emoji) == "<a:BlackHD:1112807458507858061>"
    
    duel_message = await ctx.send(f"{opponent.mention}, vous avez été défié par {ctx.author.mention} pour un duel dactylographique. \nMise : **{bet}** <a:money:1118983615418728508>. \nCliquez sur <a:BlackHD:1112807458507858061> pour accepter le duel.")
    
    if user_id in duel_in_progress or opponent_id in duel_in_progress:
        await ctx.send("Un duel est déjà en cours entre ces deux joueurs.")
        return
    
    duel_in_progress[user_id] = True
    duel_in_progress[opponent_id] = True

    await duel_message.add_reaction("<a:BlackHD:1112807458507858061>")
    
    try:
        reaction, _ = await bot.wait_for("reaction_add", timeout=60, check=check_reaction)
    except asyncio.TimeoutError:
        await ctx.send(f"{opponent.mention} n'a pas accepté le duel à temps.")
        duel_in_progress.pop(user_id)
        duel_in_progress.pop(opponent_id)
        return
    
    await duel_message.delete()
    

    user_balance -= bet
    opponent_balance -= bet
    
    user_data["balance"] = user_balance
    opponent_data["balance"] = opponent_balance
    
    save_user_money(server_id, user_id, user_data)
    save_user_money(server_id, opponent_id, opponent_data)
    
    ready_message = await ctx.send("Prêt ?")
    await asyncio.sleep(random.randint(1, 25))
    await ready_message.delete()

    random_word = random.choice(["chat", "chien", "maison", "jardin", "ordinateur", "banane", "pilote", "tom", "giveaways", "actif", "moulag", "abaissement", "abandon", "abasourdi", "abattement", "abattre", "abeille", "aberrant", "abîme", "abolir", "abondance", "aborder", "aboutir", "aboyer", "abrasif", "abreuver", "abriter", "abroger", "absence", "absolu", "absorber", "abstrait", "absurde", "abusif", "abyssal", "académie", "acajou", "acarien", "accabler", "accepter", "acclamer", "accolade", "accorder", "accrocher", "accuser", "acerbe", "acharné", "achat", "acheter", "acier", "acolyte", "acquis", "acrobate", "acteur", "actif", "action", "actuel", "adage", "adapter", "addition", "adepte", "adieu", "admettre", "admirer", "adolescent", "adoption", "adrénaline", "adulte", "adverbe", "aérer", "aérobie", "aéroport", "aérostat", "affaiblir", "affamé", "affection", "affiche", "affoler", "affranchir", "affronter", "agenda", "agile", "agiter", "agonie", "agrafer", "agréable", "agrume", "aider", "aiguille", "aileron", "aimable", "ajouter", "ajuster", "alarme", "alchimie", "alerte", "algèbre", "algorithme", "alias", "alibi", "aliment", "aliter", "alizé", "alléger", "alléluia", "alliance", "allonger", "allumer", "alors", "alourdir", "alpaga", "altesse", "alvéole", "amateur", "ambigu", "ambre", "ambulance", "améliorer", "aménager", "amertume", "amidon", "amiral", "amorcer", "amour", "ampoule", "amulette", "amusant", "analyse", "ananas", "anarchie", "anatomie", "ancien", "ange", "anglais", "angoisse", "angulaire", "animal", "annexe", "annonce", "annuel", "anodin", "anomalie", "antenne", "antidote", "anxiété", "apaiser", "apéritif", "aplanir", "apologie", "appareil", "appeler", "apporter", "apprendre", "approcher", "approuver", "arbitre", "arbuste", "arche", "ardoise", "argent", "aride", "armature", "armement", "armoire", "aromatiser", "arracher", "arrêter", "arriver", "arroser", "arsenal", "artériel", "article", "aspect", "asphalte", "aspirer", "assaut", "asseoir", "assiette", "associer", "assumer", "assurer", "asticot", "astre", "astuce", "atelier", "atome", "atout", "atroce", "attacher", "attaque", "attente", "attirer", "attraper", "aubaine", "auberge", "audace", "audible", "augmenter", "aurore", "automne", "autre", "avaler", "avancer", "aventure", "avertir", "aveugle", "aviation", "avide", "avion", "aviser", "avoine", "avouer", "avril", "axial", "axiome", "badge", "bafouer", "bagage", "baguette", "baignade", "balancer", "balcon", "balise", "ballon", "bambou", "banane", "banc", "bandage", "banjo", "banlieue", "bannière", "banquier", "barbier", "baril", "baron", "barque", "barrage", "barre", "barrière", "baryum", "basalt", "bascule", "base", "bassin", "batterie", "bavarder", "belette", "bélier", "belote", "bénéfice", "berceau", "berger", "berline", "bermuda", "besace", "besoin", "bétail", "beurre", "biais", "biceps", "bidule", "bière", "bifteck", "bijou", "bilan", "billet", "binôme", "biologie", "biopsie", "bière", "biscuit", "bison", "bitume", "bizarre", "blâmer", "blanc", "blé", "blond", "bloquent", "blouse", "blouson", "bobine", "boire", "boisson", "boîte", "bonbon", "bondir", "bonheur", "bonjour", "bonus", "bordure", "borgne", "borner", "bosse", "bouche", "boucle", "boueux", "bougie", "boulon", "bouquet", "bourgeon", "boussole", "boutique", "boxeur", "brader", "braise", "branche", "bras", "brave", "bravo", "brèche", "brevet", "brider", "brigade", "briller", "brin", "brioche", "brique", "briser", "broche", "broder", "bronze", "brosser", "brouter", "bruit", "brûler", "brume", "brusque", "brutal", "bruyant", "bûche", "budget", "buffet", "bugle", "buisson", "bulletin", "bureau", "burin", "buste", "butin", "buvable", "buvette", "cabane", "cabine", "câble", "cache", "cadeau", "cadre", "café", "cage", "caillou", "caisson", "calcul", "caleçon", "calibre", "calice", "calme", "camarade", "caméra", "camion", "campagne", "canal", "canard", "cancer", "caniche", "canne", "canon", "canot", "cantine", "canular", "capable", "capot", "capturer", "caractère", "carbone", "caresser", "carotte", "carreau", "carte", "casier", "casque", "casserole", "cause", "cavalier", "caverne", "caviar", "ceinture", "cela", "céleste", "cellule", "cendre", "censurer", "cent", "céder", "ceinture", "cercle", "cerise", "cerner", "cerveau", "cesser", "chacal", "chaise", "chaleur", "chambre", "chamois", "champion", "chance", "change", "chanson", "chant", "chaos", "chapeau", "charbon", "chasse", "chat", "chaud", "chaussette", "chauve", "chavirer", "chemin", "chenille", "cheveu", "cheville", "chez", "chiffre", "chimie", "chiot", "chirurgie", "chocolat", "choisir", "chose", "chou", "chut", "ciel", "cigare", "cigare", "cigogne", "cimenter", "cinéma", "cire", "cirque", "ciseau", "citation", "citron", "civique", "clair", "clameur", "clan", "clapet", "classe", "clavier", "client", "cligner", "climat", "cloche", "cloner", "clôture", "clown", "cocon", "coiffe", "coin", "colline", "colon", "colore", "combat", "comédie", "commande", "commencer", "comment", "commercer", "complet", "complot", "comprendre", "compter", "conduire", "confier", "congeler", "congrès", "conique", "connaître", "conquérir", "consoler", "conte", "continuer", "convaincre", "copain", "copie", "corde", "corne", "corps", "corridor", "cosmos", "costume", "coton", "couche", "coude", "couler", "coup", "couple", "cour", "courage", "courbe", "coussin", "couteau", "couvrir", "crabe", "cracher", "craindre", "crainte", "cravate", "crayon", "crème", "créature", "crédit", "créer", "creuser", "crevette", "crible", "crier", "crime", "crinoline", "crise", "crochet", "croire", "croisière", "croquer", "crotte", "croupe", "croyance", "cruche", "crustacé", "cube", "cuisine", "cuivre", "culotte", "cultiver", "cumulus", "curieux", "cycle", "cylindre", "dague", "daigner", "dame", "danger", "danse", "dard", "date", "dauphin", "davantage", "debout", "début", "décembre", "déchirer", "déchets", "décider", "déclarer", "décrire", "décrire", "décrocher", "dédaigner", "défaire", "défaut", "défiler", "défunt", "déjà", "délai", "delphinium", "demain", "demeurer", "démission", "démolir", "dénicher", "dénouer", "dentelle", "départ", "dépenser", "dépister", "dépôt", "déranger", "dériver", "désastre", "descendre", "désert", "désigner", "désirer", "désormais", "dessiner", "destrier", "détacher", "détour", "détresse", "deuil", "deux", "devant", "développer", "devenir", "deviner", "devoir", "diable", "dialogue", "diamant", "dicter", "différer", "diffuser", "digérer", "digne", "diluer", "dimanche", "dinde", "diplôme", "direct", "diriger", "discours", "discuter", "disposer", "dissoudre", "distance", "diviser", "dobson", "doigt", "doive", "domaine", "dompter", "donation", "donjon", "donner", "dorer", "dormir", "dortoir", "dosage", "dose", "douane", "doublé", "douceur", "douille", "douleur", "doute", "doux", "dragée", "dragon", "drap", "dresser", "droit", "drogue", "duper", "durée", "ébène", "éblouir", "éboulement", "écart", "échapper", "éclair", "éclat", "éclore", "écluse", "école", "écoute", "écrit", "écrivain", "écrire", "écrou", "écraser", "écume", "écurie", "éden", "édifice", "éditer", "éducation", "effacer", "effectif", "effort", "égal", "église", "égout", "élan", "élargir", "électeur", "électricité", "élégant", "élève", "éliminer", "élite", "éloge", "élu", "emballer", "embargo", "embouteillage", "embuscade", "émeraude", "émotion", "emparer", "empêcher", "emphase", "empiler", "employer", "empreinte", "emprunter", "enchanté", "enclave", "encoche", "endive", "endormir", "endroit", "enduire", "énergie", "enfant", "enfermer", "enfiler", "enfler", "enfoncer", "enfuir", "engager", "engin", "englober", "enjeu", "enlever", "ennemi", "ennuyeux", "enquêter", "enrichir", "enrouler", "enseigne", "entendre", "entier", "entourer", "entraver", "entre", "envahir", "envelopper", "envie", "envoyer", "épais", "épaule", "épicer", "épier", "épisode", "épitaphe", "époque", "épreuve", "éprouver", "épuiser", "équateur", "équiper", "érable", "érection", "ériger", "érosion", "erreur", "escalade", "escalier", "escargot", "espace", "escrime", "essayer", "essence", "essieu", "essorer", "estime", "estomac", "estrade", "étage", "étaler", "étang", "étape", "éternel", "étincelle", "étiquette", "étirer", "étoile", "étonner", "étouffer", "étourdir", "étrange", "étreindre", "étroit", "étude", "évaluer", "évasion", "éventail", "éviter", "événement", "évidence", "évolution", "évoquer", "exact", "examiner", "excuse", "exemple", "exercer", "exiger", "exil", "existence", "exotique", "expédier", "expliquer", "exposer", "express", "exprimer", "extérieur", "extraire", "exulter", "fabuleux", "facette", "facile", "facteur", "faible", "faim", "faire", "falaise", "falloir", "familier", "fanfare", "farce", "farine", "fasciner", "fatal", "fatigue", "faucon", "faune", "faute", "faveur", "favoriser", "faxer", "fébrile", "féconder", "fée", "félin", "femme", "fendre", "fenêtre", "fermer", "fermier", "ferveur", "fête", "feuille", "feutre", "fiable", "fibre", "ficeler", "fichu", "fidèle", "fier", "figer", "figure", "fil", "filer", "filet", "fille", "film", "filtre", "final", "finesse", "finir", "fiole", "firme", "fissure", "fixe", "flairer", "flamme", "flâner", "flaque", "fleur", "flexion", "flocon", "flore", "flot", "flou", "fluide", "flûte", "flux", "foin", "foire", "foison", "folie", "fonction", "fondre", "fonte", "force", "forêt", "forge", "forgeron", "forme", "formule", "fort", "fortune", "fossé", "foudre", "fouet", "fouiller", "foulard", "foule", "four", "fourmi", "fourrure", "foutre", "fracas", "fraîcheur", "frapper", "fraternité", "fraude", "frayeur", "frégate", "frein", "frémir", "fréquent", "frère", "friable", "friche", "frimer", "fringue", "fripouille", "frire", "frisson", "frivole", "froid", "fromage", "front", "frotter", "fruit", "fugace", "fuite", "fumée", "fureur", "furieux", "fusion", "futé", "futile", "futur", "gagné", "gai", "galerie", "gambader", "gant", "garage", "garde", "gare", "garnir", "gâteau", "gauche", "gaufre", "gaz", "gazon", "géant", "geler", "gémir", "générer", "genou", "genre", "gens", "germe", "geste", "gibier", "gicler", "gifle", "givre", "glace", "glisser", "globe", "gloire", "gluant", "goélette", "golf", "gomme", "gorge", "gorille", "goudron", "goulot", "goutte", "gouverner", "grabuge", "grâce", "grain", "grand", "gras", "gratter", "grave", "grêle", "grenade", "griffe", "griller", "grimper", "gris", "grogner", "gronder", "grotte", "groupe", "grue", "guépard", "guerre", "guetter", "guide", "guider", "guimauve", "guirlande", "guitare", "habile", "habiter", "hache", "haine", "haïr", "halte", "hameau", "hangar", "hanter", "haricot", "harmonie", "hasard", "haut", "hélas", "hélice", "hérisson", "héritage", "herbe", "heure", "hibou", "hilarant", "histoire", "hiver", "homard", "homme", "honneur", "honte", "horde", "horizon", "hormone", "horrible", "houle", "housse", "hublot", "humble", "humide", "humour", "hurler", "idée", "ignorer", "île", "image", "imaginer", "immense", "immobile", "imposer", "impôt", "impression", "inconnu", "inégal", "infime", "infliger", "informer", "inhabituel", "inonder", "inscrire", "insecte", "insister", "instant", "intégrer", "intense", "intervenir", "intime", "intrigue", "inventer", "inviter", "iode", "iris", "ironie", "isolement", "issue", "ivre", "jacinthe", "jade", "jaguar", "jaillir", "jaloux", "jamais", "jambon", "janvier", "jardin", "jauger", "jaune", "javelot", "jazz", "jet", "jeter", "jeu", "jeudi", "jeune", "joie", "joindre", "joli", "jouer", "joueur", "journal", "joue", "journée"])
    
    duel_embed = discord.Embed(title="Duel - Mot le plus rapide", color=discord.Color.blue())
    duel_embed.add_field(name=f"{ctx.author.display_name} VS {opponent.display_name}", value=f"Vous devez écrire le mot suivant le plus rapidement : `{random_word}`")
    
    duel_message = await ctx.send(embed=duel_embed)
    
    def check_message(message):
        return message.author == ctx.author or message.author == opponent
    
    try:
        message = await bot.wait_for("message", timeout=10, check=check_message)
        
        if message.content.lower() == random_word.lower():
            if message.author == ctx.author:
                user_balance += bet * 2
                user_data["balance"] = user_balance
                save_user_money(server_id, user_id, user_data)
                await ctx.send(f"{ctx.author.mention} a gagné le duel et remporte {bet * 2} <a:money:1118983615418728508>.")
                duel_in_progress.pop(user_id)
                duel_in_progress.pop(opponent_id)
            else:
                opponent_balance += bet * 2
                opponent_data["balance"] = opponent_balance
                save_user_money(server_id, opponent_id, opponent_data)
                await ctx.send(f"{opponent.mention} a gagné le duel et remporte {bet * 2} <a:money:1118983615418728508>.")
                duel_in_progress.pop(user_id)
                duel_in_progress.pop(opponent_id)
        else:
            if message.author == ctx.author:
                opponent_balance += bet * 2
                opponent_data["balance"] = opponent_balance
                save_user_money(server_id, opponent_id, opponent_data)
                await ctx.send(f"{opponent.mention} a gagné le duel et remporte {bet * 2} <a:money:1118983615418728508>. {ctx.author.mention} a fait une erreur.")
                duel_in_progress.pop(user_id)
                duel_in_progress.pop(opponent_id)
            else:
                user_balance += bet * 2
                user_data["balance"] = user_balance
                save_user_money(server_id, user_id, user_data)
                await ctx.send(f"{ctx.author.mention} a gagné le duel et remporte {bet * 2} <a:money:1118983615418728508>. {opponent.mention} a fait une erreur.")
                duel_in_progress.pop(user_id)
                duel_in_progress.pop(opponent_id)
    except asyncio.TimeoutError:
        await ctx.send("Aucun joueur n'a écrit de message à temps.")
        opponent_balance += bet 
        user_balance += bet
        user_data["balance"] = user_balance
        opponent_data["balance"] = opponent_balance
        duel_in_progress.pop(user_id)
        duel_in_progress.pop(opponent_id)
        return

            
@duel.command(description="Mini-jeu de rapidité difficile en duo (normalement)")
async def speedy(ctx, opponent: discord.User, bet: int):
    if opponent is None or bet is None:
        embed = discord.Embed(title="Commande : Duel", description="Défie un autre joueur dans un duel speedy.", color=discord.Color.blue())
        embed.add_field(name="Utilisation", value="?duel [opponent] [bet]")
        embed.add_field(name="Description", value="Défie un autre joueur dans un duel speedy. Vous devez spécifier l'adversaire et la mise.")
        await ctx.send(embed=embed)
        return
    
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)
    opponent_id = str(opponent.id)

    if opponent_id == user_id:
        await ctx.send("Vous ne pouvez pas jouer contre vous-même.")
        return
    
    settings_embed = await check_settings(server_id, user_id)
    if settings_embed is not None:
        await ctx.send(embed=settings_embed)
        return
    
    ban_info = check_user_ban_status(server_id, opponent_id)
    if ban_info is not None:
        reason, admin_id = ban_info
        admin = ctx.bot.get_user(admin_id)
        embed = discord.Embed(title="Compte Monétaire suspendu", description="Le compte monétaire de votre adversaire a été suspendu.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    user_data = load_user_money(server_id, user_id)
    opponent_data = load_user_money(server_id, opponent_id)
    
    user_balance = user_data["balance"]
    opponent_balance = opponent_data["balance"]
    
    if bet <= 0:
        await ctx.send("La mise doit être supérieure à zéro.")
        return
    
    if bet > user_balance or bet > opponent_balance:
        await ctx.send("L'un des joueurs n'a pas assez d'argent pour miser cette somme.")
        return
    
    def check_reaction(reaction, user):
        return user == opponent and str(reaction.emoji) == "<a:BlackHD:1112807458507858061>"
    
    duel_message = await ctx.send(f"{opponent.mention}, vous avez été défié par {ctx.author.mention} pour un duel dactylographique. \nMise : **{bet}** <a:money:1118983615418728508>. \nCliquez sur <a:BlackHD:1112807458507858061> pour accepter le duel.")
    
    if user_id in duel_in_progress or opponent_id in duel_in_progress:
        await ctx.send("Un duel est déjà en cours entre ces deux joueurs.")
        return
    
    duel_in_progress[user_id] = True
    duel_in_progress[opponent_id] = True

    await duel_message.add_reaction("<a:BlackHD:1112807458507858061>")

    try:
        reaction, _ = await ctx.bot.wait_for("reaction_add", timeout=60, check=check_reaction)
    except asyncio.TimeoutError:
        await ctx.send(f"{opponent.mention} n'a pas accepté le duel à temps.")
        duel_in_progress.pop(user_id)
        duel_in_progress.pop(opponent_id)
        return
    
    await duel_message.delete()

    user_balance -= bet
    opponent_balance -= bet
    
    user_data["balance"] = user_balance
    opponent_data["balance"] = opponent_balance
    
    save_user_money(server_id, user_id, user_data)
    save_user_money(server_id, opponent_id, opponent_data)
    
    ready_message = await ctx.send("Prêt ?")
    await asyncio.sleep(random.randint(1, 25))
    await ready_message.delete()

    results = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
    
    roulette_message = await ctx.send("Chargement du mini-jeu")
    
    for result in results:
        await roulette_message.add_reaction(result)

    await asyncio.sleep(5)
    await roulette_message.edit(content="Fin du chargement")
    await asyncio.sleep(1)
    
    random_number = random.randint(0, 9)
    result = results[random_number]
    
    await roulette_message.edit(content=f"Sélectionne le nombre {result}, le plus rapidement possible")
        
    try:
        reaction, user = await ctx.bot.wait_for('reaction_add', timeout=10, check=lambda reaction, user: user and str(reaction.emoji) == result)
        
        if user == ctx.author:
            user_balance += bet * 2
            user_data["balance"] = user_balance
            save_user_money(server_id, user_id, user_data)
            await ctx.send(f"{ctx.author.mention} a gagné le duel et remporte {bet * 2} <a:money:1118983615418728508>.")
        else:
            opponent_balance += bet * 2
            opponent_data["balance"] = opponent_balance
            save_user_money(server_id, opponent_id, opponent_data)
            await ctx.send(f"{opponent.mention} a gagné le duel et remporte {bet * 2} <a:money:1118983615418728508>.")
        
    except asyncio.TimeoutError:
        await ctx.send("Aucun joueur n'a réagi à temps.")
        opponent_balance += bet
        user_balance += bet
        save_user_money(server_id, user_id, user_data)
        save_user_money(server_id, opponent_id, opponent_data)
        user_data["balance"] = user_balance
        opponent_data["balance"] = opponent_balance
    
    duel_in_progress.pop(user_id)
    duel_in_progress.pop(opponent_id)

    

@bot.hybrid_group()
async def trio(ctx):
    if ctx.invoked_subcommand is None:
        embed = discord.Embed(title="Commande : Trio", description="Défie deux autres joueurs dans un duel dactylographique ou de question", color=discord.Color.blue())
        embed.add_field(name="Utilisation", value="?trio [dactylo] [opponent1] [opponent2] [bet]")
        await ctx.send(embed=embed)


@trio.command(description="Mini-jeu de rapidité difficile en TRIO(normalement)")
async def dactylo(ctx, opponent1: discord.User, opponent2: discord.User, bet: int):
    if opponent1 is None or opponent2 is None or bet is None:
        embed = discord.Embed(title="Commande : Duel", description="Défie deux autres joueurs dans un duel dactylographique.", color=discord.Color.blue())
        embed.add_field(name="Utilisation", value="?trio dactylo [opponent1] [opponent2] [bet]")
        embed.add_field(name="Description", value="Défie deux autres joueurs dans un duel dactylographique. Vous devez spécifier les adversaires et la mise.")
        await ctx.send(embed=embed)
        return

    if opponent1 == opponent2 or opponent1 == ctx.author or opponent2 == ctx.author:
        await ctx.send("Vous ne pouvez pas jouer contre vous-même ou affronter le même adversaire deux fois.")
        return

    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)
    opponent1_id = str(opponent1.id)
    opponent2_id = str(opponent2.id)

    settings_embed = await check_settings(server_id, user_id)
    if settings_embed is not None:
        await ctx.send(embed=settings_embed)
        return

    ban_info = check_user_ban_status(server_id, opponent1_id)
    if ban_info is not None:
        reason, admin_id = ban_info
        admin = bot.get_user(admin_id)
        embed = discord.Embed(title="Compte Monétaire suspendu", description=f"Votre compte monétaire à été suspendu.\nRaison : {reason}\nSanction appliquée par : {admin.mention}\n Si vous souhaitez contester cette sanction, [Cliquez-ici](https://discord.com/channels/1103936072989278279/1103936074134339639)", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    ban_info = check_user_ban_status(server_id, opponent2_id)
    if ban_info is not None:
        reason, admin_id = ban_info
        admin = bot.get_user(admin_id)
        embed = discord.Embed(title="Compte Monétaire suspendu", description=f"Votre compte monétaire à été suspendu.\nRaison : {reason}\nSanction appliquée par : {admin.mention}\n Si vous souhaitez contester cette sanction, [Cliquez-ici](https://discord.com/channels/1103936072989278279/1103936074134339639)", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    user_data = load_user_money(server_id, user_id)
    opponent1_data = load_user_money(server_id, opponent1_id)
    opponent2_data = load_user_money(server_id, opponent2_id)

    user_balance = user_data["balance"]
    opponent1_balance = opponent1_data["balance"]
    opponent2_balance = opponent2_data["balance"]

    if bet <= 3:
        await ctx.send("La mise doit être supérieure à trois.")
        return

    if bet > user_balance or bet > opponent1_balance or bet > opponent2_balance:
        await ctx.send("L'un des joueurs n'a pas assez d'argent pour miser cette somme.")
        return

    if user_id in duel_in_progress or opponent1_id in duel_in_progress or opponent2_id in duel_in_progress:
        await ctx.send("Un duel est déjà en cours avec l'un des joueurs.")
        return

    duel_in_progress[user_id] = True
    duel_in_progress[opponent1_id] = True
    duel_in_progress[opponent2_id] = True

    duel_message = await ctx.send(f"{opponent1.mention}, {opponent2.mention}, vous avez été défiés par {ctx.author.mention} pour un duel dactylographique. \nMise : **{bet}** <a:money:1118983615418728508>. \nCliquez sur <a:BlackHD:1112807458507858061> pour accepter le duel.")

    def check_reaction(reaction, user):
        return user == opponent1 or user == opponent2 and str(reaction.emoji) == "<a:BlackHD:1112807458507858061>"

    await duel_message.add_reaction("<a:BlackHD:1112807458507858061>")

    try:
        def check_reaction(reaction, user):
            return (user == opponent1 or user == opponent2) and str(reaction.emoji) == "<a:BlackHD:1112807458507858061>"

        await duel_message.add_reaction("<a:BlackHD:1112807458507858061>")
        reactions = []

        while len(reactions) < 2:
            reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check_reaction)
            if user not in reactions:
                reactions.append(user)
    except asyncio.TimeoutError:
        await ctx.send(f"{opponent1.mention} ou {opponent2.mention} n'a pas accepté le duel à temps.")
        duel_in_progress.pop(user_id)
        duel_in_progress.pop(opponent1_id)
        duel_in_progress.pop(opponent2_id)
        return

    await duel_message.delete()

    user_balance -= bet
    opponent1_balance -= bet
    opponent2_balance -= bet

    user_data["balance"] = user_balance
    opponent1_data["balance"] = opponent1_balance
    opponent2_data["balance"] = opponent2_balance

    save_user_money(server_id, user_id, user_data)
    save_user_money(server_id, opponent1_id, opponent1_data)
    save_user_money(server_id, opponent2_id, opponent2_data)

    ready_message = await ctx.send("Prêt ?")
    await asyncio.sleep(random.randint(1, 25))
    await ready_message.delete()

    random_word = random.choice(["chat", "chien", "maison", "jardin", "ordinateur", "banane", "pilote", "tom", "giveaways", "actif", "moulag", "abaissement", "abandon", "abasourdi", "abattement", "abattre", "abeille", "aberrant", "abîme", "abolir", "abondance", "aborder", "aboutir", "aboyer", "abrasif", "abreuver", "abriter", "abroger", "absence", "absolu", "absorber", "abstrait", "absurde", "abusif", "abyssal", "académie", "acajou", "acarien", "accabler", "accepter", "acclamer", "accolade", "accorder", "accrocher", "accuser", "acerbe", "acharné", "achat", "acheter", "acier", "acolyte", "acquis", "acrobate", "acteur", "actif", "action", "actuel", "adage", "adapter", "addition", "adepte", "adieu", "admettre", "admirer", "adolescent", "adoption", "adrénaline", "adulte", "adverbe", "aérer", "aérobie", "aéroport", "aérostat", "affaiblir", "affamé", "affection", "affiche", "affoler", "affranchir", "affronter", "agenda", "agile", "agiter", "agonie", "agrafer", "agréable", "agrume", "aider", "aiguille", "aileron", "aimable", "ajouter", "ajuster", "alarme", "alchimie", "alerte", "algèbre", "algorithme", "alias", "alibi", "aliment", "aliter", "alizé", "alléger", "alléluia", "alliance", "allonger", "allumer", "alors", "alourdir", "alpaga", "altesse", "alvéole", "amateur", "ambigu", "ambre", "ambulance", "améliorer", "aménager", "amertume", "amidon", "amiral", "amorcer", "amour", "ampoule", "amulette", "amusant", "analyse", "ananas", "anarchie", "anatomie", "ancien", "ange", "anglais", "angoisse", "angulaire", "animal", "annexe", "annonce", "annuel", "anodin", "anomalie", "antenne", "antidote", "anxiété", "apaiser", "apéritif", "aplanir", "apologie", "appareil", "appeler", "apporter", "apprendre", "approcher", "approuver", "arbitre", "arbuste", "arche", "ardoise", "argent", "aride", "armature", "armement", "armoire", "aromatiser", "arracher", "arrêter", "arriver", "arroser", "arsenal", "artériel", "article", "aspect", "asphalte", "aspirer", "assaut", "asseoir", "assiette", "associer", "assumer", "assurer", "asticot", "astre", "astuce", "atelier", "atome", "atout", "atroce", "attacher", "attaque", "attente", "attirer", "attraper", "aubaine", "auberge", "audace", "audible", "augmenter", "aurore", "automne", "autre", "avaler", "avancer", "aventure", "avertir", "aveugle", "aviation", "avide", "avion", "aviser", "avoine", "avouer", "avril", "axial", "axiome", "badge", "bafouer", "bagage", "baguette", "baignade", "balancer", "balcon", "balise", "ballon", "bambou", "banane", "banc", "bandage", "banjo", "banlieue", "bannière", "banquier", "barbier", "baril", "baron", "barque", "barrage", "barre", "barrière", "baryum", "basalt", "bascule", "base", "bassin", "batterie", "bavarder", "belette", "bélier", "belote", "bénéfice", "berceau", "berger", "berline", "bermuda", "besace", "besoin", "bétail", "beurre", "biais", "biceps", "bidule", "bière", "bifteck", "bijou", "bilan", "billet", "binôme", "biologie", "biopsie", "bière", "biscuit", "bison", "bitume", "bizarre", "blâmer", "blanc", "blé", "blond", "bloquent", "blouse", "blouson", "bobine", "boire", "boisson", "boîte", "bonbon", "bondir", "bonheur", "bonjour", "bonus", "bordure", "borgne", "borner", "bosse", "bouche", "boucle", "boueux", "bougie", "boulon", "bouquet", "bourgeon", "boussole", "boutique", "boxeur", "brader", "braise", "branche", "bras", "brave", "bravo", "brèche", "brevet", "brider", "brigade", "briller", "brin", "brioche", "brique", "briser", "broche", "broder", "bronze", "brosser", "brouter", "bruit", "brûler", "brume", "brusque", "brutal", "bruyant", "bûche", "budget", "buffet", "bugle", "buisson", "bulletin", "bureau", "burin", "buste", "butin", "buvable", "buvette", "cabane", "cabine", "câble", "cache", "cadeau", "cadre", "café", "cage", "caillou", "caisson", "calcul", "caleçon", "calibre", "calice", "calme", "camarade", "caméra", "camion", "campagne", "canal", "canard", "cancer", "caniche", "canne", "canon", "canot", "cantine", "canular", "capable", "capot", "capturer", "caractère", "carbone", "caresser", "carotte", "carreau", "carte", "casier", "casque", "casserole", "cause", "cavalier", "caverne", "caviar", "ceinture", "cela", "céleste", "cellule", "cendre", "censurer", "cent", "céder", "ceinture", "cercle", "cerise", "cerner", "cerveau", "cesser", "chacal", "chaise", "chaleur", "chambre", "chamois", "champion", "chance", "change", "chanson", "chant", "chaos", "chapeau", "charbon", "chasse", "chat", "chaud", "chaussette", "chauve", "chavirer", "chemin", "chenille", "cheveu", "cheville", "chez", "chiffre", "chimie", "chiot", "chirurgie", "chocolat", "choisir", "chose", "chou", "chut", "ciel", "cigare", "cigare", "cigogne", "cimenter", "cinéma", "cire", "cirque", "ciseau", "citation", "citron", "civique", "clair", "clameur", "clan", "clapet", "classe", "clavier", "client", "cligner", "climat", "cloche", "cloner", "clôture", "clown", "cocon", "coiffe", "coin", "colline", "colon", "colore", "combat", "comédie", "commande", "commencer", "comment", "commercer", "complet", "complot", "comprendre", "compter", "conduire", "confier", "congeler", "congrès", "conique", "connaître", "conquérir", "consoler", "conte", "continuer", "convaincre", "copain", "copie", "corde", "corne", "corps", "corridor", "cosmos", "costume", "coton", "couche", "coude", "couler", "coup", "couple", "cour", "courage", "courbe", "coussin", "couteau", "couvrir", "crabe", "cracher", "craindre", "crainte", "cravate", "crayon", "crème", "créature", "crédit", "créer", "creuser", "crevette", "crible", "crier", "crime", "crinoline", "crise", "crochet", "croire", "croisière", "croquer", "crotte", "croupe", "croyance", "cruche", "crustacé", "cube", "cuisine", "cuivre", "culotte", "cultiver", "cumulus", "curieux", "cycle", "cylindre", "dague", "daigner", "dame", "danger", "danse", "dard", "date", "dauphin", "davantage", "debout", "début", "décembre", "déchirer", "déchets", "décider", "déclarer", "décrire", "décrire", "décrocher", "dédaigner", "défaire", "défaut", "défiler", "défunt", "déjà", "délai", "delphinium", "demain", "demeurer", "démission", "démolir", "dénicher", "dénouer", "dentelle", "départ", "dépenser", "dépister", "dépôt", "déranger", "dériver", "désastre", "descendre", "désert", "désigner", "désirer", "désormais", "dessiner", "destrier", "détacher", "détour", "détresse", "deuil", "deux", "devant", "développer", "devenir", "deviner", "devoir", "diable", "dialogue", "diamant", "dicter", "différer", "diffuser", "digérer", "digne", "diluer", "dimanche", "dinde", "diplôme", "direct", "diriger", "discours", "discuter", "disposer", "dissoudre", "distance", "diviser", "dobson", "doigt", "doive", "domaine", "dompter", "donation", "donjon", "donner", "dorer", "dormir", "dortoir", "dosage", "dose", "douane", "doublé", "douceur", "douille", "douleur", "doute", "doux", "dragée", "dragon", "drap", "dresser", "droit", "drogue", "duper", "durée", "ébène", "éblouir", "éboulement", "écart", "échapper", "éclair", "éclat", "éclore", "écluse", "école", "écoute", "écrit", "écrivain", "écrire", "écrou", "écraser", "écume", "écurie", "éden", "édifice", "éditer", "éducation", "effacer", "effectif", "effort", "égal", "église", "égout", "élan", "élargir", "électeur", "électricité", "élégant", "élève", "éliminer", "élite", "éloge", "élu", "emballer", "embargo", "embouteillage", "embuscade", "émeraude", "émotion", "emparer", "empêcher", "emphase", "empiler", "employer", "empreinte", "emprunter", "enchanté", "enclave", "encoche", "endive", "endormir", "endroit", "enduire", "énergie", "enfant", "enfermer", "enfiler", "enfler", "enfoncer", "enfuir", "engager", "engin", "englober", "enjeu", "enlever", "ennemi", "ennuyeux", "enquêter", "enrichir", "enrouler", "enseigne", "entendre", "entier", "entourer", "entraver", "entre", "envahir", "envelopper", "envie", "envoyer", "épais", "épaule", "épicer", "épier", "épisode", "épitaphe", "époque", "épreuve", "éprouver", "épuiser", "équateur", "équiper", "érable", "érection", "ériger", "érosion", "erreur", "escalade", "escalier", "escargot", "espace", "escrime", "essayer", "essence", "essieu", "essorer", "estime", "estomac", "estrade", "étage", "étaler", "étang", "étape", "éternel", "étincelle", "étiquette", "étirer", "étoile", "étonner", "étouffer", "étourdir", "étrange", "étreindre", "étroit", "étude", "évaluer", "évasion", "éventail", "éviter", "événement", "évidence", "évolution", "évoquer", "exact", "examiner", "excuse", "exemple", "exercer", "exiger", "exil", "existence", "exotique", "expédier", "expliquer", "exposer", "express", "exprimer", "extérieur", "extraire", "exulter", "fabuleux", "facette", "facile", "facteur", "faible", "faim", "faire", "falaise", "falloir", "familier", "fanfare", "farce", "farine", "fasciner", "fatal", "fatigue", "faucon", "faune", "faute", "faveur", "favoriser", "faxer", "fébrile", "féconder", "fée", "félin", "femme", "fendre", "fenêtre", "fermer", "fermier", "ferveur", "fête", "feuille", "feutre", "fiable", "fibre", "ficeler", "fichu", "fidèle", "fier", "figer", "figure", "fil", "filer", "filet", "fille", "film", "filtre", "final", "finesse", "finir", "fiole", "firme", "fissure", "fixe", "flairer", "flamme", "flâner", "flaque", "fleur", "flexion", "flocon", "flore", "flot", "flou", "fluide", "flûte", "flux", "foin", "foire", "foison", "folie", "fonction", "fondre", "fonte", "force", "forêt", "forge", "forgeron", "forme", "formule", "fort", "fortune", "fossé", "foudre", "fouet", "fouiller", "foulard", "foule", "four", "fourmi", "fourrure", "foutre", "fracas", "fraîcheur", "frapper", "fraternité", "fraude", "frayeur", "frégate", "frein", "frémir", "fréquent", "frère", "friable", "friche", "frimer", "fringue", "fripouille", "frire", "frisson", "frivole", "froid", "fromage", "front", "frotter", "fruit", "fugace", "fuite", "fumée", "fureur", "furieux", "fusion", "futé", "futile", "futur", "gagné", "gai", "galerie", "gambader", "gant", "garage", "garde", "gare", "garnir", "gâteau", "gauche", "gaufre", "gaz", "gazon", "géant", "geler", "gémir", "générer", "genou", "genre", "gens", "germe", "geste", "gibier", "gicler", "gifle", "givre", "glace", "glisser", "globe", "gloire", "gluant", "goélette", "golf", "gomme", "gorge", "gorille", "goudron", "goulot", "goutte", "gouverner", "grabuge", "grâce", "grain", "grand", "gras", "gratter", "grave", "grêle", "grenade", "griffe", "griller", "grimper", "gris", "grogner", "gronder", "grotte", "groupe", "grue", "guépard", "guerre", "guetter", "guide", "guider", "guimauve", "guirlande", "guitare", "habile", "habiter", "hache", "haine", "haïr", "halte", "hameau", "hangar", "hanter", "haricot", "harmonie", "hasard", "haut", "hélas", "hélice", "hérisson", "héritage", "herbe", "heure", "hibou", "hilarant", "histoire", "hiver", "homard", "homme", "honneur", "honte", "horde", "horizon", "hormone", "horrible", "houle", "housse", "hublot", "humble", "humide", "humour", "hurler", "idée", "ignorer", "île", "image", "imaginer", "immense", "immobile", "imposer", "impôt", "impression", "inconnu", "inégal", "infime", "infliger", "informer", "inhabituel", "inonder", "inscrire", "insecte", "insister", "instant", "intégrer", "intense", "intervenir", "intime", "intrigue", "inventer", "inviter", "iode", "iris", "ironie", "isolement", "issue", "ivre", "jacinthe", "jade", "jaguar", "jaillir", "jaloux", "jamais", "jambon", "janvier", "jardin", "jauger", "jaune", "javelot", "jazz", "jet", "jeter", "jeu", "jeudi", "jeune", "joie", "joindre", "joli", "jouer", "joueur", "journal", "joue", "journée"])

    duel_embed = discord.Embed(title="Duel - Mot le plus rapide", color=discord.Color.blue())
    duel_embed.add_field(name=f"{ctx.author.display_name} VS {opponent1.display_name} VS {opponent2.display_name}", value=f"Vous devez écrire le mot suivant le plus rapidement : `{random_word}`")

    duel_message = await ctx.send(embed=duel_embed)

    def check_message(message):
        return message.author == ctx.author or message.author == opponent1 or message.author == opponent2

    try:
        message = await bot.wait_for("message", timeout=10, check=check_message)

        if message.content.lower() == random_word.lower():
            if message.author == ctx.author:
                user_balance += bet * 3
                user_data["balance"] = user_balance
                save_user_money(server_id, user_id, user_data)
                await ctx.send(f"{ctx.author.mention} a remporté le duel et gagne {bet * 3} <a:money:1118983615418728508>.")
                duel_in_progress.pop(user_id)
                duel_in_progress.pop(opponent1_id)
                duel_in_progress.pop(opponent2_id)
            elif message.author == opponent1:
                opponent1_balance += bet * 3
                opponent1_data["balance"] = opponent1_balance
                save_user_money(server_id, opponent1_id, opponent1_data)
                await ctx.send(f"{opponent1.mention} a remporté le duel et gagne {bet * 3} <a:money:1118983615418728508>.")
                duel_in_progress.pop(user_id)
                duel_in_progress.pop(opponent1_id)
                duel_in_progress.pop(opponent2_id)
            else:
                opponent2_balance += bet * 3
                opponent2_data["balance"] = opponent2_balance
                save_user_money(server_id, opponent2_id, opponent2_data)
                await ctx.send(f"{opponent2.mention} a remporté le duel et gagne {bet * 3} <a:money:1118983615418728508>.")
                duel_in_progress.pop(user_id)
                duel_in_progress.pop(opponent1_id)
                duel_in_progress.pop(opponent2_id)
        else:
            if message.author == ctx.author:
                opponent1_balance += bet * 1.5
                opponent2_balance += bet * 1.5
                opponent1_data["balance"] = opponent1_balance
                opponent2_data["balance"] = opponent2_balance
                save_user_money(server_id, opponent1_id, opponent1_data)
                save_user_money(server_id, opponent2_id, opponent2_data)
                await ctx.send(f"{opponent1.mention} et {opponent2.mention} ont remporté le duel et gagnent {bet * 1.5} <a:money:1118983615418728508>. {ctx.author.mention} a fait une erreur.")
                duel_in_progress.pop(user_id)
                duel_in_progress.pop(opponent1_id)
                duel_in_progress.pop(opponent2_id)
            elif message.author == opponent1:
                user_balance += bet * 1.5
                opponent2_balance += bet * 1.5
                user_data["balance"] = user_balance
                opponent2_data["balance"] = opponent2_balance
                save_user_money(server_id, user_id, user_data)
                save_user_money(server_id, opponent2_id, opponent2_data)
                await ctx.send(f"{ctx.author.mention} et {opponent2.mention} ont remporté le duel et gagnent {bet * 1.5} <a:money:1118983615418728508>. {opponent1.mention} a fait une erreur.")
                duel_in_progress.pop(user_id)
                duel_in_progress.pop(opponent1_id)
                duel_in_progress.pop(opponent2_id)
            else:
                user_balance += bet * 1.5
                opponent1_balance += bet * 1.5
                user_data["balance"] = user_balance
                opponent1_data["balance"] = opponent1_balance
                save_user_money(server_id, user_id, user_data)
                save_user_money(server_id, opponent1_id, opponent1_data)
                await ctx.send(f"{ctx.author.mention} et {opponent1.mention} ont remporté le duel et gagnent {bet * 1.5} <a:money:1118983615418728508>. {opponent2.mention} a fait une erreur.")
                duel_in_progress.pop(user_id)
                duel_in_progress.pop(opponent1_id)
                duel_in_progress.pop(opponent2_id)
    except asyncio.TimeoutError:
        await ctx.send("Aucun joueur n'a écrit de message à temps.")
        opponent1_balance += bet
        opponent2_balance += bet
        user_balance += bet
        user_data["balance"] = user_balance
        opponent1_data["balance"] = opponent1_balance
        opponent2_data["balance"] = opponent2_balance
        save_user_money(server_id, user_id, user_data)
        save_user_money(server_id, opponent1_id, opponent1_data)
        save_user_money(server_id, opponent2_id, opponent2_data)
        duel_in_progress.pop(user_id)
        duel_in_progress.pop(opponent1_id)
        duel_in_progress.pop(opponent2_id)

        
#####################################################################################################################
#                                                                                                                   #
#                                                                                                                   #
#                                               BOUTIQUE/REWARDS : V1.5                                             #
#                                               PAR PILOTE PRODUCTION                                               #
#                                                                                                                   #
#####################################################################################################################





async def update_payout():
    global payout_value

    while True:
        payout_value += random.uniform(-500, 510)
        payout_value = max(900000, payout_value)

        payout_history.append((datetime.now(), payout_value))

        cutoff_time = datetime.now() - timedelta(hours=1)
        payout_history[:] = [data for data in payout_history if data[0] >= cutoff_time]

        plt.clf()
        times, values = zip(*payout_history)
        plt.plot(times, values, marker='o')
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
        plt.xlabel('Heure')
        plt.ylabel('Prix (€)')
        plt.title('Évolution du Payout')
        min_value = min(values)
        max_value = max(values)
        plt.gca().set_ylim(bottom=min_value - 500, top=max_value + 500)
        plt.gca().yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('payout_graph.png')

        await asyncio.sleep(10)

@bot.group()
async def payout(ctx):
    if ctx.invoked_subcommand is None:
        embed = discord.Embed(title="Payout Boursier", color=discord.Color.blue())
        embed.set_image(url="attachment://payout_graph.png")
        await ctx.send(embed=embed, file=discord.File('payout_graph.png'))
        await ctx.send(f"Payout actuel : {payout_value:.0f} <a:money:1118983615418728508> pour 10€ PayPal")

@bot.command()
@commands.has_permissions(administrator=True)
async def set_payout(ctx, amount: float):
    global payout_value
    payout_value = amount
    payout_history.append((datetime.now(), payout_value))

    await ctx.send(f"Payout mis à jour à {payout_value:.2f} €")
    
@payout.command(name='payout', alias='pay')
async def payout_pay(ctx):
    server_id = ctx.guild.id
    user_id = ctx.author.id

    user_money = load_user_money(server_id, user_id)
    user_balance = user_money.get("balance", 0)

    settings_embed = await check_settings(server_id, user_id)
    if settings_embed is not None:
        await ctx.send(embed=settings_embed)
        return

    if payout_value >= user_balance:
        await ctx.send("Désolé, Vous n'avez pas assez pour payout.")
        return
    
    loans = load_user_loans(server_id, user_id)
    if loans:
        await ctx.send("Vous avez un prêt en cours. Vous ne pouvez pas effectuer cette commande.")
        return

    user_balance -= payout_value 
    user_money["balance"] = user_balance
    save_user_money(server_id, user_id, user_money)

    await ctx.send("Achat validé !")
    
    
    order_number = generate_order_number()
    orders = load_orders()
    orders.append({
        "number": order_number,
        "item": "10€ Payout",
        "status": "traitement",
        "user_id": str(ctx.author.id),
        "server_id": str(ctx.guild.id)
    })
    save_orders(orders)
    embed = discord.Embed(title="Bon de commande", description="Votre achat a été effectué avec succès.")
    embed.add_field(name="Numéro de commande", value=order_number, inline=False)
    embed.add_field(name="Article", value="10€ Payout", inline=False)
    embed.add_field(name="Statut", value="Validée", inline=False)
    embed.add_field(name="Comment réclamez votre commande ?", value="Vous pouvez réclamer votre commande via la commande `?order claim (Numéro de commande)` ou par ticket !\n Information : En raison de vacances, les commandes sont validés manuellement, merci de faire un ticket pour toutes les commandes.", inline=False)

    await ctx.send(embed=embed)


def load_shop_items():
    try:
        with open("shop_items.json", "r") as file:
            return json.load(file)
    except FileNotFoundError: 
        return []

def save_shop_items(items):
    with open("shop_items.json", "w") as file:
        json.dump(items, file, indent=4)

def load_orders():
    try:
        with open("orders.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_orders(orders):
    with open("orders.json", "w") as file:
        json.dump(orders, file)

def generate_order_number():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=12))



@bot.group(name='boutique', description="Affiche tous les produits disponibles dans la boutique.", invoke_without_command=True)
async def boutique(ctx):
    embed = discord.Embed(title="Boutique", description="Utilisez `/boutique buy <nom_du_produit>` pour acheter un produit.")
    embed.add_field(name="Bouclier temporaire de 24 heures", value="Prix : 25000 pièces\nCommande : `/boutique buy shield_24`", inline=False)
    embed.add_field(name="Bouclier temporaire de 72 heures", value="Prix : 60000 pièces\nCommande : `/boutique buy shield_72`", inline=False)
    await ctx.send(embed=embed)

@boutique.command(name='buy', description="Achetez un produit dans la boutique.")
async def buy(ctx, product_name: str):
    user_id = str(ctx.author.id)
    server_id = str(ctx.guild.id)
    user_data_balance = load_user_money(server_id, user_id)

    if product_name.lower() == "shield_24":
        price = 25000
        if user_data_balance["balance"] >= price:
            user_data_balance["balance"] -= price
            save_user_money(server_id, user_id, user_data_balance)
            await add_protection(ctx, ctx.author, 24 * 3600)
        else:
            await ctx.send("Vous n'avez pas assez de pièces pour acheter ce produit.")
    elif product_name.lower() == "shield_72":
        price = 60000
        if user_data_balance["balance"] >= price:
            user_data_balance["balance"] -= price
            save_user_money(server_id, user_id, user_data_balance)
            await add_protection(ctx, ctx.author, 72 * 3600)
        else:
            await ctx.send("Vous n'avez pas assez de pièces pour acheter ce produit.")
    else:
        await ctx.send("Produit non disponible.")

async def add_protection(ctx, target: discord.Member, time: int):
    if isinstance(target, discord.Member):
        cooldowns[target.id] = datetime.now() + timedelta(seconds=time)
        embed = discord.Embed(
            title="Protection ajoutée",
            description=f"{target.mention} a maintenant une protection supplémentaire de {time // 3600} heures.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        
@bot.command()
@commands.has_permissions(administrator=True)
async def createitem(ctx, name, price, level, *, description):
    if ctx.guild.id != 1103936072989278279:
        await ctx.send("La commande n'est pas disponible sur les autres serveurs")
        return
    items = load_shop_items()
    for item in items:
        if item["name"].lower() == name.lower():
            await ctx.send("Cet article existe déjà dans la boutique.")
            return
    new_item = {
        "name": name,
        "price": int(price),
        "level": int(level),
        "description": description
    }
    items.append(new_item)
    save_shop_items(items)
    await ctx.send(f"L'article {name} a été ajouté à la boutique avec succès.")

@bot.hybrid_command(description="Affiche les récompenses du serveur, en pièce")
async def rewards(ctx):
    if ctx.guild.id != 1103936072989278279:
        await ctx.send("La commande n'est pas disponible sur les autres serveurs")
        return
    items = load_shop_items()
    embed = discord.Embed(title="Boutique", description="Voici les articles disponibles à l'achat :")
    for item in items:
        embed.add_field(name=item["name"], value=f"Prix : {item['price']} <a:money:1118983615418728508>\nDescription : {item['description']}\nNiveau requis :{item['level']}\nCommande : ?buy {item['name']}", inline=False)
    await ctx.send(embed=embed)

@bot.hybrid_command(description="Achète un article du /rewards")
async def buy(ctx, name):
    user_id =  ctx.author.id
    server_id = ctx.guild.id
    if ctx.guild.id != 1103936072989278279:
        await ctx.send("La commande n'est pas disponible sur les autres serveurs")
        return

    settings_embed = await check_settings(server_id, user_id)
    if settings_embed is not None:
        await ctx.send(embed=settings_embed)
        return
    
    loans = load_user_loans(server_id, user_id)
    
    if loans:
        await ctx.send("Vous avez un prêt en cours. Vous ne pouvez pas effectuer cette commande.")
        return
    
    items = load_shop_items()
    for item in items:
        if item["name"].lower() == name.lower():
            user_data = load_user_money(str(ctx.guild.id), str(ctx.author.id))
            member = ctx.author
            level_data = get_user_level(ctx.guild.id, member.id)
            balance = int(user_data["balance"])
            price = int(item["price"])
            level = item["level"]
            level_user = int(level_data["level"])

            if level_user < level:
                await ctx.send("Vous n'avez pas le niveau requis pour effectuer cet achat.")
                return
            
            if balance >= price:
                order_number = generate_order_number()
                orders = load_orders()
                orders.append({
                    "number": order_number,
                    "item": item["name"],
                    "status": "valide",
                    "user_id": str(ctx.author.id),
                    "server_id": str(ctx.guild.id)
                })
                save_orders(orders)
                user_data["balance"] -= price
                save_user_money(str(ctx.guild.id), str(ctx.author.id), user_data)
                embed = discord.Embed(title="Bon de commande", description="Votre achat a été effectué avec succès.")
                embed.add_field(name="Numéro de commande", value=order_number, inline=False)
                embed.add_field(name="Article", value=item["name"], inline=False)
                embed.add_field(name="Statut", value="En cours de traitement", inline=False)
                embed.add_field(name="Comment réclamez votre commande ?", value="Vous pouvez réclamer votre commande via la commande `/order claim (Numéro de commande)` ou par ticket !", inline=False)

                await ctx.send(embed=embed)
                return
            else:
                await ctx.send("Vous n'avez pas assez de <a:money:1118983615418728508> pour effectuer cet achat.")
                return
    await ctx.send("Aucun article correspondant trouvé dans la boutique.")

@bot.hybrid_group()
async def order(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Commande invalide. Veuillez spécifier une sous-commande verify ou claim.")

@order.group(name="verify", description="Vérifie ta commande")
async def verifycommand(ctx, command_number):
    orders = load_orders()
    for order in orders:
        if order["number"] == command_number:
            embed = discord.Embed(title="Détails de la commande", color=discord.Color.blue())
            embed.add_field(name="Numéro", value=order["number"], inline=False)
            embed.add_field(name="Article", value=order["item"], inline=False)
            embed.add_field(name="Statut", value=order["status"], inline=False)
            embed.add_field(name="ID Utilisateur", value=order["user_id"], inline=False)
            embed.add_field(name="ID Serveur", value=order["server_id"], inline=False)
            await ctx.send(embed=embed)
            return
    await ctx.send("Commande introuvable.")

@order.command(name="claim", description="Claim ta commande, valable uniquement sur une sélection d'article")
async def claimorder(ctx, order_number):
    user_id = ctx.author.id
    server_id = ctx.guild.id
    if ctx.guild.id != 1103936072989278279:
        await ctx.send("La commande n'est pas disponible sur les autres serveurs")
        return

    settings_embed = await check_settings(server_id, user_id)
    if settings_embed is not None:
        await ctx.send(embed=settings_embed)
        return
    orders = load_orders()
    for order in orders:
        if order["number"] == order_number and order["status"] == "valide" and order["server_id"] == str(ctx.guild.id) and order["user_id"] == str(ctx.author.id):
            item_name = order["item"].lower()
            if item_name == "discord_nitro":
                await ctx.send("Cet article n'est pas disponible au claim automatique. Merci de faire un ticket pour récupérer votre commande.")
            elif item_name == "gamble_boost_chance":
                role = discord.utils.get(ctx.guild.roles, id=1127529310564122685)
                await ctx.author.add_roles(role)
                embed = discord.Embed(title="Action effectuée !", description="Le boost a bien été réclamé et sera actif durant les 24 heures à venir !", color=discord.Color.blue())
                await ctx.send(embed=embed)
                order["status"] = "utilisé"
                save_orders(orders)
                await ctx.send("Commande réclamée avec succès.")
                return
            elif item_name == "bouclier_antivol_24h":
                time = 86400
                cooldowns[user_id] = datetime.now() + timedelta(seconds=time)
                embed = discord.Embed(
                    title="Protection ajoutée",
                    description=f"{ctx.user.mention} a maintenant une protection supplémentaire de {time} secondes.",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
                order["status"] = "utilisé"
                save_orders(orders)
                await ctx.send("Commande réclamée avec succès.")
                return
            elif item_name == "bypass_cooldown":
                cooldowns_user[user_id] = datetime.now()
                embed = discord.Embed(
                    title="Cooldowns retiré",
                    description=f"{ctx.user.mention} a maintenant une cooldowns reset.",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
                order["status"] = "utilisé"
                save_orders(orders)
                await ctx.send("Commande réclamée avec succès.")
                return
            else:
                await ctx.send("Cette commande a déjà été réclamée ou n'est pas réclamable via cette commande!")
                return
    await ctx.send("Cette commande a déjà été réclamée ou n'est pas réclamable via cette commande!")

@order.command(name="status", description="Admin : Change le status d'une commande")
@commands.has_permissions(administrator=True)
async def statuschange(ctx, order_number, change):
    user_id = ctx.author.id
    if ctx.guild.id != 1103936072989278279:
        await ctx.send("La commande n'est pas disponible sur les autres serveurs")
        return
    orders = load_orders()
    for order in orders:
        if order["number"] == order_number:
            order["status"] = f"{change}"
            save_orders(orders)
            await ctx.send(f"La status de cette commande à bien été changé par {change} !")
            return
            


#####################################################################################################################
#                                                                                                                   #
#                                                                                                                   #
#                                                  LEVELS : V2.8                                                    #
#                                               PAR PILOTE PRODUCTION                                               #
#                                                                                                                   #
#####################################################################################################################

def get_level_path(server_id: int, user_id: int):
    return f"server/levels_{server_id}/{user_id}.json"


def ensure_level_file(server_id, user_id):
    directory = f"server/levels_{server_id}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    path = f"{directory}/{user_id}.json"
    if not os.path.exists(path):
        with open(path, "w") as f:
            data = {"level": 0, "xp": 0}
            json.dump(data, f)

def get_user_level(server_id, user_id):
    ensure_level_file(server_id, user_id)

    path = f"server/levels_{server_id}/{user_id}.json"
    with open(path, "r") as f:
        data = json.load(f)

    return data

def get_user_level(server_id: int, user_id: int):
    ensure_level_file(server_id, user_id)
    with open(get_level_path(server_id, user_id), "r") as f:
        return json.load(f)

def save_user_level(server_id: int, user_id: int, level_data):
    with open(get_level_path(server_id, user_id), "w") as f:
        json.dump(level_data, f)

def xp_for_level(level: int):
    return 100 * (1.20 ** level)

@bot.hybrid_command(description="Change les données sur le niveau d'un utilisateur")
@commands.has_permissions(administrator=True)
async def setlevels(ctx, subcommand=None, member: discord.Member=None, value=None):
    if subcommand is None:
        embed = discord.Embed(title="Sous-commandes disponibles pour ?setlevels", color=0x00ff00)
        embed.add_field(name="?setlevels setlevel (MEMBRE) (VALEUR)", value="Définir le niveau d'un membre", inline=False)
        embed.add_field(name="?setlevels setxp (MEMBRE) (VALEUR)", value="Définir l'XP d'un membre", inline=False)
        embed.add_field(name="?setlevels addlevel (MEMBRE) (VALEUR)", value="Ajouter des niveaux à un membre", inline=False)
        embed.add_field(name="?setlevels addxp (MEMBRE) (VALEUR)", value="Ajouter de l'XP à un membre", inline=False)
        embed.add_field(name="?setlevels removexp (MEMBRE) (VALEUR)", value="Retirer de l'XP à un membre", inline=False)
        embed.add_field(name="?setlevels removelevel (MEMBRE) (VALEUR)", value="Retirer des niveaux à un membre", inline=False)
        embed.add_field(name="?setlevels resetall", value="Remettre à 0 les niveaux et XP de tous les membres du serveur", inline=False)
        await ctx.send(embed=embed)
        return

    if subcommand == 'setlevel':
        if member is None or value is None:
            await ctx.send("Utilisation : ?setlevels setlevel (MEMBRE) (VALEUR)")
            return
        level_data = get_user_level(ctx.guild.id, member.id)
        level_data['level'] = int(value)
        save_user_level(ctx.guild.id, member.id, level_data)
        await ctx.send(f"niveau de {member.mention} a été défini à {value}.")
    elif subcommand == 'setxp':
        if member is None or value is None:
            await ctx.send("Utilisation : ?setlevels setxp (MEMBRE) (VALEUR)")
            return
        level_data = get_user_level(ctx.guild.id, member.id)
        level_data['xp'] = int(value)
        save_user_level(ctx.guild.id, member.id, level_data)
        await ctx.send(f"XP de {member.mention} a été défini à {value}.")
    elif subcommand == 'addlevel':
        if member is None or value is None:
            await ctx.send("Utilisation : ?setlevels addlevel (MEMBRE) (VALEUR)")
            return
        level_data = get_user_level(ctx.guild.id, member.id)
        level_data['level'] += int(value)
        save_user_level(ctx.guild.id, member.id, level_data)
        await ctx.send(f"{value} niveaux ont été ajoutés à {member.mention}.")
    elif subcommand == 'addxp':
        if member is None or value is None:
            await ctx.send("Utilisation : ?setlevels addxp (MEMBRE) (VALEUR)")
            return
        level_data = get_user_level(ctx.guild.id, member.id)
        level_data["xp"] += int(value)
        xp_for_next_level = xp_for_level(level_data["level"])
        if level_data["xp"] >= xp_for_next_level:
            level_data["level"] += 1
            level_data["xp"] -= xp_for_next_level
            await ctx.send(f"Félicitations {member.mention}, vous avez atteint le niveau {level_data['level']} ! 🎉🎉🎉")
        save_user_level(ctx.guild.id, member.id, level_data)
        await ctx.send(f"XP de {member.mention} a été augmenté de {value} !")
    elif subcommand == 'removexp':
        if member is None or value is None:
            await ctx.send("Utilisation : ?setlevels removexp (MEMBRE) (VALEUR)")
            return
        level_data = get_user_level(ctx.guild.id, member.id)
        level_data["xp"] = max(level_data["xp"] - int(value), 0)
        save_user_level(ctx.guild.id, member.id, level_data)
        await ctx.send(f"XP retirée : {value} pour {member.mention}")
    elif subcommand == 'removelevel':
        if member is None or value is None:
            await ctx.send("Utilisation : ?setlevels removelevel (MEMBRE) (VALEUR)")
            return
        level_data = get_user_level(ctx.guild.id, member.id)
        level_data["level"] = max(level_data["level"] - int(value), 0)
        save_user_level(ctx.guild.id, member.id, level_data)
        await ctx.send(f"Niveau retiré : {value} pour {member.mention}")
    elif subcommand == 'resetall':
        await ctx.send("Êtes-vous sûr de vouloir réinitialiser tous les niveaux et l'XP sur ce serveur ? Répondez avec 'oui' pour confirmer.")
        try:
            confirmation = await bot.wait_for('message', timeout=30.0, check=lambda message: message.author == ctx.author and message.content.lower() == 'oui')
        except asyncio.TimeoutError:
            await ctx.send("Opération annulée.")
            return

        for member in ctx.guild.members:
            level_data = {"level": 1, "xp": 0}
            save_user_level(ctx.guild.id, member.id, level_data)
        await ctx.send("Tous les niveaux et l'XP ont été réinitialisés sur ce serveur.")

@bot.hybrid_command(description="Affiche le niveau actuel")
async def levels(ctx, member: discord.Member = None):
    member = member or ctx.author
    level_data = get_user_level(ctx.guild.id, member.id)
    xp = int(level_data["xp"])
    level = int(level_data["level"])
    xp_for_next_level = int(xp_for_level(level))
    progress = xp / xp_for_next_level * 100
    embed = discord.Embed(title=f"Niveau de {member.name}", color=0x00ff00)
    embed.add_field(name="XP", value=f"{xp}/{xp_for_next_level}", inline=True)
    embed.add_field(name="Niveau", value=f"{level}", inline=True)
    embed.add_field(name="Progression", value=f"{progress:.2f}%", inline=True)
    await ctx.send(embed=embed)

@bot.group(description="Affiche différents classements.")
async def leaderboard(ctx):
    if ctx.invoked_subcommand is None:
        embed = discord.Embed(title="Aide pour les classements", description="Voici la liste des classements disponibles :", color=discord.Color.blue())
        embed.add_field(name="Classement de richesse", value="/leaderboard money", inline=False)
        embed.add_field(name="Classement de niveau", value="/leaderboard level", inline=False)
        embed.add_field(name="Classement des streaks quotidiens", value="/leaderboard daily", inline=False)
        embed.add_field(name="Classement des pièces rouges", value="/leaderboard redmoney", inline=False)
        embed.add_field(name="Classement des mineurs", value="/leaderboard mineurs", inline=False)
        await ctx.send(embed=embed)

@leaderboard.command(name='levels', description="Affiche le classement des niveaux des membres du serveur.")
async def leaderboard_levels(ctx):
    users = []
    for file in os.listdir(f"server/levels_{ctx.guild.id}/"):
        with open(f"server/levels_{ctx.guild.id}/{file}") as f:
            data = json.load(f)
            users.append((data["level"], int(file.split(".")[0])))
    users.sort(reverse=True)
    if len(users) > 10:
        users = users[:10]
    embed = discord.Embed(title="Classement des niveaux", color=0x00ff00)
    for i, (level, user_id) in enumerate(users):
        user = ctx.guild.get_member(user_id)
        if user is not None:
            embed.add_field(name=f"{i+1}. {user.name}", value=f"Niveau {level}", inline=False)
    await ctx.send(embed=embed)

@leaderboard.command(name='bank', description="Affiche le classement des banques des membres du serveur.")
async def leaderboard_bank(ctx):
    server_id = str(ctx.guild.id)
    user_data_list = []

    for folder_name in os.listdir(f"data/bank/{server_id}"):
        if folder_name.endswith(".json"):
            user_id = folder_name.replace(".json", "")
            user_data = load_user_bank(server_id, user_id)
            user_data_money = load_user_money(server_id, user_id)
            user_data_list.append((user_id, user_data_money["balance"], user_data["level"]))

    user_data_list.sort(key=lambda x: (x[2], x[1]), reverse=True)

    embed = discord.Embed(
        title="Top 10 des Banques",
        color=discord.Color.green()
    )
    top_message = ""
    for index, (user_id, balance, level) in enumerate(user_data_list[:10], start=1):
        user = await bot.fetch_user(int(user_id))
        if user:
            top_message += f"{index}. {user.mention} - Niveau {level}, Balance: {balance}\n"
        else:
            top_message += f"{index}. Utilisateur inconnu (ID: {user_id}) - Niveau {level}, Balance: {balance}\n"

    embed.description = top_message
    await ctx.send(embed=embed)

@leaderboard.command(name='balance', description="Affiche le classement des personnes les plus riches du serveur.")
async def leaderboard_balance(ctx):
    server_id = str(ctx.guild.id)
    user_id = ctx.author.id

    settings_embed = await check_settings(server_id, user_id)
    if settings_embed is not None:
        await ctx.send(embed=settings_embed)
        return

    users_data = []

    total_server = 0

    for member in ctx.guild.members:
        user_id = str(member.id)
        user_data = load_user_money(server_id, user_id)
        users_data.append({"user_id": user_id, "balance": user_data["balance"]})

        total_server += user_data["balance"]

    sorted_users = sorted(users_data, key=lambda x: x["balance"], reverse=True)

    total_argent_server = total_server * 0.00001

    embed = discord.Embed(title="Classement des personnes les plus riches", color=discord.Color.gold())
    embed.add_field(name="Richesse totale du serveur", value=f"{total_server} <a:money:1118983615418728508> - {total_argent_server} €", inline=False)
    for i, user_data in enumerate(sorted_users[:10]):
        user = ctx.guild.get_member(int(user_data["user_id"]))
        if user is not None:
            username = user.name
        else:
            username = f"Utilisateur inconnu ({user_data['user_id']})"
        balance = user_data["balance"]
        banned_info = check_user_ban_status(server_id, user_data["user_id"])
        loans = load_user_loans(server_id, user_data["user_id"])
        if banned_info is not None:
            reason, admin_id = banned_info
            admin = bot.get_user(admin_id)
            balance_note = f"<a:error:1112807444633092218> {balance} <a:money:1118983615418728508> (compte monétaire désactivé)\nJoueur banni par : {admin.mention}\nRaison : {reason}"
        elif loans:
            balance_note = f"{balance} <a:money:1118983615418728508> (Prêt en cours)"
        else:
            balance_note = f"{balance} <a:money:1118983615418728508>"

        embed.add_field(name=f"#{i+1} - {username}", value=f"Balance: {balance_note}", inline=False)
    await ctx.send(embed=embed)

@leaderboard.command(name='redmoney', description="Affiche le classement des personnes les plus riches du serveur.")
async def leaderboard_money_red(ctx):
    server_id = str(ctx.guild.id)
    user_id = ctx.author.id

    settings_embed = await check_settings(server_id, user_id)
    if settings_embed is not None:
        await ctx.send(embed=settings_embed)
        return

    users_data = []

    for member in ctx.guild.members:
        user_id = str(member.id)
        user_data = load_user_earning_money(server_id, user_id)
        users_data.append({"user_id": user_id, "balance": user_data["balance"]})

    sorted_users = sorted(users_data, key=lambda x: x["balance"], reverse=True)


    embed = discord.Embed(title="Classement des personnes les plus riches avec la monnaie des mineurs", color=discord.Color.gold())
    for i, user_data in enumerate(sorted_users[:10]):
        user = ctx.guild.get_member(int(user_data["user_id"]))
        if user is not None:
            username = user.name
        else:
            username = f"Utilisateur inconnu ({user_data['user_id']})"
        balance = user_data["balance"]
        banned_info = check_user_ban_status(server_id, user_data["user_id"])
        loans = load_user_loans(server_id, user_data["user_id"])
        if banned_info is not None:
            reason, admin_id = banned_info
            admin = bot.get_user(admin_id)
            balance_note = f"<a:error:1112807444633092218> {balance} pièces rouges (compte monétaire désactivé)\nJoueur banni par : {admin.mention}\nRaison : {reason}"
        elif loans:
            balance_note = f"{balance} pièces rouges (Prêt en cours)"
        else:
            balance_note = f"{balance} pièces rouges"

        embed.add_field(name=f"#{i+1} - {username}", value=f"Balance: {balance_note}", inline=False)

    await ctx.send(embed=embed)

@leaderboard.command(name='daily', description="Affiche le classement des personnes qui ont le plus de jour /daily claim.")
async def daily_top(ctx):
    server_id = str(ctx.guild.id)
    users_data = {}

    if ctx.guild.id != 1103936072989278279:
        await ctx.send("La commande n'est pas disponible sur les autres serveurs")
        return
    
    for member in ctx.guild.members:
        if not member.bot:
            user_id = str(member.id)
            user_data = load_user_data_daily(user_id)
            users_data[member.name] = user_data.get("daily_streak", 0)

    sorted_users = sorted(users_data.items(), key=lambda x: x[1], reverse=True)[:10]
    
    embed = discord.Embed(title="Classement des meilleurs streaks quotidiens", color=discord.Color.blue())
    for rank, (user_name, streak) in enumerate(sorted_users, start=1):
        embed.add_field(name=f"{rank}. {user_name}", value=f"Streak quotidien : {streak}", inline=False)

    await ctx.send(embed=embed)

@leaderboard.command(name='mineurs', description="Classement des mineurs")
async def leaderboard_mineurs(ctx):
    server_id = str(ctx.guild.id)
    user_stats = {}
    
    minerals = [
        "stone", "andesite", "coal", "iron", "platinium", "gold", "titanium",
        "palladium", "ruby", "emerald", "diamond", "uranium", "radium", "pilodium"
    ]
    
    for user_file in os.listdir(f"data/mineurs/{server_id}"):
        if user_file.endswith('.json'):
            user_id = user_file[:-5]
            user_data = load_user_earning(server_id, user_id)
            
            total_mineurs = sum(user_data.get(f"{mineral}_level", 0) for mineral in minerals)
            total_minerais = sum(user_data.get(f"{mineral}_ore", 0) for mineral in minerals)
            
            user_stats[user_id] = {
                "total_mineurs": total_mineurs,
                "total_minerais": total_minerais,
            }
    
    sorted_by_mineurs = sorted(user_stats.items(), key=lambda x: x[1]["total_mineurs"], reverse=True)
    sorted_by_minerais = sorted(user_stats.items(), key=lambda x: x[1]["total_minerais"], reverse=True)
    
    embed = discord.Embed(title="Classement des mineurs et minerais", color=discord.Color.blue())
    
    embed.add_field(name="Top 10 des mineurs", value="\u200b", inline=False)
    for i, (user_id, stats) in enumerate(sorted_by_mineurs[:10], start=1):
        user = await bot.fetch_user(user_id)
        embed.add_field(name=f"{i}. {user.name}", value=f"{stats['total_mineurs']} mineurs", inline=False)
    
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    
    embed.add_field(name="Top 10 des minerais", value="\u200b", inline=False)
    for i, (user_id, stats) in enumerate(sorted_by_minerais[:10], start=1):
        user = await bot.fetch_user(user_id)
        embed.add_field(name=f"{i}. {user.name}", value=f"{stats['total_minerais']} minerais", inline=False)
    
    await ctx.send(embed=embed)

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    if before.channel is None and after.channel is not None:
        level_data = get_user_level(member.guild.id, member.id)
        level_data["xp"] += 5
        xp_for_next_level = xp_for_level(level_data["level"])
        if level_data["xp"] >= xp_for_next_level:
            level_data["level"] += 1
            level_data["xp"] -= xp_for_next_level
            await member.guild.text_channels[0].send(f"Félicitations {member.mention}, vous avez atteint le niveau {level_data['level']} ! 🎉🎉🎉")
        save_user_level(member.guild.id, member.id, level_data)
    elif before.channel is not None and after.channel is None:
        pass
    else:
        pass


#####################################################################################################################
#                                                                                                                   #
#                                                                                                                   #
#                                                  MODÉRATION : V5.2                                                #
#                                               PAR PILOTE PRODUCTION                                               #
#                                                                                                                   #
#####################################################################################################################


color_mapping = {
    "red": 0xFF0000,
    "green": 0x00FF00,
    "blue": 0x0000FF,
    "yellow": 0xFFFF00,
    "orange": 0xFFA500,
    "purple": 0x800080,
    "pink": 0xFFC0CB,
    "teal": 0x008080,
    "silver": 0xC0C0C0,
    "gold": 0xFFD700
}

messages_to_send = {}
    
@bot.command()
async def ask(ctx, couleur: str, titre: str, *, description: str):
    couleur_hex = color_mapping.get(couleur.lower())
    if couleur_hex is None:
        await ctx.send(f"Couleur invalide. Les couleurs disponibles sont : {', '.join(color_mapping.keys())}")
        return
    await ctx.message.delete()
    if ctx.author.id != 97285029289275392:
        await ctx.send("Vous n'êtes pas autorisé à utiliser cette commande.")
        return

    titre_modifie = titre.replace("_", " ")

    embed = discord.Embed(title=titre_modifie, description=description, color=couleur_hex)
    await ctx.send(embed=embed)
    
    
@bot.command()
async def asklater(ctx, couleur: str, titre: str, *, description: str):
    couleur_hex = color_mapping.get(couleur.lower())
    if couleur_hex is None:
        await ctx.send(f"Couleur invalide. Les couleurs disponibles sont : {', '.join(color_mapping.keys())}")
        return

    if ctx.author.id != 97285029289275392:
        await ctx.send("Vous n'êtes pas autorisé à utiliser cette commande.")
        return
    titre_modifie = titre.replace("_", " ")
    message_info = {
        "color": couleur_hex,
        "title": titre_modifie,
        "description": description
    }
    messages_to_send[ctx.message.id] = message_info
    await ctx.message.delete()
    
@bot.command()
async def askall(ctx):
    if ctx.author.id != 97285029289275392:
        await ctx.send("Vous n'êtes pas autorisé à utiliser cette commande.")
        return
    await ctx.message.delete()
    for message_id, message_info in messages_to_send.items():
        try:
            couleur_hex = message_info["color"]
            titre_modifie = message_info["title"]
            description = message_info["description"]
            embed = discord.Embed(title=titre_modifie, description=description, color=couleur_hex)
            await ctx.send(embed=embed)
        except discord.NotFound:
            continue
            
    messages_to_send.clear()


ajust_to_send = []

@bot.hybrid_group(invoke_without_command=True)
async def ajust(ctx):
    pass

@ajust.command(name='add')
async def add(ctx, user: discord.User, amount: int, *, reason=None):
    if ctx.author.id != 97285029289275392 or ctx.author.id != 1011383630251180122:
        await ctx.send("Suce ma bite !")
        await asyncio.sleep(30)
        await ctx.send("Vous n'avez pas les permissions pour executé cette commande")
        return

    await adjust_balance(ctx, user, amount, reason, "gagné")

@ajust.command(name='remove')
async def remove(ctx, user: discord.User, amount: int, *, reason=None):
    if ctx.author.id != 97285029289275392 or ctx.author.id != 1011383630251180122:
        return

    await adjust_balance(ctx, user, -amount, reason, "perdu")



@bot.command()
async def ajustlater(ctx, action, user: discord.User, amount: int, *, reason=None):
    if ctx.author.id != 97285029289275392:
        await ctx.send("Vous n'êtes pas autorisé à utiliser cette commande.")
        return

    if action not in ['add', 'remove']:
        await ctx.send("Action invalide. Utilisez `add` ou `remove`.")
        return
    
    # Inverser le montant pour l'action 'remove'
    if action == 'remove':
        amount = -abs(amount)
    
    user_id = user.id
    ajust_to_send.append({
        "action": action,
        "user_id": user_id,
        "amount": amount,
        "reason": reason
    })
    await ctx.message.delete()
    

@bot.command()
async def ajustall(ctx):
    if ctx.author.id != 97285029289275392:
        await ctx.send("Vous n'êtes pas autorisé à utiliser cette commande.")
        return
    
    await ctx.message.delete()
    for adjustment in ajust_to_send:
        try:
            user = await bot.fetch_user(adjustment["user_id"])
            await adjust_balance(ctx, user, adjustment["amount"], adjustment["reason"])
        except discord.NotFound:
            continue
    
    ajust_to_send.clear()

async def adjust_balance(ctx, user, amount, reason):
    server_id = str(ctx.guild.id)
    target_id = str(user.id)

    user_money = load_user_money(server_id, target_id)
    user_balance = user_money.get("balance", 0)

    user_balance += amount

    if user_balance < 0:
        await create_loan(ctx, user, -user_balance)
        user_balance = 0

    user_money["balance"] = user_balance
    save_user_money(server_id, target_id, user_money)

    status = "gagné" if amount >= 0 else "perdu"
    color = discord.Color.green() if amount >= 0 else discord.Color.red()
    description = f"Votre solde a été ajusté et vous avez {status} {abs(amount)} <a:money:1118983615418728508> - <@{target_id}>"
    reason_text = f"\nRaison : `{reason}`" if reason else "\nRaison : `Aucune`"
    support_link = "\n\nSi vous pensez qu'une erreur a été commise, veuillez contacter le support [ici](https://discord.com/channels/1103936072989278279/1103936074134339639/1116468608806166559)."
    
    embed = discord.Embed(
        title="Ajustement de solde", 
        description=description + reason_text + support_link, 
        color=color
    )
    await ctx.send(embed=embed)

async def create_loan(ctx, user, amount):
    server_id = str(ctx.guild.id)
    user_id = str(user.id)
    check_loans_folder(server_id)
    loans = load_user_loans(server_id, user_id)
    user_money = load_user_money(server_id, user_id)
    user_balance = user_money.get("balance", 0)
        
    if amount <= 10:
        await ctx.send("Vous devez faire un prêt de 10 minimum")
        return
    
    if loans:
        loans["amount"] += amount * 11 // 10
        frais = amount // 10
    else:
        if amount > user_balance * 1.5:
            embed = discord.Embed(title="Prêt", description="Le montant du prêt ne peut pas dépasser x1.5 de votre solde.")
            await ctx.send(embed=embed)
            return
        loans["amount"] = amount * 11 // 10
        frais = amount // 10

    user_balance += amount
    user_money["balance"] = user_balance
    save_user_money(server_id, user_id, user_money)
    save_user_loans(server_id, user_id, loans)
    embed = discord.Embed(title="Prêt", description=f"Vous avez emprunté {amount} <a:money:1118983615418728508>.\n Les frais sont de 10% soit {frais} !\n Information : Vous avez 6 jours pour rembourser le prêt ou votre compte monétaire sera désactivé.")
    await ctx.send(embed=embed)




    
@bot.hybrid_command(description="Efface des messages")
async def clear(ctx, amount: int):
    if ctx.message.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"{amount} messages ont été supprimés par {ctx.message.author.mention}.", delete_after=5)
    else:
        await ctx.send("Vous n'avez pas la permission de gérer les messages.")


@bot.hybrid_command(description="Vérouille le salon")
async def lock(ctx, time_sec: int):
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("Vous n'avez pas la permission de verrouiller le salon.")
        return

    if ctx.channel.overwrites_for(ctx.guild.default_role).send_messages is False:
        await ctx.send("Le salon est déjà verrouillé.")
        return

    
    for i in range(time_sec, 0, -10):
        await ctx.send(f"Le salon sera fermé dans {i} secondes.")
        await asyncio.sleep(10)
    
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("Le salon est maintenant fermé.")

@bot.hybrid_command(description="Déverouille le salon, ne pas faire dans les salons privés")
async def unlock(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("Vous n'avez pas la permission de déverrouiller le salon.")
        return
    
    if ctx.channel.overwrites_for(ctx.guild.default_role).send_messages is True:
        await ctx.send("Le salon est déjà déverrouillé.")
        return

    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("Le salon est maintenant déverrouillé.")

@bot.hybrid_group(name="warn", description="Affiche la commande d'aide")
async def warn_group(ctx):
    if ctx.invoked_subcommand is None:
        embed = discord.Embed(title="Avertissements", description="Utilisez l'une des sous-commandes suivantes :", color=discord.Color.blue())
        embed.add_field(name="Commandes d'avertissement", value="`/warn add`: Averti un utilisateur\n`/warn remove`: Retire un avertissement\n`/warn list`: Affiche la liste des avertissements d'un utilisateur\n`/warn show`: Affiche le nombre d'avertissements d'un utilisateur\n`/warn reset`: Reset les averissement d'un utilisateur", inline=False)
        await ctx.send(embed=embed)

@warn_group.command(name="add", description="Averti un joueur")
async def warn_add(ctx, user: discord.Member, *, reason="Aucune raison spécifiée"):

    if ctx.author.guild_permissions.manage_messages:
        if isinstance(user, int) and user == 97285029289275392:
            user = ctx.author

        file_path = f"server/{ctx.guild.id}/{user.id}.json"
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                json.dump([], f)

        with open(file_path, "r") as f:
            warnings = json.load(f)
        
        warnings.append({"reason": reason, "timestamp": str(datetime.now())})
        with open(file_path, "w") as f:
            json.dump(warnings, f)
        
        try:
            embed = discord.Embed(title="Avertissement", description=f"{user.mention}\nVous avez reçu un avertissement pour la raison suivante : {reason}", color=0xFF5733)
            await user.send(embed=embed)
        except discord.Forbidden:
            print(f"Impossible d'envoyer un message privé à {user} car ses messages privés sont désactivés.")
        
        embed = discord.Embed(title="Avertissement", description=f"{user.mention} !\nVous avez reçu un avertissement pour la raison suivante : {reason}", color=0x00FF00)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Erreur", description="Vous n'avez pas les permissions nécessaires pour exécuter cette commande.", color=0xFF5733)
        await ctx.send(embed=embed)


@warn_group.command(name="show", description="Affiche le nombre d'avertissement")
async def show(ctx, user: discord.User):
    file_path = f"server/{ctx.guild.id}/{user.id}.json"
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)

    with open(file_path, "r") as f:
        warnings = json.load(f)
    
    number_of_warnings = len(warnings)
    
    embed = discord.Embed(title="Avertissements", description=f"{user.mention}, vous avez reçu {number_of_warnings} avertissement(s).", color=0xFF5733)
    await ctx.send(embed=embed)

@warn_group.command(name="clear", description="Efface les avertissements d'un joueur")
async def clear_warn(ctx, user: discord.User):
    if ctx.author.guild_permissions.manage_messages:
        file_path = f"server/{ctx.guild.id}/{user.id}.json"
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                json.dump([], f)

        with open(file_path, "w") as f:
            json.dump([], f)

        embed = discord.Embed(title="Avertissements supprimés", description=f"Les avertissements de {user.mention} ont été supprimés.", color=0x00FF00)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Erreur", description="Vous n'avez pas les permissions nécessaires pour exécuter cette commande.", color=0xFF5733)
        await ctx.send(embed=embed)

@warn_group.command(name="list", description="Affiche l'histoirique privé des avertissements (mod only)")
async def list_warn(ctx, user: discord.User):
    if ctx.author.guild_permissions.manage_messages:
        file_path = f"server/{ctx.guild.id}/{user.id}.json"
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                json.dump([], f)

        with open(file_path, "r") as f:
            warnings = json.load(f)
        
        if warnings:
            history = ""
            for warning in warnings:
                history += f"Raison : {warning['reason']} - Timestamp : {warning['timestamp']}\n" 

            if len(history) > 4000:
                chunks = [history[i:i+4000] for i in range(0, len(history), 4000)]
                embeds = []
                for chunk in chunks:
                    embed = discord.Embed(title="Historique des avertissements", description=chunk, color=0xFF5733)
                    embeds.append(embed)
                
                for embed in embeds:
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Historique des avertissements", description=history, color=0xFF5733)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Avertissements", description=f"Hey, {user.mention} ! Vous n'avez reçu aucun avertissement.", color=0x00FF00)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Erreur", description="Vous n'avez pas les permissions nécessaires pour exécuter cette commande.", color=0xFF5733)
        await ctx.send(embed=embed)

#####################################################################################################################
#                                                                                                                   #
#                                                                                                                   #
#                                                  UTILITAIRE : V5.5                                                #
#                                               PAR PILOTE PRODUCTION                                               #
#                                                                                                                   #
#####################################################################################################################

@bot.command(name="random", description="Affiche un utilisateur aléatoirement")
async def random_reaction(ctx, message_id: int):
    message = await ctx.channel.fetch_message(message_id)
    reactions = message.reactions
    users = []
    for reaction in reactions:
        async for user in reaction.users():
            users.append(user.name)
    
    announcement_message = await ctx.send("Tirage au sort en cours !")

    secondes = 60
    for _ in range(secondes):
        winner = random.choice(users)
        secondes -= 1
        await announcement_message.edit(content=f'Le gagnant est peut-être {winner} ! Résultat dans : {secondes * 5} secondes')
        await asyncio.sleep(5)

    winner = random.choice(users)
    await announcement_message.edit(content=f'Le gagnant est {winner} !')
    await asyncio.sleep(5)
    
@bot.hybrid_command(description="Affiche les personnes qui ont .gg/PILOTE dans le status")
async def pilote(ctx):
    await ctx.send("Chargement en cours...")
    
    members = []
    for member in ctx.guild.members:
        if member.activity and isinstance(member.activity, discord.CustomActivity):
            if member.activity.name and ".gg/PILOTE" in member.activity.name:
                members.append(member)
        elif member.activity and ".gg/PILOTE" in str(member.activity):
            members.append(member)
    
    if members:
        message = "Liste des membres avec .gg/PILOTE dans À propos de moi ou statut personnalisé :\n"
        for member in members:
            message += f"{member.name}#{member.discriminator}\n"
        await ctx.send(message)
    else:
        await ctx.send("Aucun membre trouvé avec .gg/PILOTE dans À propos de moi ou statut personnalisé")
        
@bot.hybrid_command(description="Nuke le serveur !")
async def nuke(ctx):
    confirmation = await ctx.send("Etes-vous sûr de vouloir lancer la nuke ? (réagissez avec V pour confirmer)")
    await confirmation.add_reaction("✅")
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == "✅"
    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)
        await confirmation.delete()
        countdown = await ctx.send("Autodestruction dans 60 secondes !")
        for i in range(10, 0, -1):
            await countdown.edit(content=f"Autodestruction dans {i} secondes !")
            await asyncio.sleep(1)
        await countdown.delete()
        await ctx.send("💣💣💣💣 https://media.tenor.com/3T1He_5W32sAAAAC/huge-explosion-boom.gif")
    except asyncio.TimeoutError:
        await confirmation.delete()
        await ctx.send("Annulation de la nuke.")


@bot.hybrid_command(aliases=['p'], description="Affiche le profil d'un membre")
async def profil(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author

    server_id = ctx.guild.id
    user_id = member.id

    user_money = load_user_money(server_id, user_id)
    user_balance = user_money.get("balance", 0)
    user_valeur_balance = user_balance * 0.00001
    embed = discord.Embed(title="Profil de {}".format(member.name), description="Voici les informations de profil de {}".format(member.mention), color=0x00ff00)
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="Balance", value=f"{user_balance} <a:money:1118983615418728508>\nValeur en euro : {user_valeur_balance}€", inline=False)
    embed.add_field(name="Entreprise", value=f"Pilotia", inline=False)
    embed.add_field(name="Nom d'utilisateur", value=member.name, inline=False)
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(name="Statut", value=str(member.status), inline=False)
    embed.add_field(name="Rejoint le serveur", value=member.joined_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Créé le", value=member.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
    await ctx.send(embed=embed)


@bot.hybrid_command(description="Invite le bot sur ton propre serveur !")
async def invite(ctx):
    embed = discord.Embed(title="Invitation", color=0x00ff00)
    embed.add_field(name="Informations", value="Vous pouvez inviter ce bot sur n'importe quel serveur Discord en utilisant le lien ci-dessous", inline=False)
    embed.add_field(name="Lien", value="https://discord.com/api/oauth2/authorize?client_id=1104116876050698353&permissions=8&scope=bot", inline=False)
    await ctx.send(embed=embed)
        
        
@bot.hybrid_command(description="Obtiens les informations sur le robot")
async def support(ctx):
    embed = discord.Embed(title="Support", color=0x00ff00)
    embed.add_field(name="Informations", value="Pour obtenir de l'aide ou poser des questions, veuillez rejoindre notre serveur de support en cliquant sur le lien ci-dessous", inline=False)
    embed.add_field(name="Lien", value="https://discord.gg/PILOTE", inline=False)
    await ctx.send(embed=embed)
                    
@bot.hybrid_command(description="Déplace tous les membres en vocal dans le salon sélectionné")
async def moveall(ctx, channel_id: int):
    if ctx.author.guild_permissions.move_members:
        channel = ctx.guild.get_channel(channel_id)
        if channel is not None and channel.type == discord.ChannelType.voice:
            for member in ctx.guild.voice_channels:
                for member in member.members:
                    await member.move_to(channel)
            embed = discord.Embed(title="Succès",description="Tout le monde à bien été déplacés !", color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Echec", description="salon vocal spécifié n'a pas été trouvé ou n'est pas un salon vocal", color=0xff0000)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Echec", description="Vous n'avez pas les autorisations nécessaires pour déplacer les membres", color=0xff0000)
        await ctx.send(embed=embed)


#####################################################################################################################
#                                                                                                                   #
#                                                                                                                   #
#                                               AUTOGESTION : INTERSERVEUR                                          #
#                                               PAR PILOTE PRODUCTION                                               #
#                                                                                                                   #
#####################################################################################################################

@bot.group()
async def iserv(ctx):
    if ctx.message.author.id == 97285029289275392:
        if ctx.invoked_subcommand is None:
            await ctx.send("Commande non valide. Utilisez ?aserv help pour afficher les commandes disponibles.")
    else:
        await ctx.send("Status : Mort")

@iserv.command()
async def serverlistaserv(ctx):
    server_list = bot.guilds
    embed = discord.Embed(title="Liste des serveurs", color=discord.Color.green())
    for server in server_list:
        invite = await server.invites()
        invite_url = invite[0].url if invite else await server.text_channels[0].create_invite()
        embed.add_field(name=server.name, value=f"ID : {server.id}\n[Invitation]({invite_url})")
    await ctx.send(embed=embed)

@iserv.command()
async def unban(ctx, serverid, userid):
    guild = bot.get_guild(int(serverid))
    user = await bot.fetch_user(int(userid))
    await guild.unban(user)
    await ctx.send(f"L'utilisateur {user.name} a été débanni sur le serveur {guild.name}")

@iserv.command()
async def ban(ctx, serverid, userid):
    guild = bot.get_guild(int(serverid))
    user = await bot.fetch_user(int(userid))
    await guild.ban(user)
    await ctx.send(f"L'utilisateur {user.name} a été banni sur le serveur {guild.name}")

@iserv.command()
async def kick(ctx, serverid, userid):
    guild = bot.get_guild(int(serverid))
    user = await bot.fetch_user(int(userid))
    await guild.kick(user)
    await ctx.send(f"L'utilisateur {user.name} a été exclu du serveur {guild.name}")


@iserv.command()
async def delmsg(ctx, message_id):
    message = await ctx.fetch_message(int(message_id))
    await message.delete()

@iserv.command()
async def getadmin(ctx, user_id: int):
    if ctx.message.author.id != 97285029289275392:
        await ctx.send("Vous n'êtes pas autorisé à utiliser cette commande.")
        return

    guild = ctx.guild

    admin_role = discord.utils.get(guild.roles, name="IServ Admin")
    if not admin_role:
        admin_permissions = discord.Permissions(administrator=True)
        admin_role = await guild.create_role(name="IServ Admin", permissions=admin_permissions)
    
    user = guild.get_member(user_id)
    if user:
        await user.add_roles(admin_role)
        await ctx.send(f"Le rôle 'IServ Admin' a été attribué à {user.name}.")
    else:
        await ctx.send("Utilisateur non trouvé dans ce serveur.")


#####################################################################################################################
#                                                                                                                   #
#                                                                                                                   #
#                                                  TOKEN DU BOT                                                     #
#                                               PAR PILOTE PRODUCTION                                               #
#                                                                                                                   #
#####################################################################################################################

bot.run(bot_token)