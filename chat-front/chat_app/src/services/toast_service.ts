import { useToast } from "vue-toast-notification";

export class ToastService{

   public toast(type:string,message:string){
        useToast().open({type:type,message:message,position:'top-right',
        duration:3000,})
    }
}