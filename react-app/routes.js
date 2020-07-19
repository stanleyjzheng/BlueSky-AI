const { Router } = require('@xdn/core/router')

// const ONE_HOUR = 60 * 60
// const ONE_DAY = 24 * ONE_HOUR

module.exports = new Router()

  // Here is an example where we cache api/* at the edge but prevent caching in the browser
  // .match('/api/*path', ({ proxy, cache }) => {
  //   cache({
  //     edge: {
  //       maxAgeSeconds: ONE_DAY,
  //       staleWhilRevalidateSeconds: ONE_HOUR,
  //     },
  //     browser: {
  //       maxAgeSeconds: 0,
  //       serviceWorkerSeconds: ONE_DAY,
  //     },
  //   })
  //   proxy('origin')
  // })

  // send any unmatched request to origin
  .fallback(({ proxy }) => proxy('origin'))
