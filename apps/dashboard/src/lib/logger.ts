import pino from 'pino';

const env = process.env.NODE_ENV;
const isProduction = env === 'production';

const logger = pino({
  level: isProduction ? "info" : "debug",
  base: { env },
});

export default logger;
