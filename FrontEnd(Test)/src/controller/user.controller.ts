import { Request, Response } from "express";
import { omit } from "lodash";
import { createUser } from "../Service/user.service";
import { createUserInput } from "../schema/user.schema";

export async function createUserHandler(
    req: Request<{}, {}, createUserInput["body"]>, 
    res: Response
    ){

    try {
        const user = await createUser(req.body)
        return res.send(omit(user.toJSON(), "password"));
    } catch (error: any) {
        console.log(error)
        return res.status(409).send(error.message)
    }
}