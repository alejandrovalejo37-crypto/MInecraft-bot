function decideNextState() {
  const r = Math.random()

  if (r < 0.4) return 'IDLE'
  if (r < 0.75) return 'EXPLORE'

  return 'MOVE'
}

module.exports = {
  decideNextState
}
