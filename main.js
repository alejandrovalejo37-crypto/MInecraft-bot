const mineflayer = require('mineflayer')
const { pathfinder, Movements } = require('mineflayer-pathfinder')

const { decideNextState } = require('./brain')
const { exploreRandomly, moveToRandomNearby } = require('./movement')
const { idleBehavior } = require('./idle')
const { sleep } = require('./utils')

const bot = mineflayer.createBot({
  host: 'localhost',
  port: 25565,
  username: 'NPC_Bot'
})

bot.loadPlugin(pathfinder)

let state = 'IDLE'

bot.once('spawn', async () => {
  const mcData = require('minecraft-data')(bot.version)

  const movements = new Movements(bot, mcData)

  bot.pathfinder.setMovements(movements)

  console.log('NPC conectado')

  while (true) {
    state = decideNextState()

    console.log('Estado:', state)

    switch (state) {
      case 'IDLE':
        await idleBehavior(bot)
        break

      case 'EXPLORE':
        await exploreRandomly(bot)
        break

      case 'MOVE':
        await moveToRandomNearby(bot)
        break
    }

    await sleep(1000 + Math.random() * 3000)
  }
})
