const debugInformations = []

require("https")
  .createServer((_req, res) => {
    res.writeHead(200, { "Content-Type": "text/plain; charset=utf-8" })
    res.end(
      `"BotZone 専属ボット" is active now 👌\n\n--- Debug Information ---\n${debugInformations.join(
        "\n"
      )}`
    )
  })
  .listen(3000)

const { Client, MessageEmbed } = require("discord.js")
const client = new Client()
const config = require("./config.json")

client.on("debug", (info) => {
  debugInformations.push(info)
})

client.on("ready", () => {
  console.log("BotZone 起動確認")
  client.guilds.cache.forEach((guild) => {
    if (guild.id !== "589312721506271236") guild.leave()
  })

  client.channels.cache.get("657500911043870740").send(
    new MessageEmbed()
      .setTitle("BB起動 Log")
      .setColor("#0d6ce5")
      .setTimestamp()
      .setThumbnail(client.user.avatarURL())
      .setDescription("Bot が起動しました")
      .addFields([
        {
          name: "BotZone に参加している人数",
          value: client.users.cache.size,
        },
        {
          name: "BotZone のチャンネル数",
          value: client.channels.cache.size,
        },
      ])
  )

  client.user.setActivity("BotZone 専属Bot 機能考え中", { type: "PLAYING" })
})

client.on("message", async (message) => {
  if (!message.content.startsWith(config.prefix)) return

  const args = message.content.slice(config.prefix.length).split(" ")
  const command = args.shift().toLowerCase()

  if (command === "ping") message.channel.send(`WebSocket: ${client.ws.ping} ms\nMessage: ${new Date() - message.createdAt} ms`)
  if (command === "bot"){
    const Guild_bots = message.guild.members.cache.filter((user) => {
      return user.user.bot == true
    })
    message.channel.send(`BOT数: ${Guild_bots.size}`)
  }
  if (command === "create") {
    try {
      const privateChannelExists = message.guild.channels.cache.some(
        (channel) => channel.name === `room-${message.author.username}`
      )
      if (privateChannelExists) {
        message.delete()
        message.channel.send(
          new MessageEmbed().setTitle(
            `${message.author.tag} さん\nチャンネルは既に作成されています`
          )
        )
      } else {
        message.delete()
        const channel = await message.guild.channels.create(`room-${message.author.username}`, { type: "text" })
        await channel.setParent("619886010423312384")
        await channel.overwritePermissions([
          {
            id: message.author.id, //user
            allow: ["VIEW_CHANNEL", "SEND_MESSAGES"],
            type: "member"
          },
          {
            id: "589312721506271236", //everyone
            deny: ["VIEW_CHANNEL"],
          },
          {
            id: "602356923148402688", // BOT役職
            allow: ["VIEW_CHANNEL"],
            type: "role"
          },
        ])

        message.channel.send(
          new MessageEmbed().setTitle(
            `${message.author.tag} さん\nプライベートチャンネルを作成しました。`
          )
        )
      }
    } catch (err) {
      console.error(err)
    }
  }
})

client.login(process.env.DISCORD_BOT_TOKEN)
