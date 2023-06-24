import { type } from "os";
import { TypeOf, object, string } from "zod";

export const createUserSchema = object({
  body: object({
    name: string({
      required_error: "Name is required",
    }),
    password: string({
      required_error: "Password is required",
    }).min(6, "password is too short, min 6 chars"),
    passwordConfirmation: string({
      required_error: "Password Confirmattion is required",
    }),
    email: string({
      required_error: "Email is required",
    }).email("Not a valid Email"),
  }).refine((data) => data.password === data.passwordConfirmation, {
    message: "password do not match",
    path: ["passwordConfirmation"],
  }),
});

export type createUserInput = TypeOf<typeof createUserSchema>;
