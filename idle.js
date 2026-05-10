const { sleep } = require('./utils')

async function idleBehavior(bot) {
  const iterations = Math.floor(Math.random() * 5) + 2

  for (let i = 0; i < iterations; i++) {
    const yaw = bot.entity.yaw + (Math.random() - 0.5)
    const pitch = (Math.random() - 0.5) * 0.5

    await bot.look(yaw, pitch, true)

    if (Math.random() > 0.7) {
      bot.setControlState('jump', true)

      await sleep(100)

      bot.setControlState('jump', false)
    }

    await sleep(1000 + Math.random() * 2000)
  }
}

module.exports = {
  idleBehavior
}
