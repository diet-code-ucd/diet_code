import { Request, Response } from "express";
import { validatePassword } from "../Service/user.service";
import { createSession, findSessions } from "../Service/session.service";
import config from "config";
import { signJwt } from "../utils/jwt.utils";

export async function createUserSessionHandler(req: Request, res: Response) {
  //Validate the User password

  const user = await validatePassword(req.body);

  if (!user) {
    return res.status(401).send("Invalid Username or password");
  }

  //Create a session
  const session = await createSession(user._id, req.get("user-agent") || "");

  //Create a access token
  const accessToken = signJwt(
    { ...user, session: session._id },
    { expiresIn: config.get("accessTokenTtl") }
  );

  //create a refresh token

  const refreshToken = signJwt(
    { ...user, session: session._id },
    { expiresIn: config.get("accessTokenTtl") }
  );

  //returtn access & refresh Token

  return res.send({ accessToken, refreshToken });
}

export async function getUserSessionHandler(req: Request, res: Response) {
  const userId = res.locals.user._id;

  const session = await findSessions({ user: userId, valid: true });

  return res.send(session);
}
