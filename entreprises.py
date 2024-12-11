# PROJET ENTREPRISE 2023 : Abandonné depuis le 26 octobre

entreprise_folder = "entreprises"

def load_entreprise(server_id, entreprise_name):
    try:
        with open(f"{entreprise_folder}/{server_id}/{entreprise_name}.json", "r") as file:
            entreprise_data = json.load(file)
    except FileNotFoundError:
        entreprise_data = {
            "nom": entreprise_name,
            "date_creation": "",
            "chef": "",
            "privacy": "",
            "banque": 500,
            "tier": 0,
            "employes": [],
            "co_owners": [],
            "description": "",
            "isSetup": False
        }
    return entreprise_data

def search_entreprise_by_user_id(server_id, user_id):
    user_id_str = str(user_id)

    for filename in os.listdir(f"{entreprise_folder}/{server_id}"):
        if filename.endswith(".json"):
            entreprise_data = load_entreprise(server_id, filename[:-5])
            print(f"User ID: {user_id_str}")
            print(f"Entreprise Data ID: {entreprise_data['chef']}")
            print(f"Entreprise Data: {entreprise_data}")
            if user_id_str == entreprise_data["chef"]:
                return entreprise_data["nom"]
            elif any(user_id_str == co_owner["id"] for co_owner in entreprise_data["co_owners"]):
                return entreprise_data["nom"]
            elif any(user_id_str == employee["id"] for employee in entreprise_data["employes"]):
                return entreprise_data["nom"]
    return None



def save_entreprise(server_id, entreprise_name, entreprise_data):
    with open(f"{entreprise_folder}/{server_id}/{entreprise_name}.json", "w") as file:
        json.dump(entreprise_data, file)

@bot.group(aliases=["e"], description="Gestion des entreprises")
async def entreprise(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Utilisation : /help entreprise")

@entreprise.command(description="Création d'une entreprise")
async def create(ctx, nom):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    ctx.send("Cette fonctionnalité n'est pas encore disponible au public !")
    return

    server_folder = f"{entreprise_folder}/{server_id}"
    if not os.path.exists(server_folder):
        os.makedirs(server_folder)

    entreprise_path = f"{server_folder}/{user_id}.json"

    if os.path.exists(entreprise_path):
        await ctx.send("Vous avez déjà une entreprise. Vous ne pouvez pas en créer plus d'une.")
        return

    entreprise_data = {
        "nom": nom,
        "date_creation": "",
        "chef": ctx.author.id,
        "privacy": "",
        "banque": 500,
        "tier": 0,
        "employes": [],
        "co_owners": [],
        "description": "",
        "isSetup": False
    }

    with open(entreprise_path, "w") as file:
        json.dump(entreprise_data, file)

    await ctx.send(f"Entreprise '{nom}' créée. Veuillez configurer votre entreprise en utilisant `/entreprise setup`")

@entreprise.command(description="Configurer une entreprise")
async def setup(ctx):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    entreprise_path = f"{entreprise_folder}/{server_id}/{user_id}.json"

    if not os.path.exists(entreprise_path):
        await ctx.send(f"{ctx.author.display_name}, vous n'avez pas encore créé d'entreprise. Utilisez `/entreprise create` pour en créer une.")
        return
    print(f"Authy {user_id}")
    print("Lancement du mode débug")
    entreprise_name = search_entreprise_by_user_id(server_id, user_id)
    if entreprise_name is None:
        await ctx.send("Vous n'êtes pas associé à une entreprise.")
        return
    
    entreprise_data = load_entreprise(server_id, entreprise_name)
    if ctx.author.name != entreprise_data["chef"] and ctx.author.id not in entreprise_data["co_owners"]:
        await ctx.send("Vous n'avez pas les permissions pour effectuer cette action.")
        return

    if entreprise_data["isSetup"]:
        await ctx.send("Votre entreprise a déjà été configurée.")
        return

    await ctx.send("Veuillez définir la description de votre entreprise (600 secondes pour répondre) :")
    try:
        description_msg = await bot.wait_for("message", timeout=600, check=lambda message: message.author == ctx.author)
        entreprise_data["description"] = description_msg.content
    except asyncio.TimeoutError:
        await ctx.send("Temps écoulé. La description n'a pas été définie et le processus a été annulé.")
        return

    await ctx.send("Veuillez définir le salaire des employés (minimum 100$ par semaine au Tier 0) :")
    try:
        salary_msg = await bot.wait_for("message", timeout=600, check=lambda message: message.author == ctx.author)
        salary = int(salary_msg.content)
        if salary < 100:
            await ctx.send("Le salaire doit être d'au moins 100$. Veuillez réessayer.")
            return
        entreprise_data["salaire"] = salary
    except (asyncio.TimeoutError, ValueError):
        await ctx.send("Temps écoulé ou montant invalide. Le salaire doit être un nombre supérieur ou égal à 100.")
        return

    await ctx.send("Veuillez définir le type de votre entreprise (serveurs, électricité, loterie, commerce) :")
    try:
        type_msg = await bot.wait_for("message", timeout=600, check=lambda message: message.author == ctx.author)
        entreprise_type = type_msg.content.lower()
        if entreprise_type not in ["serveurs", "électricité", "paris", "commerce"]:
            await ctx.send("Le type d'entreprise est invalide. Veuillez choisir parmi : serveurs, électricité, loterie, commerce.")
            return
        entreprise_data["type"] = entreprise_type
    except asyncio.TimeoutError:
        await ctx.send("Temps écoulé. Le type d'entreprise n'a pas été défini.")
        return

    entreprise_data["isSetup"] = True
    save_entreprise(server_id, user_id, entreprise_data)

    await ctx.send("Félicitations ! Votre entreprise a été configurée avec succès.")
    
@entreprise.command(description="Change le fondateur de l'entreprise")
async def owner(ctx, new_owner: discord.Member):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    entreprise_name = search_entreprise_by_user_id(server_id, user_id)
    if entreprise_name is None:
        await ctx.send("Vous n'êtes pas associé à une entreprise.")
        return

    entreprise_path = f"{entreprise_folder}/{server_id}/{user_id}.json"
    new_owner_id = str(new_owner.id)
    new_owner_path = f"{entreprise_folder}/{server_id}/{new_owner_id}.json"

    entreprise_data = load_entreprise(server_id, entreprise_name)
    if ctx.author.name != entreprise_data["chef"]:
        await ctx.send("Vous n'êtes pas le fondateur de cette entreprise.")
        return

    if new_owner.id not in [co_owner["id"] for co_owner in entreprise_data["co_owners"]]:
        await ctx.send(f"{new_owner.name} doit être un co-propriétaire pour devenir propriétaire.")
        return

    os.rename(entreprise_path, new_owner_path)

    entreprise_data["chef"] = new_owner.name
    save_entreprise(server_id, new_owner_id, entreprise_data)

    await ctx.send(f"{new_owner.name} est maintenant le propriétaire de l'entreprise {entreprise_name}.")


@entreprise.command(description="Ajoute ou retire un co-propriétaire")
async def co_owner(ctx, action, target: discord.Member):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    entreprise_name = search_entreprise_by_user_id(server_id, user_id)
    if entreprise_name is None:
        await ctx.send("Vous n'êtes pas associé à une entreprise.")
        return

    entreprise_data = load_entreprise(server_id, entreprise_name)

    if action == "add":
        if target.id in [co_owner["id"] for co_owner in entreprise_data["co_owners"]] or target.id in [employee["id"] for employee in entreprise_data["employes"]]:
            await ctx.send(f"{target.name} est déjà un employé ou un co-propriétaire de l'entreprise.")
        else:
            entreprise_data["co_owners"].append({"id": target.id, "name": target.name})
            save_entreprise(server_id, entreprise_name, entreprise_data)
            await ctx.send(f"{target.name} est maintenant un co-propriétaire de l'entreprise {entreprise_name}.")
    elif action == "remove":
        if any(co_owner["id"] == target.id for co_owner in entreprise_data["co_owners"]):
            entreprise_data["co_owners"] = [co_owner for co_owner in entreprise_data["co_owners"] if co_owner["id"] != target.id]
            save_entreprise(server_id, entreprise_name, entreprise_data)
            await ctx.send(f"{target.name} n'est plus un co-propriétaire de l'entreprise {entreprise_name}.")
        else:
            await ctx.send(f"{target.name} n'est pas un co-propriétaire de l'entreprise.")


@entreprise.command(description="Voir le tier de l'entreprise")
async def tier(ctx, nom):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    entreprise_data = load_entreprise(server_id, nom)

    if not entreprise_data["isSetup"]:
        await ctx.send("L'entreprise n'est pas encore configurée.")
        return

    tier = get_tier(entreprise_data["salaire"])
    await ctx.send(f"L'entreprise {nom} est au tier {tier}.")

def get_tier(salaire):
    if salaire >= 1500:
        return 5
    elif salaire >= 1000:
        return 3
    elif salaire >= 750:
        return 2
    elif salaire >= 500:
        return 1
    else:
        return 0
    
@entreprise.command(description="Acheter un tier pour l'entreprise")
async def tier_buy(ctx, tier: int):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    entreprise_name = search_entreprise_by_user_id(server_id, user_id)
    if entreprise_name is None:
        await ctx.send("Vous n'êtes pas associé à une entreprise.")
        return

    entreprise_data = load_entreprise(server_id, entreprise_name)

    if ctx.author.name != entreprise_data["chef"] and ctx.author.id not in [co_owner["id"] for co_owner in entreprise_data["co_owners"]]:
        await ctx.send("Vous n'avez pas les permissions pour effectuer cette action.")
        return

    prix_tier = {1: 75000, 2: 10000, 3: 15000, 4: 75000, 5: 100000}

    if tier not in prix_tier:
        await ctx.send("Le tier sélectionné n'est pas valide.")
        return

    if entreprise_data["banque"] < prix_tier[tier]:
        await ctx.send("L'entreprise n'a pas assez d'argent pour acheter ce tier.")
        return

    entreprise_data["classement"] = tier
    entreprise_data["banque"] -= prix_tier[tier]

    save_entreprise(server_id, entreprise_name, entreprise_data)

    await ctx.send(f"L'entreprise {entreprise_name} a acheté le tier {tier}. Le salaire des employés a été mis à jour au minimum de ce tier.")

def search_entreprise_by_name(server_id, entreprise_name):
    for filename in os.listdir(f"{entreprise_folder}/{server_id}"):
        if filename.endswith(".json"):
            entreprise_data = load_entreprise(server_id, filename[:-5])
            if entreprise_name.lower() == entreprise_data["nom"].lower():
                return entreprise_data
    return None

@entreprise.command(description="Affiche les informations sur l'entreprise")
async def info(ctx, nom):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)


    entreprise_name = search_entreprise_by_name(server_id, nom)
    if entreprise_name is None:
        await ctx.send(f"L'entreprise {nom} n'existe pas.")
        return


    entreprise_data = load_entreprise(server_id, entreprise_name)

    embed = discord.Embed(title=f"Informations sur l'entreprise {entreprise_name}", color=discord.Color.blue())
    embed.add_field(name="Date de création", value=entreprise_data["date_creation"], inline=True)
    embed.add_field(name="Chef", value=entreprise_data["chef"], inline=True)
    embed.add_field(name="Banque", value=f"${entreprise_data['banque']}", inline=True)
    embed.add_field(name="Tier", value=entreprise_data["tier"], inline=True)
    embed.add_field(name="Description", value=entreprise_data["description"], inline=False)

    co_owners_str = ", ".join(entreprise_data["co_owners"])
    employes_str = ", ".join(entreprise_data["employes"])

    embed.add_field(name="Co-propriétaires", value=co_owners_str, inline=False)
    embed.add_field(name="Employés", value=employes_str, inline=False)
    embed.add_field(name="Type d'entreprise", value=entreprise_data["type"], inline=True)

    await ctx.send(embed=embed)

@entreprise.command(description="Quitte votre entreprise")
async def leave(ctx, raison):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    entreprise_data = search_entreprise_by_user_id(server_id, user_id)

    if not entreprise_data:
        await ctx.send("Vous n'êtes dans aucune entreprise.")
        return

    if user_id == entreprise_data["chef"] or user_id in [co_owner["id"] for co_owner in entreprise_data["co_owners"]]:
        await ctx.send("Vous ne pouvez pas quitter l'entreprise en tant que fondateur ou co-propriétaire.")
        return

    if user_id in [employee["id"] for employee in entreprise_data["employes"]]:
        entreprise_data["employes"] = [employee for employee in entreprise_data["employes"] if employee["id"] != user_id]

    save_entreprise(server_id, entreprise_data["nom"], entreprise_data)

    if ctx.guild.id == 1103936072989278279:
        print(f"{ctx.author.name} a quitté l'entreprise {entreprise_data['nom']} pour la raison suivante : {raison}")

    await ctx.send(f"Vous avez quitté l'entreprise {entreprise_data['nom']} pour la raison suivante : {raison}")

@entreprise.command(description="Dissout votre entreprise")
async def disband(ctx):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    entreprise_data = search_entreprise_by_user_id(server_id, user_id)

    if not entreprise_data:
        await ctx.send("Vous n'êtes dans aucune entreprise.")
        return

    if user_id != entreprise_data["chef"]:
        await ctx.send("Vous n'avez pas les permissions pour dissoudre cette entreprise.")
        return

    os.remove(f"{entreprise_folder}/{server_id}/{entreprise_data['nom']}.json")

    await ctx.send(f"L'entreprise {entreprise_data['nom']} a été dissoute et les données ont été supprimées.")

@entreprise.command(description="Éjecte un membre de votre entreprise")
async def eject(ctx, target: discord.Member, raison):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    entreprise_data = search_entreprise_by_user_id(server_id, user_id)

    if not entreprise_data:
        await ctx.send("Vous n'êtes dans aucune entreprise.")
        return

    if user_id != entreprise_data["chef"] and user_id not in [co_owner["id"] for co_owner in entreprise_data["co_owners"]]:
        await ctx.send("Vous n'avez pas les permissions pour éjecter un membre de l'entreprise.")
        return

    if target.id not in [employee["id"] for employee in entreprise_data["employes"]]:
        await ctx.send(f"{target.name} n'est pas un membre de l'entreprise.")
        return

    entreprise_data["employes"] = [employee for employee in entreprise_data["employes"] if employee["id"] != target.id]

    save_entreprise(server_id, entreprise_data["nom"], entreprise_data)

    if ctx.guild.id == 1103936072989278279:
        print(f"{target.name} a été éjecté de l'entreprise {entreprise_data['nom']} pour la raison suivante : {raison}")

    await ctx.send(f"{target.name} a été éjecté de l'entreprise {entreprise_data['nom']} pour la raison suivante : {raison}")


@entreprise.command(description="Met à jour le salaire des employés en fonction du tier")
async def update_salary(ctx):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)
    
    entreprise_nom = search_entreprise_by_user_id(server_id, user_id)
    if not entreprise_nom:
        await ctx.send("Vous n'êtes membre d'aucune entreprise.")
        return

    entreprise_data = load_entreprise(server_id, entreprise_nom)

    if ctx.author.name != entreprise_data["chef"] and ctx.author not in entreprise_data["co_owners"]:
        await ctx.send("Vous n'avez pas les permissions pour mettre à jour le salaire des employés.")
        return

    tier = get_tier(entreprise_data["salaire"])
    minimum_salaire = get_minimum_salaire(tier)
    if entreprise_data["salaire"] < minimum_salaire:
        entreprise_data["salaire"] = minimum_salaire

    save_entreprise(server_id, entreprise_nom, entreprise_data)

    await ctx.send(f"Le salaire des employés de l'entreprise {entreprise_nom} a été mis à jour en fonction du tier.")


    await ctx.send(f"Le salaire des employés de l'entreprise {nom} a été mis à jour en fonction du tier.")
@entreprise.command(description="Définit la politique de confidentialité de l'entreprise")
async def privacy(ctx, politique):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    entreprise_nom = search_entreprise_by_user_id(server_id, user_id)
    if not entreprise_nom:
        await ctx.send("Vous n'êtes membre d'aucune entreprise.")
        return

    entreprise_data = load_entreprise(server_id, entreprise_nom)

    if ctx.author.name != entreprise_data["chef"] and ctx.author not in entreprise_data["co_owners"]:
        await ctx.send("Vous n'avez pas les permissions pour définir la politique de confidentialité de l'entreprise.")
        return

    if politique.lower() not in ["public", "privé"]:
        await ctx.send("La politique de confidentialité doit être 'public' ou 'privé'.")
        return

    entreprise_data["privacy"] = politique.lower()
    save_entreprise(server_id, entreprise_nom, entreprise_data)

    await ctx.send(f"La politique de confidentialité de l'entreprise {entreprise_nom} a été définie comme '{politique}'.")

@entreprise.command(description="Invite un membre dans une entreprise")
async def invite(ctx, target: discord.Member):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    entreprise_nom = search_entreprise_by_user_id(server_id, user_id)
    if not entreprise_nom:
        await ctx.send("Vous n'êtes membre d'aucune entreprise.")
        return

    entreprise_data = load_entreprise(server_id, entreprise_nom)

    ban_info = check_user_ban_status(server_id, target)
    if ban_info is not None:
        reason, admin_id = ban_info
        admin = bot.get_user(admin_id)
        embed = discord.Embed(title="Compte Monétaire suspendu", description=f"Votre compte monétaire à été suspendu.\nRaison : {reason}\nSanction appliquée par : {admin.mention}\n Si vous souhaitez contester cette sanction, [Cliquez-ici](https://discord.com/channels/1103936072989278279/1103936074134339639)", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    if ctx.author.id != entreprise_data["chef_id"] and ctx.author.id not in entreprise_data["co_owners"]:
        await ctx.send("Vous n'avez pas les permissions pour inviter un membre dans l'entreprise.")
        return

    if target.id in entreprise_data["employes"]:
        await ctx.send(f"{target.name} est déjà un employé de l'entreprise.")
        return

    invitation_message = await ctx.send(f"{target.mention}, vous êtes invité à rejoindre l'entreprise {entreprise_nom}. Cliquez sur ✅ pour accepter (l'invitation expire dans 10 minutes).")

    await invitation_message.add_reaction('✅')

    def check(reaction, user):
        return user == target and str(reaction.emoji) == '✅' and reaction.message.id == invitation_message.id

    try:
        await bot.wait_for("reaction_add", timeout=600, check=check)
        entreprise_data["employes"].append(target.id)
        save_entreprise(server_id, entreprise_nom, entreprise_data)

        await ctx.send(f"{target.name} a accepté l'invitation et rejoint l'entreprise {entreprise_nom}.")
    except asyncio.TimeoutError:
        await ctx.send(f"L'invitation pour {target.name} a expiré.")


@entreprise.group(name="electricity", aliases=["elec"], description="Gestion de l'électricité dans l'entreprise")
async def electricity(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Utilisation : /help entreprise electricity")

@entreprise.group(name="servers", description="Gestion des serveurs dans l'entreprise")
async def servers(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Utilisation : /help entreprise servers")

@electricity.command(name="sell", description="Vendre de l'électricité d'une autre entreprise")
async def electricity_sell(ctx, quantite: int, prix: int):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    entreprise_nom = search_entreprise_by_user_id(server_id, user_id)
    if entreprise_nom:
        entreprise_data = load_entreprise(server_id, entreprise_nom)

        if entreprise_data["power"] >= quantite:
            entreprise_data["power"] -= quantite
            save_entreprise(server_id, entreprise_nom, entreprise_data)

            market_data = load_market_data(server_id, "elec")
            offre = {"entreprise": entreprise_nom, "quantite": quantite, "prix": prix}
            market_data[entreprise_nom] = offre
            save_market_data(server_id, "elec", market_data)

            await ctx.send(f"L'entreprise {entreprise_nom} propose de vendre {quantite} d'électricité à {prix}.")

        else:
            await ctx.send("L'entreprise n'a pas assez d'électricité à vendre.")
    else:
        await ctx.send("Vous n'êtes membre d'aucune entreprise.")


@electricity.command(name="list", description="Affiche l'éléctrité en vente")
async def electricity_list(ctx):
    server_id = str(ctx.guild.id)

    market_data = {}
    try:
        with open(f"{entreprise_folder}/{server_id}/market_elec.json", "r") as file:
            market_data = json.load(file)
    except FileNotFoundError:
        pass

    offres_triees = sorted(market_data.values(), key=lambda x: x["prix"])

    message = "**Offres d'Électricité en Vente :**\n"
    for offre in offres_triees:
        message += f"Entreprise : {offre['entreprise']}, Quantité : {offre['quantite']}, Prix : {offre['prix']}\n"

    await ctx.send(message)


@entreprise.command(description="Classement des entreprises d'électricité")
async def electricity_leaderboard(ctx):
    server_id = str(ctx.guild.id)

    entreprises_data = load_entreprises(server_id)

    entreprises_triees = sorted(entreprises_data, key=lambda x: x["power_gen"], reverse=True)[:10]

    message = "**Classement des Entreprises d'Électricité :**\n"
    for idx, entreprise in enumerate(entreprises_triees, start=1):
        message += f"{idx}. {entreprise['nom']} - Power Gen : {entreprise['power_gen']}\n"

    await ctx.send(message)


def load_entreprises(server_id):
    entreprises_data = []
    server_path = os.path.join(entreprise_folder, str(server_id))

    if os.path.exists(server_path):
        for filename in os.listdir(server_path):
            if filename.endswith(".json"):
                entreprise_path = os.path.join(server_path, filename)
                with open(entreprise_path, "r") as file:
                    entreprise_data = json.load(file)
                    entreprises_data.append(entreprise_data)
    return entreprises_data

async def consommation_electricite():
    await asyncio.sleep(3600)

    while True:
        for guild in bot.guilds:
            server_id = str(guild.id)
            entreprises_data = load_entreprises(server_id)

            for entreprise in entreprises_data:
                consommation = len(entreprise["inventaire"])

                if entreprise["power"] >= consommation:
                    entreprise["hash"] += consommation * random.randint(10, 30)

                entreprise["power"] -= consommation

                save_entreprise(server_id, entreprise["nom"], entreprise)

            
@electricity.command(name="buy", description="Acheter de l'électricité d'une autre entreprise")
async def electricity_buy(ctx, entreprise_nom, quantite: int):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    acheteur_nom = search_entreprise_by_user_id(server_id, user_id)
    if acheteur_nom:
        acheteur_data = load_entreprise(server_id, acheteur_nom)

        vendeur_data = load_entreprise(server_id, entreprise_nom)

        if vendeur_data and vendeur_data["power"] >= quantite:
            vendeur_data["power"] -= quantite
            acheteur_data["power"] += quantite

            save_entreprise(server_id, entreprise_nom, vendeur_data)
            save_entreprise(server_id, acheteur_nom, acheteur_data)

            await ctx.send(f"Vous avez acheté {quantite} d'électricité de l'entreprise {entreprise_nom}.")

        else:
            await ctx.send(f"L'entreprise {entreprise_nom} n'a pas assez d'électricité à vendre.")
    else:
        await ctx.send("Vous n'êtes membre d'aucune entreprise.")


@entreprise.command(description="Afficher les statistiques des serveurs")
async def servers_stats(ctx):
    server_id = str(ctx.guild.id)


    entreprise_data = load_entreprise(server_id, ctx.author.name)

    if entreprise_data["type"] != "serveurs":
        await ctx.send("Cette commande est réservée aux entreprises de type serveurs.")
        return

    message = f"**Statistiques des Serveurs de {ctx.author.name} :**\n"
    message += f"Serveurs en Service : {entreprise_data['power']}\n"
    message += f"Hash Actuel : {entreprise_data['hash']}\n"

    await ctx.send(message)

@entreprise.command(description="Acheter des serveurs pour l'entreprise")
async def servers_buy(ctx, quantite: int):
    server_id = str(ctx.guild.id)

    entreprise_data = load_entreprise(server_id, ctx.author.name)

    if entreprise_data["type"] != "serveurs":
        await ctx.send("Cette commande est réservée aux entreprises de type serveurs.")
        return

    cout = quantite * 50000

    if entreprise_data["argent"] < cout:
        await ctx.send("Vous n'avez pas assez d'argent pour acheter ces serveurs.")
        return

    entreprise_data["power"] += quantite
    entreprise_data["argent"] -= cout
    save_entreprise(server_id, ctx.author.name, entreprise_data)

    await ctx.send(f"Vous avez acheté {quantite} serveur(s) pour {cout}.")

@entreprise.command(description="Vendre des hash")
async def servers_sell(ctx, quantite: int):
    server_id = str(ctx.guild.id)

    entreprise_data = load_entreprise(server_id, ctx.author.name)

    if entreprise_data["type"] != "serveurs":
        await ctx.send("Cette commande est réservée aux entreprises de type serveurs.")
        return


    if entreprise_data["hash"] < quantite:
        await ctx.send("L'entreprise n'a pas assez de hash à vendre.")
        return

    revenu = quantite * random.randint(10, 30)

    entreprise_data["hash"] -= quantite
    entreprise_data["argent"] += revenu
    save_entreprise(server_id, ctx.author.name, entreprise_data)

    await ctx.send(f"Vous avez vendu {quantite} hash pour {revenu}.")

@entreprise.command(description="Afficher la boutique de serveurs")
async def servers_shop(ctx):
    message = "**Boutique de Serveurs :**\n"
    message += "1. Serveur - Prix : 50000\n"
    message += "Génère de la puissance de minage entre 10 - 30 hash\n"
    message += "Pour acheter un serveur, utilisez la commande /entreprise servers buy [quantité]."
    await ctx.send(message)