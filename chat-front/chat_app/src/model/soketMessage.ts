export class Smessage{
    id:string;
    sender_id:number;
    message:string;
    timestamp:string;
    receiver_id:number;

    constructor(){
        this.id="";
        this.sender_id=0;
        this.receiver_id=0;
        this.message="";
        this.timestamp="";
    }

}