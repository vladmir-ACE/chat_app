export class User{
    id:number;
    username:string;
    email:string;
    phone_number:string;
    password:string;
    username_or_email:string;
    img:string;

    constructor(){
        this.id=0;
        this.email="";
        this.img="";
        this.username="";
        this.phone_number="";
        this.password="";
        this.username_or_email="";
    }

}