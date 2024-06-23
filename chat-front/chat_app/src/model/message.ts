export class Message{
    id:number;
    sender_id:number;
    content:string;
    timestamp:string;
    receiver_id:number;

    constructor(){
        this.id=0;
        this.sender_id=0;
        this.receiver_id=0;
        this.content="";
        this.timestamp="";
    }

}