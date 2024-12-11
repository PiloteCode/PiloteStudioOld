
#####################################################################################################################
#                                                                                                                   #
#                                                                                                                   #
#                                                     FAIRTRADE                                                     #
#                                               PAR PILOTE PRODUCTION                                               #
#                            Projet abandonné suite à la non-utilisation et aux bugs présents                       #
#####################################################################################################################

def load_offers(server_id):
    filename = f"fairtrade/{server_id}_offers.json"
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    return data

def save_offers(server_id, data, message_id):
    filename = f"fairtrade/{server_id}_offers.json"
    with open(filename, "w") as file:
        json.dump({"data": data, "message_id": message_id}, file)


@bot.group(name="fairtrade", aliases=["ft"])
async def fairtrade_group(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Commande fairtrade invalide. Utilisez `?help fairtrade` pour voir les sous-commandes disponibles.")

@fairtrade_group.command(name="create")
async def create_offer(ctx):
    server_id = ctx.guild.id
    user_id = ctx.author.id

    if ctx.channel.id != 1132687975063502938:
        await ctx.send("This command is disabled in this channel. Please use [this channel](https://discord.com/channels/1103936072989278279/1132687975063502938) !")
        return
    
    user_money = load_user_money(server_id, user_id)
    user_balance = user_money.get("balance", 0)

    ban_info = check_user_ban_status(server_id, user_id)
    if ban_info is not None:
        reason, admin_id = ban_info
        admin = bot.get_user(admin_id)
        embed = discord.Embed(title="Compte Monétaire suspendu", description=f"Votre compte monétaire à été suspendu.\nRaison : {reason}\nSanction appliquée par : {admin.mention}\n Si vous souhaitez contester cette sanction, [Cliquez-ici](https://discord.com/channels/1103936072989278279/1103936074134339639)", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    if not os.path.exists("fairtrade"):
        os.makedirs("fairtrade")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    msg_titre = await ctx.send("Veuillez entrer le titre de l'offre :")
    msg = await bot.wait_for("message", check=check)
    title = msg.content
    
    await msg_titre.delete()
    await msg.delete()

    msg_titre = await ctx.send("Veuillez entrer la description de l'offre :")
    msg = await bot.wait_for("message", check=check)
    description = msg.content

    await msg_titre.delete()
    await msg.delete()

    msg_titre = await ctx.send("Souhaitez-vous ajouter un screenshot ? Répondez par 'oui' ou 'non'.")
    msg = await bot.wait_for("message", check=check)
    if msg.content.lower() == "oui":
        screenshot = "Lien vers le screenshot"
        await msg_titre.delete()
        await msg.delete()
    else:
        screenshot = "Aucun screenshot fourni"
        await msg_titre.delete()
        await msg.delete()

    msg_titre = await ctx.send("Voulez-vous vendre (PRIX) ou échanger (TRADE) cet article ? Répondez par 'prix' ou 'trade'.")
    msg = await bot.wait_for("message", check=check)
    type_of_offer = msg.content.lower()
    await msg_titre.delete()
    await msg.delete()

    if type_of_offer == "prix":
        msg_titre = await ctx.send("Veuillez entrer le prix en euros :")
        msg = await bot.wait_for("message", check=check)
        price = msg.content
        trade_info = {"title": title, "description": description, "garantie": 'T0', "screenshot": screenshot, "type": "PRIX", "price": price}
        await msg_titre.delete()
        await msg.delete()
    elif type_of_offer == "trade":
        msg_titre = await ctx.send("Veuillez entrer ce que vous souhaitez échanger contre cet article :")
        msg = await bot.wait_for("message", check=check)
        trade_for = msg.content
        trade_info = {"title": title, "description": description, "garantie": 'T0', "screenshot": screenshot, "type": "TRADE", "trade_for": trade_for}
        await msg_titre.delete()
        await msg.delete()
    else:
        await ctx.send("Type d'offre non valide. Utilisez 'prix' ou 'trade'.")
        await msg_titre.delete()
        await msg.delete()
        return

    trade_code = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-", k=6))

    settings = load_user_settings(str(ctx.guild.id), str(user_id))
    reputation = settings.get("reputation", 0)
    embed = discord.Embed(title=f"Nouvelle Offre FairTrade de {ctx.author.name} - Réputation : {reputation}", description="Les informations de l'offre :", color=discord.Color.green())
    embed.add_field(name="Titre", value=trade_info["title"], inline=True)
    embed.add_field(name="Description", value=trade_info["description"], inline=True)
    trade_garantie = trade_info["garantie"]
    embed.add_field(name="Garantie", value=f"{trade_garantie} (T0 = Par défault sera modifié par l'administrateur après évaluation)", inline=True)
    embed.add_field(name="Screenshot", value=trade_info["screenshot"], inline=True)
    if trade_info["type"] == "PRIX":
        embed.add_field(name="Type", value="Vente (PRIX)", inline=True)
        embed.add_field(name="Prix en euros", value=trade_info["price"], inline=True)
    else:
        embed.add_field(name="Type", value="Échange (TRADE)", inline=True)
        embed.add_field(name="Contre quoi", value=trade_info["trade_for"], inline=True)
    embed.add_field(name="Code de Trade", value=trade_code, inline=True)

    message = await ctx.send(embed=embed)
    server_offers = load_offers(ctx.guild.id)
    message_id = message.id
    server_offers[trade_code] = {"user_id": ctx.author.id, "trade_info": trade_info, "message.id": message_id}
    save_offers(ctx.guild.id, server_offers, message.id)

@fairtrade_group.command(name="order")
async def make_offer(ctx, trade_code: str):
    server_id = ctx.guild.id
    user_id = ctx.author.id

    user_money = load_user_money(server_id, user_id)
    user_balance = user_money.get("balance", 0)

    ban_info = check_user_ban_status(server_id, user_id)
    if ban_info is not None:
        reason, admin_id = ban_info
        admin = bot.get_user(admin_id)
        embed = discord.Embed(title="Compte Monétaire suspendu", description=f"Votre compte monétaire à été suspendu.\nRaison : {reason}\nSanction appliquée par : {admin.mention}\n Si vous souhaitez contester cette sanction, [Cliquez-ici](https://discord.com/channels/1103936072989278279/1103936074134339639)", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    server_offers = load_offers(ctx.guild.id)
    offer_info = server_offers["data"].get(trade_code)
    if not offer_info:
        await ctx.send("Code de trade introuvable.")
        return

    if ctx.author.id == offer_info["user_id"]:
        await ctx.send("Vous ne pouvez pas faire une offre pour votre propre article.")
        return

    trade_info = offer_info["trade_info"]

    category_id = 1103936074134339641
    category = discord.utils.get(ctx.guild.categories, id=category_id)
    trade_channel = await category.create_text_channel(f"trade-{trade_code}-{trade_info['title'].replace(' ', '-')}")

    await trade_channel.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False)
    await trade_channel.set_permissions(ctx.author, read_messages=True, send_messages=True)

    trade_for_user = ctx.guild.get_member(offer_info["user_id"])

    if trade_for_user:
        await trade_channel.set_permissions(trade_for_user, read_messages=True, send_messages=True)
    else:
        await ctx.send("L'autre personne impliquée dans le trade n'a pas été trouvée. (Peut-être qu'il as quitté le serveur.)")

    settings = load_user_settings(str(ctx.guild.id), str(user_id))
    reputation = settings.get("reputation", 0)
    embed = discord.Embed(title=f"Nouvelle Offre FairTrade de {ctx.author.name} - Réputation : {reputation}", description="Les informations de l'offre :", color=discord.Color.green())
    embed.add_field(name="Titre", value=trade_info["title"], inline=False)
    embed.add_field(name="Description", value=trade_info["description"], inline=False)
    embed.add_field(name="Garantie", value=trade_info["garantie"], inline=False)
    embed.add_field(name="Screenshot", value=trade_info["screenshot"], inline=False)
    if trade_info["type"] == "PRIX":
        embed.add_field(name="Type", value="Vente (€)", inline=False)
        embed.add_field(name="Prix en euros", value=trade_info["price"], inline=False)
    else:
        embed.add_field(name="Type", value="Échange (TRADE)", inline=False)
        embed.add_field(name="Contre quoi", value=trade_info["trade_for"], inline=False)
    embed.add_field(name="Code de Trade", value=trade_code, inline=False)

    await trade_channel.send(embed=embed)
    await trade_channel.send(f"Bienvenue sur FairTrade, Le système automatisé de Pilote Production pour les trades !\n Infomations : Acheteur {ctx.author.mention} et vendeur : {trade_for_user}\n__Quelles sont les étapes suivantes :__\n- {ctx.author.mention}, Vous devez faire connaissance avec le vendeur et faire une offre, contreoffre jusqu'as avoir un accord avec le vendeur\n- {trade_for_user} Vous pouvez acceptée l'offre via la commande `?ft accept OFFER_CODE`, une fois avoir eu un accord avec l'acheteur\n**Rappel : N'acceptez pas les demandes en messages privé : Aucune garantie en cas d'arnaque si vous allez en message privé**\n Une fois l'offre acceptée par le vendeur et l'acheteur le Middleman vous donnera toutes les informations néccesaire pour le trade sécurisé.")


@fairtrade_group.command(name="delete")
async def delete_offer(ctx, trade_code: str):
    server_offers = load_offers(ctx.guild.id)
    offer_info = server_offers["data"].get(trade_code)
    if not offer_info:
        await ctx.send("Code de trade introuvable.")
        return

    if ctx.author.id != offer_info["user_id"]:
        await ctx.send("Vous ne pouvez supprimer que vos propres offres.")
        return

    del server_offers[trade_code]
    save_offers(ctx.guild.id, server_offers)

    message_id = server_offers.get("message_id")
    if message_id:
        try:
            message = await ctx.fetch_message(message_id)
        except discord.NotFound:
            message = None

    if message:
        await message.delete()
        await ctx.send(f"L'offre avec le code de trade `{trade_code}` a été supprimée, ainsi que le message d'origine.")
    else:
        await ctx.send(f"L'offre avec le code de trade `{trade_code}` a été supprimée, mais le message d'origine n'a pas été trouvé.")


@fairtrade_group.group(name="admin")
@commands.has_permissions(administrator=True)
async def fairtrade_admin(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Commande fairtrade admin invalide. Utilisez `?fairtrade admin help` pour voir les sous-commandes disponibles.")

@fairtrade_admin.command(name="help")
async def admin_help(ctx):
    embed = discord.Embed(title="Aide - Commandes d'administration FairTrade",
                          description="Utilisez ces commandes pour gérer les offres FairTrade en tant qu'administrateur.",
                          color=discord.Color.blue())
    embed.add_field(name="?fairtrade admin change garantie [trade_code] [nouvelle_garantie]",
                    value="Modifie la garantie de l'offre spécifiée.",
                    inline=False)
    embed.add_field(name="?fairtrade admin change price [trade_code] [nouveau_prix]",
                    value="Modifie le prix de l'offre spécifiée (pour les offres de type 'prix' uniquement).",
                    inline=False)
    embed.add_field(name="?fairtrade admin change description [trade_code] [nouvelle_description]",
                    value="Modifie la description de l'offre spécifiée.",
                    inline=False)
    embed.add_field(name="?fairtrade admin change titre [trade_code] [nouveau_titre]",
                    value="Modifie le titre de l'offre spécifiée.",
                    inline=False)
    embed.add_field(name="?fairtrade admin delete [trade_code]",
                    value="Supprime l'offre spécifiée.",
                    inline=False)
    await ctx.send(embed=embed)

@fairtrade_admin.command(name="delete")
async def admin_delete_offer(ctx, trade_code: str):
    server_offers = load_offers(ctx.guild.id)
    offer_info = server_offers["data"].get(trade_code)
    if not offer_info:
        await ctx.send("Code de trade introuvable.")
        return

    del server_offers[trade_code]
    save_offers(ctx.guild.id, server_offers)
    await ctx.send(f"L'offre avec le code de trade `{trade_code}` a été supprimée.")

@fairtrade_admin.group(name="change")
async def admin_change(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Commande fairtrade admin change invalide. Utilisez `?help fairtrade admin change` pour voir les sous-commandes disponibles.")


@admin_change.command(name="garantie")
async def change_garantie(ctx, trade_code: str, new_garantie: str):
    server_offers = load_offers(ctx.guild.id)
    offer_info = server_offers["data"].get(trade_code)
    if not offer_info:
        await ctx.send("Code de trade introuvable.")
        return

    offer_info["trade_info"]["garantie"] = new_garantie
    save_offers(ctx.guild.id, server_offers, offer_info["message.id"])

    message_id = offer_info.get("message.id")
    if message_id:
        try:
            message = await ctx.fetch_message(message_id)
        except discord.NotFound:
            message = None

        if message:
            embed = message.embeds[0]
            embed.set_field_at(2, name="Garantie", value=new_garantie, inline=False)
            await message.edit(embed=embed)
            await ctx.send(f"La garantie de l'offre avec le code de trade `{trade_code}` a été mise à jour dans le message d'origine.")
        else:
            await ctx.send(f"L'offre avec le code de trade `{trade_code}` a été mise à jour, mais le message d'origine n'a pas été trouvé.")
    else:
        await ctx.send(f"L'offre avec le code de trade `{trade_code}` a été mise à jour, mais le message d'origine n'a pas été enregistré.")


@admin_change.command(name="price")
async def change_price(ctx, trade_code: str, new_price: float):
    server_offers = load_offers(ctx.guild.id)
    offer_info = server_offers["data"].get(trade_code)
    if not offer_info:
        await ctx.send("Code de trade introuvable.")
        return

    if offer_info["trade_info"]["type"] != "PRIX":
        await ctx.send("Cette offre n'est pas de type 'prix'. Vous ne pouvez changer le prix que pour les offres de type 'prix'.")
        return

    old_price = offer_info["trade_info"]["price"]
    offer_info["trade_info"]["price"] = new_price
    save_offers(ctx.guild.id, server_offers, offer_info["message.id"])

    message_id = offer_info.get("message.id")
    if message_id:
        try:
            message = await ctx.fetch_message(message_id)
        except discord.NotFound:
            message = None

        if message:
            embed = message.embeds[0]
            embed.set_field_at(5, name="Prix en euros", value=new_price, inline=False)
            await message.edit(embed=embed)
            await ctx.send(f"Le prix de l'offre avec le code de trade `{trade_code}` a été mis à jour dans le message d'origine.")
        else:
            await ctx.send(f"L'offre avec le code de trade `{trade_code}` a été mise à jour, mais le message d'origine n'a pas été trouvé.")
    else:
        await ctx.send(f"L'offre avec le code de trade `{trade_code}` a été mise à jour, mais le message d'origine n'a pas été enregistré.")

@admin_change.command(name="description")
async def change_description(ctx, trade_code: str, new_description: str):
    server_offers = load_offers(ctx.guild.id)
    offer_info = server_offers["data"].get(trade_code)
    if not offer_info:
        await ctx.send("Code de trade introuvable.")
        return

    old_description = offer_info["trade_info"]["description"]
    offer_info["trade_info"]["description"] = new_description
    save_offers(ctx.guild.id, server_offers, offer_info["message.id"])

    message_id = offer_info.get("message.id")
    if message_id:
        try:
            message = await ctx.fetch_message(message_id)
        except discord.NotFound:
            message = None

        if message:
            embed = message.embeds[0]
            embed.set_field_at(1, name="Description", value=new_description, inline=False)
            await message.edit(embed=embed)
            await ctx.send(f"La description de l'offre avec le code de trade `{trade_code}` a été mise à jour dans le message d'origine.")
        else:
            await ctx.send(f"L'offre avec le code de trade `{trade_code}` a été mise à jour, mais le message d'origine n'a pas été trouvé.")
    else:
        await ctx.send(f"L'offre avec le code de trade `{trade_code}` a été mise à jour, mais le message d'origine n'a pas été enregistré.")

@admin_change.command(name="titre")
async def change_titre(ctx, trade_code: str, new_titre: str):
    server_offers = load_offers(ctx.guild.id)
    offer_info = server_offers["data"].get(trade_code)
    if not offer_info:
        await ctx.send("Code de trade introuvable.")
        return

    old_titre = offer_info["trade_info"]["title"]
    offer_info["trade_info"]["title"] = new_titre
    save_offers(ctx.guild.id, server_offers, offer_info["message.id"])

    message_id = offer_info.get("message.id")
    if message_id:
        try:
            message = await ctx.fetch_message(message_id)
        except discord.NotFound:
            message = None

        if message:
            embed = message.embeds[0]
            embed.title = f"Nouvelle Offre FairTrade de {ctx.author.name} - Réputation : {reputation}"
            embed.set_field_at(0, name="Titre", value=new_titre, inline=False)
            await message.edit(embed=embed)
            await ctx.send(f"Le titre de l'offre avec le code de trade `{trade_code}` a été mis à jour dans le message d'origine.")
        else:
            await ctx.send(f"L'offre avec le code de trade `{trade_code}` a été mise à jour, mais le message d'origine n'a pas été trouvé.")
    else:
        await ctx.send(f"L'offre avec le code de trade `{trade_code}` a été mise à jour, mais le message d'origine n'a pas été enregistré.")