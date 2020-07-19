// This file was automatically added by xdn deploy.
// You should commit this file to source control.
module.exports = {
  backends: {
    origin: {
      domainOrIp: process.env.ORIGIN_DOMAIN_OR_IP || 'developer.moovweb.com',
      hostHeader: process.env.ORIGIN_HOST_HEADER || 'developer.moovweb.com',
    },
  },
}
