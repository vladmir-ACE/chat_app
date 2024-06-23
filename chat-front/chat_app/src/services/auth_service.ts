export class AuthService{

    public setUserInfo(Info:any){
        for (const [key, value] of Object.entries(Info)) {

     
            localStorage.setItem(key, JSON.stringify(value));
            
          }
    }

    setToken(token:string){
        localStorage.setItem('token', token);
    }

    getToken(){
        return localStorage.getItem('token');
    }
    

    getUserInfo(info:string){
        return localStorage.getItem(info);
      }
    


}