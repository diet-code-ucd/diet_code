//import {DocumentDefinition} from 'mongoose'

import { get } from "config";
import userModel, { UserDocument, UserInput } from "../models/user.model";
import { omit } from "lodash";

export async function createUser(input: UserInput) {
  try {
    return await userModel.create(input);
  } catch (error: any) {
    throw new Error(error);
  }
}
export async function validatePassword({
  email,
  password,
}: {
  email: string;
  password: string;
}) {
  const user = await userModel.findOne({ email });

  if (!user) {
    return false;
  }

  const isValid = await user.comparePassword(password);

  if (!isValid) {
    return false;
  }

  return user;
}
