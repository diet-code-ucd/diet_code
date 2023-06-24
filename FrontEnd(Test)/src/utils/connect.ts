import mongoose from "mongoose";
import config from "config"

async function connect(){
const dbUri = config.get<string>("dbUri")
//console.log(dbUri)

    try{
        await mongoose.connect(dbUri);
        console.log("Connected to DB");
    }catch(error){
        console.error("Cannot connect to DB");
        process.exit(1);
    }
}

export default connect;