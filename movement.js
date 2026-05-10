const { goals } = require('mineflayer-pathfinder')
const { sleep } = require('./utils')

async function exploreRandomly(bot) {
  const x = bot.entity.position.x + (Math.random() - 0.5) * 30
  const z = bot.entity.position.z + (Math.random() - 0.5) * 30
  const y = bot.entity.position.y

  const goal = new goals.GoalNear(x, y, z, 1)

  bot.pathfinder.setGoal(goal)

  await randomLook(bot)

  await sleep(4000 + Math.random() * 5000)

  bot.pathfinder.stop()
}

async function moveToRandomNearby(bot) {
  const x = bot.entity.position.x + (Math.random() - 0.5) * 10
  const z = bot.entity.position.z + (Math.random() - 0.5) * 10
  const y = bot.entity.position.y

  bot.pathfinder.setGoal(new goals.GoalNear(x, y, z, 1))

  await sleep(2000 + Math.random() * 3000)

  bot.pathfinder.stop()
}

async function randomLook(bot) {
  const yaw = bot.entity.yaw + (Math.random() - 0.5)
  const pitch = (Math.random() - 0.5) * 0.4

  await bot.look(yaw, pitch, true)
}

module.exports = {
  exploreRandomly,
  moveToRandomNearby
}
