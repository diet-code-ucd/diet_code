import { Request, Response, NextFunction } from "express";
import { get } from "lodash";
import { verifyJwt } from "../utils/jwt.utils";

const deserializedUser = (req: Request, res: Response, next: NextFunction) => {
  const accessToken = get(req, "headers.authorization", "").replace(
    /^Bearer\s/,
    ""
  );

  if (!accessToken) {
    return next();
  }

  console.log("accessToke", accessToken);

  const { decoded, expired } = verifyJwt(accessToken);
  console.log("decoded", decoded);
  if (decoded) {
    res.locals.user = decoded;
    return next();
  }

  return next();
};

export default deserializedUser;
