async def get_prefix(ctx):
    if ctx.guild == None:
        return "k!"
    else:
        mongo_url = "mongodb+srv://admin:4n0tS0g00D1ne@sentry.z5zvv.mongodb.net/Reliex?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["Sentry"]
        collection = db["prefixes"]
        if collection.count_documents({"_id": ctx.guild.id}) == 0:
            collection.insert_one({"_id": ctx.guild.id, "prefix": "k!"})
        pref = collection.find_one({"_id": ctx.guild.id})
        prefix = pref["prefix"]
        return prefix
