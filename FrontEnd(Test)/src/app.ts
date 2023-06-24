import express from "express";
import config from "config";
import connect from "./utils/connect";
//import logger from "./utils/logger";
import routes from "./routes";
import exp from "constants";

import deserializedUser from "./middle/deserializedUser";

const app = express();
const port = config.get<number>("port");

app.use(express.json());
app.use(deserializedUser);

app.listen(port, async () => {
  console.log("App is running");

  await connect();
  routes(app);
});
