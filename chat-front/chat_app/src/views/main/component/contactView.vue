<script  lang="ts">
import { api } from '@/api_env/api';
import { User } from '@/model/user';
import apiClient from '@/services/interceptor';
import { ToastService } from '@/services/toast_service';

import chatBoxView from '@/views/main/component/chatBoxView.vue';

import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import CKEditor from "@ckeditor/ckeditor5-vue"

import { Base64UploadAdapter } from '@ckeditor/ckeditor5-upload';

import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css';
import type { Poste } from '@/model/poste';




export default{
   components:{
    chatBoxView,
    ckeditor: CKEditor.component,
    QuillEditor
   },
    data(){
        return{
            contactList :[] as User[],
            UnknowContactList :[] as User[],
            postList :[] as Poste[],
            ownPostList :[] as Poste[],
            toast:new ToastService(),
            chatUser:new User(),
            findUser:new User(),
            curentUser:{
                // id=,
                email:localStorage.getItem("email"),
                username:localStorage.getItem("username"),
                //phone_number:localStorage.getItem("phone_number"),
                
            },
            // default profile img
            imageSrc: localStorage.getItem('img')?this.getSanitizedImageSrc(localStorage.getItem('img')):"/src/assets/images/users/user-dummy-img.jpg",
           
            search:{
                search:""
            },
            defaultImg:'/src/assets/images/users/user-dummy-img.jpg',

            // text editor editor data :
       
            editor: ClassicEditor,
             editorData: "",
             showContentdata:"<h1>HELLO</h1>",
             showModalTitle:"",
        }
    },
    methods:{

    getSanitizedImageSrc(imageUrl: string ) {
        return imageUrl.replace(/^["'](.+(?=["']$))["']$/, '$1'); // Remove leading and trailing quotes
      
    },

    getContact(){
    console.log("getfunction");
    apiClient.get(api.url+"user/contactes").then(
        (res)=>{
            console.log(res.data);
            this.contactList=res.data.data;

            console.log(this.contactList);
        },
        (error)=>{
            this.toast.toast("error","erreur pour la recuperation des contact");
            console.log(error);
        }
    );
    },

    getUnknowContact(){
    console.log("getUnknowfunction");
    apiClient.get(api.url+"user/unknown_contacts").then(
        (res)=>{
            console.log(res.data);
            this.UnknowContactList=res.data.data;

            console.log(this.UnknowContactList);
        },
        (error)=>{
            this.toast.toast("error","erreur pour la recuperation des contact unknow");
            console.log(error);
        }
    );
    },


    find(){
        console.log(this.search)
        apiClient.post(api.url+"user/search",this.search).then(
            (res)=>{
                this.findUser=res.data.user;
            },
            (error)=>{
                console.log(error)
                 this.toast.toast("error","user not found");
            }
        )
    },

    addContact(){
        apiClient.post(api.url+"user/contacte/add",{contact_id:this.findUser.id}).then(
            (res)=>{
                console.log(res);
                this.toast.toast("success","Utilisateur bien ajouté aux contacts");
                this.getContact();
                
            },
            (error)=>{
                console.log(error);
                this.toast.toast("error","erreur lors de l'ajout");
            }
        )
    },
    addUnknowContact(user:User){
        this.findUser=user;
        this.addContact();

    },
    // update profile 
    selectImage() {
        (this.$refs.fileInput as HTMLInputElement).click();
    },

    handleFileChange(event:any) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = e => {
          this.imageSrc = e.target!.result!.toString();

        };
        reader.readAsDataURL(file);
        this.uploadImage(file);
      }
    },

    uploadImage(file:any){
    const formData = new FormData();
      formData.append('img', file);
        apiClient.post(api.url+"user/upload_image",formData,{
            headers:{
                 'Content-Type': 'multipart/form-data'
            }
        }).then(
            (res)=>{
                if(res.data){
                    const newImgUrl=res.data.img;
                    localStorage.setItem('img',newImgUrl);
                    console.log(newImgUrl+ "uplaod console");
                    this.toast.toast("success","profile update");
                };
                console.log(res)
            },
           (error)=>{
            this.toast.toast("error","profile non mise a jour");
            console.log(error);
           }
        )


     },

     // text editor methodes 

     
      sendPostContent(){
        console.log(this.editorData);
        apiClient.post(api.url+"chat/add_post",{content:this.editorData}).then(
            (res)=>{
                console.log(res);
                this.toast.toast("success","Post Bien ajouté");
                this.getContact();
                
            },
            (error)=>{
                console.log(error);
                this.toast.toast("error","erreur lors de l'ajout");
            }
        )

      },

      getPostContact(){
        apiClient.get(api.url+"chat/contacts_posts").then(
        (res)=>{
            console.log(res.data);
            this.postList=res.data.data;

            console.log(this.UnknowContactList);
        },
        (error)=>{
            this.toast.toast("error","erreur pour la recuperation des  postes");
            console.log(error);
        }
    );

      },

      getOwnPost(){
        apiClient.get(api.url+"chat/own_post").then(
        (res)=>{
            console.log(res.data);
            this.ownPostList=res.data.data;

            console.log(this.ownPostList);
        },
        (error)=>{
            this.toast.toast("error","erreur pour la recuperation des  postes");
            console.log(error);
        }
    );

      },
      
       showPost(post:Poste){
        this.showContentdata=post.content;
        this.showModalTitle=post.contact.username;
        console.log(this.showContentdata);

      },

      deletePost(id:number){
        apiClient.delete(api.url+"chat/delete_post/"+id).then(
            (res)=>{
                this.toast.toast("success","Poste supprime");
                this.getOwnPost();
            },
            (error)=>{
                this.toast.toast("error","erreur pour la suppression du post");
            }
        );
      }

    },
    mounted(){
      this.getContact();
      this.getUnknowContact();
      this.getPostContact();
      this.getOwnPost();


    //   const editorElement = document.querySelector('#editor');
    // if (editorElement) {
    //   ClassicEditor.create(editorElement as HTMLElement, {
    //     plugins: [Base64UploadAdapter, /* ... */],
    //     toolbar: [/* ... */]
    //   }).then(editor => {
    //     console.log("Editor is ready", editor);
    //   }).catch(error => {
    //     console.error("There was a problem initializing the editor", error);
    //   });
    // }
  }
}

      


// variable



</script>

<template>
    <!-- start chat-leftsidebar -->
<div class="chat-leftsidebar">

<div class="tab-content">
    <!-- Start Profile tab-pane -->
    <div class="tab-pane" id="pills-user" role="tabpanel" aria-labelledby="pills-user-tab">
        <!-- Start profile content -->
        <div>
            <div class="user-profile-img">
                <img src="@/assets/images/small/img-4.jpg" class="profile-img" style="height: 160px;" alt="">
                <div class="overlay-content">
                    <div>
                        <div class="user-chat-nav p-2 ps-3">
    
                            <div class="d-flex w-100 align-items-center">
                                <div class="flex-grow-1">
                                    <h5 class="text-white mb-0">Mon Profile</h5>
                                </div>
                                <div class="flex-shrink-0">
                                    <div class="dropdown">
                                        <button class="btn nav-btn text-white dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                            <i class='bx bx-dots-vertical-rounded'></i>
                                        </button>
                                        <div class="dropdown-menu dropdown-menu-end">
                                            <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Info <i class="bx bx-info-circle ms-2 text-muted"></i></a>
                                            <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Setting <i class="bx bx-cog text-muted ms-2"></i></a>
                                            <div class="dropdown-divider"></div>
                                            <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Help <i class="bx bx-help-circle ms-2 text-muted"></i></a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="text-center p-3 p-lg-4 border-bottom pt-2 pt-lg-2 mt-n5 position-relative">
                <div class="mb-lg-3 mb-2">
                    
                    <img 
                            
                            :src=imageSrc!
                            class="rounded-circle avatar-lg img-thumbnail" 
                            alt="" 
                            @click="selectImage"
                        >
                        <input 
                            type="file" 
                            ref="fileInput" 
                            @change="handleFileChange" 
                            style="display: none"
                        />
                </div>

                <h5 class="font-size-16 mb-1 text-truncate">{{ curentUser.username }}</h5>
                <p class="text-muted font-size-14 text-truncate mb-0">{{curentUser.email}}</p>
            </div>
            <!-- End profile user -->

            
        </div>
        <!-- End profile content -->
    </div> 
    <!-- End Profile tab-pane -->

    <!-- Start chats tab-pane -->
    <div class="tab-pane " id="pills-chat" role="tabpanel" aria-labelledby="pills-chat-tab">
        <!-- Start chats content -->
        <div>
            <div class="px-4 pt-4">
                <div class="d-flex align-items-start">
                    <div class="flex-grow-1">
                        <h4 class="mb-4">Contact inconue</h4>
                    </div>
                    <div class="flex-shrink-0">
                        <div data-bs-toggle="tooltip" data-bs-trigger="hover" data-bs-placement="bottom" title="Add Contact">

                            <!-- Button trigger modal -->
                            <button type="button" class="btn btn-soft-primary btn-sm" data-bs-toggle="modal" data-bs-target="#addContact-exampleModal">
                                <i class="bx bx-plus"></i>
                            </button>
                        </div>
                    </div>
                </div>
                <form>
                    <div class="input-group mb-3">
                        <input type="text" class="form-control bg-light border-0 pe-0" id="serachChatUser" onkeyup="searchUser()" placeholder="Search here.." 
                        aria-label="Example text with button addon" aria-describedby="searchbtn-addon" autocomplete="off">
                        <button class="btn btn-light" type="button" id="searchbtn-addon"><i class='bx bx-search align-middle'></i></button>
                    </div>
                </form>

            </div> <!-- .p-4 -->

            <div class="chat-room-list" data-simplebar>
                <!-- Start chat-message-list -->
                

                <div class="chat-message-list">

                    <ul class="list-unstyled chat-list chat-user-list" id="favourite-users">                      
                    </ul>

                <div 
                    v-for="user in UnknowContactList" 
                    class="d-flex justify-content-between align-items-center mb-3 px-4 mt-4 font-size-11 text-muted bg-light rounded"
                    role="button"
                    @click="chatUser=user"
                    >
                    <img :src="user.img!=null?user.img:'/src/assets/images/users/user-dummy-img.jpg'" alt="Profile" class="rounded-circle me-3" width="40" height="40">
                    <span class=" text-center">{{user.email}}</span>
                   
                    <button type="button" class="btn btn-soft-primary btn-sm" 
                    @click="addUnknowContact(user)"
                    >
                                <i class="bx bx-plus"></i>
                     </button>

                    
                </div>
                    
                    
                </div>

               
                <!-- End chat-message-list -->
            </div>

        </div>
        <!-- Start chats content -->

        <!-- Start add group Modal -->
        <div class="modal fade" id="addgroup-exampleModal" tabindex="-1" role="dialog" aria-labelledby="addgroup-exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                <div class="modal-content modal-header-colored shadow-lg border-0">
                    <div class="modal-header">
                        <h5 class="modal-title text-white font-size-16" id="addgroup-exampleModalLabel">Create New Group</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close">
                        </button>
                    </div>
                    <div class="modal-body p-4">
                        <form>
                            <div class="mb-4">
                                <label for="addgroupname-input" class="form-label">Group Name</label>
                                <input type="text" class="form-control" id="addgroupname-input" placeholder="Enter Group Name">
                            </div>
                            <div class="mb-4">
                                <label class="form-label">Group Members</label>
                                <div class="mb-3">
                                    <button class="btn btn-light btn-sm" type="button" data-bs-toggle="collapse" data-bs-target="#groupmembercollapse" aria-expanded="false" aria-controls="groupmembercollapse">
                                        Select Members
                                    </button>
                                </div>

                                <div class="collapse" id="groupmembercollapse">
                                    <div class="card border">
                                        <div class="card-header">
                                            <h5 class="font-size-15 mb-0">Contacts</h5>
                                        </div>
                                        <div class="card-body p-2">
                                            <div data-simplebar style="max-height: 150px;">
                                                <div>
                                                    <div class="contact-list-title">
                                                        A
                                                    </div>

                                                    <ul class="list-unstyled contact-list">
                                                        <li>
                                                            <div class="form-check">
                                                                <input type="checkbox" class="form-check-input" id="memberCheck1" checked>
                                                                <label class="form-check-label" for="memberCheck1">Albert Rodarte</label>
                                                            </div>
                                                        </li>

                                                        <li>
                                                            <div class="form-check">
                                                                <input type="checkbox" class="form-check-input" id="memberCheck2">
                                                                <label class="form-check-label" for="memberCheck2">Allison Etter</label>
                                                            </div>
                                                        </li>
                                                    </ul>
                                                </div>

                                                <div>
                                                    <div class="contact-list-title">
                                                        C
                                                    </div>

                                                    <ul class="list-unstyled contact-list">
                                                        <li>
                                                            <div class="form-check">
                                                                <input type="checkbox" class="form-check-input" id="memberCheck3">
                                                                <label class="form-check-label" for="memberCheck3">Craig Smiley</label>
                                                            </div>
                                                        </li>

                                                    </ul>
                                                </div>

                                                <div>
                                                    <div class="contact-list-title">
                                                        D
                                                    </div>

                                                    <ul class="list-unstyled contact-list">
                                                        <li>
                                                            <div class="form-check">
                                                                <input type="checkbox" class="form-check-input" id="memberCheck4">
                                                                <label class="form-check-label" for="memberCheck4">Daniel Clay</label>
                                                            </div>
                                                        </li>

                                                    </ul>
                                                </div>

                                                <div>
                                                    <div class="contact-list-title">
                                                        I
                                                    </div>

                                                    <ul class="list-unstyled contact-list">
                                                        <li>
                                                            <div class="form-check">
                                                                <input type="checkbox" class="form-check-input" id="memberCheck5">
                                                                <label class="form-check-label" for="memberCheck5">Iris Wells</label>
                                                            </div>
                                                        </li>

                                                    </ul>
                                                </div>

                                                <div>
                                                    <div class="contact-list-title">
                                                        J
                                                    </div>

                                                    <ul class="list-unstyled contact-list">
                                                        <li>
                                                            <div class="form-check">
                                                                <input type="checkbox" class="form-check-input" id="memberCheck6">
                                                                <label class="form-check-label" for="memberCheck6">Juan Flakes</label>
                                                            </div>
                                                        </li>

                                                        <li>
                                                            <div class="form-check">
                                                                <input type="checkbox" class="form-check-input" id="memberCheck7">
                                                                <label class="form-check-label" for="memberCheck7">John Hall</label>
                                                            </div>
                                                        </li>

                                                        <li>
                                                            <div class="form-check">
                                                                <input type="checkbox" class="form-check-input" id="memberCheck8">
                                                                <label class="form-check-label" for="memberCheck8">Joy Southern</label>
                                                            </div>
                                                        </li>

                                                    </ul>
                                                </div>

                                                <div>
                                                    <div class="contact-list-title">
                                                        M
                                                    </div>

                                                    <ul class="list-unstyled contact-list">
                                                        <li>
                                                            <div class="form-check">
                                                                <input type="checkbox" class="form-check-input" id="memberCheck9">
                                                                <label class="form-check-label" for="memberCheck9">Michael Hinton</label>
                                                            </div>
                                                        </li>

                                                        <li>
                                                            <div class="form-check">
                                                                <input type="checkbox" class="form-check-input" id="memberCheck10">
                                                                <label class="form-check-label" for="memberCheck10">Mary Farmer</label>
                                                            </div>
                                                        </li>

                                                    </ul>
                                                </div>

                                                <div>
                                                    <div class="contact-list-title">
                                                        P
                                                    </div>

                                                    <ul class="list-unstyled contact-list">
                                                        <li>
                                                            <div class="form-check">
                                                                <input type="checkbox" class="form-check-input" id="memberCheck11">
                                                                <label class="form-check-label" for="memberCheck11">Phillis Griffin</label>
                                                            </div>
                                                        </li>

                                                    </ul>
                                                </div>

                                                <div>
                                                    <div class="contact-list-title">
                                                        R
                                                    </div>

                                                    <ul class="list-unstyled contact-list">
                                                        <li>
                                                            <div class="form-check">
                                                                <input type="checkbox" class="form-check-input" id="memberCheck12">
                                                                <label class="form-check-label" for="memberCheck12">Rocky Jackson</label>
                                                            </div>
                                                        </li>

                                                    </ul>
                                                </div>

                                                <div>
                                                    <div class="contact-list-title">
                                                        S
                                                    </div>

                                                    <ul class="list-unstyled contact-list">
                                                        <li>
                                                            <div class="form-check">
                                                                <input type="checkbox" class="form-check-input" id="memberCheck13">
                                                                <label class="form-check-label" for="memberCheck13">Simon Velez</label>
                                                            </div>
                                                        </li>

                                                    </ul>
                                                </div>
                                            </div>
                                        </div>
                
                                    </div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <label for="addgroupdescription-input" class="form-label">Description</label>
                                <textarea class="form-control" id="addgroupdescription-input" rows="3" placeholder="Enter Description"></textarea>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-link" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary">Create Groups</button>
                    </div>
                </div>
            </div>
        </div>
        <!-- End add group Modal -->
    </div>
    <!-- End chats tab-pane -->

    <!-- Start contacts tab-pane -->
    <div class="tab-pane show active" id="pills-contacts" role="tabpanel" aria-labelledby="pills-contacts-tab">
        <!-- Start Contact content -->
        <div>
            <div class="px-4 pt-4">
                <div class="d-flex align-items-start">
                    <div class="flex-grow-1">
                        <h4 class="mb-4">Contacts</h4>
                    </div>
                    <div class="flex-shrink-0">
                        <div data-bs-toggle="tooltip" data-bs-trigger="hover" data-bs-placement="bottom" title="Add Contact">

                            <!-- Button trigger modal -->
                            <button type="button" class="btn btn-soft-primary btn-sm" data-bs-toggle="modal" data-bs-target="#addContact-exampleModal2">
                                <i class="bx bx-plus"></i>
                            </button>
                        </div>
                    </div>
                </div>

                <form data-bs-toggle="modal" data-bs-target="#addContact-exampleModal2">
                    <div class="input-group mb-4">
                        <input type="text" class="form-control bg-light border-0 pe-0" id="searchContact" onkeyup="searchContacts()" placeholder="Search Contacts.." aria-label="Search Contacts..." 
                        aria-describedby="button-searchcontactsaddon" autocomplete="off">
                        <button class="btn btn-light" type="button" id="button-searchcontactsaddon"><i class='bx bx-search align-middle'></i></button>
                    </div>
                </form>
            </div>
            <!-- end p-4 -->

             
            <div class="chat-message-list chat-group-list">
                
                <div 
                    v-for="user in contactList" 
                    class="d-flex align-items-center mb-3 px-4 mt-4 font-size-11 text-muted bg-light rounded"
                    role="button"
                    @click="chatUser=user"
                    >
                    <img :src="user.img!=null?user.img:'/src/assets/images/users/user-dummy-img.jpg'" alt="Profile" class="rounded-circle me-3" width="40" height="40">
                    <span class=" text-center">{{user.email}}</span>
                    <div class="flex-shrink-0 ms-3">
                                <div class="dropdown">
                                    <a class="dropdown-toggle font-size-16 text-muted px-1" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <i class="bx bx-dots-horizontal-rounded"></i>
                                    </a>
                                    <div class="dropdown-menu dropdown-menu-end">
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Open <i class="bx bx-folder-open ms-2 text-muted"></i></a>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Edit <i class="bx bx-pencil ms-2 text-muted"></i></a>
                                        <div class="dropdown-divider"></div>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Delete <i class="bx bx-trash ms-2 text-muted"></i></a>
                                    </div>
                                </div>
                            </div>
                </div>
            </div>
            <!-- end contact lists -->
        </div>
        <!-- Start Contact content -->
    </div>
    <!-- End contacts tab-pane -->

    <!-- Start Poste/calls tab-pane -->
    <div class="tab-pane" id="pills-calls" role="tabpanel" aria-labelledby="pills-calls-tab">
        <!-- Start Contact content -->
        <div>
            <div class="px-4 pt-4">
                <div class="d-flex align-items-start">
                    <div class="flex-grow-1">
                        <h4 class="mb-4">POSTES</h4>
                    </div>
                    <div class="flex-shrink-0">
                        <div data-bs-toggle="tooltip" data-bs-trigger="hover" data-bs-placement="bottom" title="Add Poste">

                            <!-- Button trigger modal -->
                            <button type="button" class="btn btn-soft-primary btn-sm" data-bs-toggle="modal" data-bs-target="#addPost">
                                <i class="bx bx-plus"></i>
                            </button>
                        </div>
                    </div>
                </div>

                
            </div>
            <!-- end p-4 -->

            <!-- Start Poste lists -->
            <div class="chat-message-list chat-group-list">

                <h2>Mes Postes</h2>
                
                <div 
                    v-for="post in ownPostList" 
                    class="d-flex align-items-center mb-3 px-4 mt-4 font-size-11 text-muted bg-light rounded"
                    
                    @click="showPost(post)"
                    >
                    <img :src=post.contact.img alt="Profile" class="rounded-circle me-3" width="40" height="40" data-bs-toggle="modal" data-bs-target="#showPost">
                    <span class=" text-center">{{post.timestamp}}</span>
                    <div class="flex-shrink-0 ms-3">
                                <div class="dropdown">
                                    <a class="dropdown-toggle font-size-16 text-muted px-1" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <i class="bx bx-dots-horizontal-rounded"></i>
                                    </a>
                                    <div class="dropdown-menu dropdown-menu-end">
         
                                        <div class="dropdown-divider"></div>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" @click="deletePost(post.id)">Delete <i class="bx bx-trash ms-2 text-muted"></i></a>
                                    </div>
                                </div>
                    </div>
                    
                </div>
                <h2>Poste des contactes </h2>
                <div 
                    v-for="post in postList" 
                    class="d-flex align-items-center mb-3 px-4 mt-4 font-size-11 text-muted bg-light rounded"
                    
                    @click="showPost(post)"
                    >
                    <img :src=post.contact.img alt="Profile" class="rounded-circle me-3" width="40" height="40" data-bs-toggle="modal" data-bs-target="#showPost">                  
                    <span class=" text-center">{{post.timestamp}}</span>
                    
                    
                </div>
            </div>
            <!-- end Poste lists -->
        </div>
        <!-- Start Contact content -->
    </div>
    <!-- End calls tab-pane -->

    <!-- Start bookmark tab-pane -->
    <div class="tab-pane" id="pills-bookmark" role="tabpanel" aria-labelledby="pills-bookmark-tab">
        <!-- Start Contact content -->
        <div>
            <div class="px-4 pt-4">
                <div class="d-flex align-items-start">
                    <div class="flex-grow-1">
                        <h4 class="mb-3">Bookmark</h4>
                    </div>
                </div>
            </div>
            <!-- end p-4 -->

            <!-- Start contact lists -->
            <div class="chat-message-list chat-bookmark-list" data-simplebar>
                <ul class="list-unstyled chat-list">
                    <li>
                        <div class="d-flex align-items-center">
                            <div class="flex-shrink-0 avatar-xs ms-1 me-3">
                                <div class="avatar-title bg-primary-subtle text-primary rounded-circle">
                                    <i class="bx bx-file"></i>
                                </div>
                            </div>
                            <div class="flex-grow-1 overflow-hidden">
                                <h5 class="font-size-14 mb-1"><a href="#" class="text-truncate p-0">design-phase-1-approved.pdf</a></h5>
                                <p class="text-muted text-truncate font-size-13 mb-0">12.5 MB</p>
                            </div>

                            <div class="flex-shrink-0 ms-3">
                                <div class="dropdown">
                                    <a class="dropdown-toggle font-size-16 text-muted px-1" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <i class="bx bx-dots-horizontal-rounded"></i>
                                    </a>
                                    <div class="dropdown-menu dropdown-menu-end">
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Open <i class="bx bx-folder-open ms-2 text-muted"></i></a>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Edit <i class="bx bx-pencil ms-2 text-muted"></i></a>
                                        <div class="dropdown-divider"></div>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Delete <i class="bx bx-trash ms-2 text-muted"></i></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </li>
                    <li>
                        <div class="d-flex align-items-center">
                            <div class="flex-shrink-0 avatar-xs ms-1 me-3">
                                <div class="avatar-title bg-primary-subtle text-primary rounded-circle">
                                    <i class="bx bx-pin"></i>
                                </div>
                            </div>
                            <div class="flex-grow-1 overflow-hidden">
                                <h5 class="font-size-14 mb-1"><a href="#" class="text-truncate p-0">Bg Pattern</a></h5>
                                <p class="text-muted text-truncate font-size-13 mb-0">https://bgpattern.com/</p>
                            </div>

                            <div class="flex-shrink-0 ms-3">
                                <div class="dropdown">
                                    <a class="dropdown-toggle font-size-18 text-muted px-1" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <i class="bx bx-dots-horizontal-rounded"></i>
                                    </a>
                                    <div class="dropdown-menu dropdown-menu-end">
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Open <i class="bx bx-folder-open ms-2 text-muted"></i></a>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Edit <i class="bx bx-pencil ms-2 text-muted"></i></a>
                                        <div class="dropdown-divider"></div>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Delete <i class="bx bx-trash ms-2 text-muted"></i></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </li>
                    <li>
                        <div class="d-flex align-items-center">
                            <div class="flex-shrink-0 avatar-xs ms-1 me-3">
                                <div class="avatar-title bg-primary-subtle text-primary rounded-circle">
                                    <i class="bx bx-image"></i>
                                </div>
                            </div>
                            <div class="flex-grow-1 overflow-hidden">
                                <h5 class="font-size-14 mb-1"><a href="#" class="text-truncate p-0">Image-001.jpg</a></h5>
                                <p class="text-muted text-truncate font-size-13 mb-0">4.2 MB</p>
                            </div>

                            <div class="flex-shrink-0 ms-3">
                                <div class="dropdown">
                                    <a class="dropdown-toggle font-size-16 text-muted px-1" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <i class="bx bx-dots-horizontal-rounded"></i>
                                    </a>
                                    <div class="dropdown-menu dropdown-menu-end">
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Open <i class="bx bx-folder-open ms-2 text-muted"></i></a>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Edit <i class="bx bx-pencil ms-2 text-muted"></i></a>
                                        <div class="dropdown-divider"></div>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Delete <i class="bx bx-trash ms-2 text-muted"></i></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </li>
                    <li>
                        <div class="d-flex align-items-center">
                            <div class="flex-shrink-0 avatar-xs ms-1 me-3">
                                <div class="avatar-title bg-primary-subtle text-primary rounded-circle">
                                    <i class="bx bx-pin"></i>
                                </div>
                            </div>
                            <div class="flex-grow-1 overflow-hidden">
                                <h5 class="font-size-14 mb-1"><a href="#" class="text-truncate p-0">Images</a></h5>
                                <p class="text-muted text-truncate font-size-13 mb-0">https://images123.com/</p>
                            </div>

                            <div class="flex-shrink-0 ms-3">
                                <div class="dropdown">
                                    <a class="dropdown-toggle font-size-18 text-muted px-1" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <i class="bx bx-dots-horizontal-rounded"></i>
                                    </a>
                                    <div class="dropdown-menu dropdown-menu-end">
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Open <i class="bx bx-folder-open ms-2 text-muted"></i></a>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Edit <i class="bx bx-pencil ms-2 text-muted"></i></a>
                                        <div class="dropdown-divider"></div>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Delete <i class="bx bx-trash ms-2 text-muted"></i></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </li>
                    <li>
                        <div class="d-flex align-items-center">
                            <div class="flex-shrink-0 avatar-xs ms-1 me-3">
                                <div class="avatar-title bg-primary-subtle text-primary rounded-circle">
                                    <i class="bx bx-pin"></i>
                                </div>
                            </div>
                            <div class="flex-grow-1 overflow-hidden">
                                <h5 class="font-size-14 mb-1"><a href="#" class="text-truncate p-0">Bg Gradient</a></h5>
                                <p class="text-muted text-truncate font-size-13 mb-0">https://bggradient.com/</p>
                            </div>

                            <div class="flex-shrink-0 ms-3">
                                <div class="dropdown">
                                    <a class="dropdown-toggle font-size-18 text-muted px-1" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <i class="bx bx-dots-horizontal-rounded"></i>
                                    </a>
                                    <div class="dropdown-menu dropdown-menu-end">
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Open <i class="bx bx-folder-open ms-2 text-muted"></i></a>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Edit <i class="bx bx-pencil ms-2 text-muted"></i></a>
                                        <div class="dropdown-divider"></div>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Delete <i class="bx bx-trash ms-2 text-muted"></i></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </li>
                    <li>
                        <div class="d-flex align-items-center">
                            <div class="flex-shrink-0 avatar-xs ms-1 me-3">
                                <div class="avatar-title bg-primary-subtle text-primary rounded-circle">
                                    <i class="bx bx-image"></i>
                                </div>
                            </div>
                            <div class="flex-grow-1 overflow-hidden">
                                <h5 class="font-size-14 mb-1"><a href="#" class="text-truncate p-0">Image-012.jpg</a></h5>
                                <p class="text-muted text-truncate font-size-13 mb-0">3.1 MB</p>
                            </div>

                            <div class="flex-shrink-0 ms-3">
                                <div class="dropdown">
                                    <a class="dropdown-toggle font-size-16 text-muted px-1" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <i class="bx bx-dots-horizontal-rounded"></i>
                                    </a>
                                    <div class="dropdown-menu dropdown-menu-end">
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Open <i class="bx bx-folder-open ms-2 text-muted"></i></a>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Edit <i class="bx bx-pencil ms-2 text-muted"></i></a>
                                        <div class="dropdown-divider"></div>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Delete <i class="bx bx-trash ms-2 text-muted"></i></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </li>
                    <li>
                        <div class="d-flex align-items-center">
                            <div class="flex-shrink-0 avatar-xs ms-1 me-3">
                                <div class="avatar-title bg-primary-subtle text-primary rounded-circle">
                                    <i class="bx bx-file"></i>
                                </div>
                            </div>
                            <div class="flex-grow-1 overflow-hidden">
                                <h5 class="font-size-14 mb-1"><a href="#" class="text-truncate p-0">analytics dashboard.zip</a></h5>
                                <p class="text-muted text-truncate font-size-13 mb-0">6.7 MB</p>
                            </div>

                            <div class="flex-shrink-0 ms-3">
                                <div class="dropdown">
                                    <a class="dropdown-toggle font-size-16 text-muted px-1" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <i class="bx bx-dots-horizontal-rounded"></i>
                                    </a>
                                    <div class="dropdown-menu dropdown-menu-end">
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Open <i class="bx bx-folder-open ms-2 text-muted"></i></a>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Edit <i class="bx bx-pencil ms-2 text-muted"></i></a>
                                        <div class="dropdown-divider"></div>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Delete <i class="bx bx-trash ms-2 text-muted"></i></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </li>
                    <li>
                        <div class="d-flex align-items-center">
                            <div class="flex-shrink-0 avatar-xs ms-1 me-3">
                                <div class="avatar-title bg-primary-subtle text-primary rounded-circle">
                                    <i class="bx bx-image"></i>
                                </div>
                            </div>
                            <div class="flex-grow-1 overflow-hidden">
                                <h5 class="font-size-14 mb-1"><a href="#" class="text-truncate p-0">Image-031.jpg</a></h5>
                                <p class="text-muted text-truncate font-size-13 mb-0">4.2 MB</p>
                            </div>

                            <div class="flex-shrink-0 ms-3">
                                <div class="dropdown">
                                    <a class="dropdown-toggle font-size-16 text-muted px-1" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <i class="bx bx-dots-horizontal-rounded"></i>
                                    </a>
                                    <div class="dropdown-menu dropdown-menu-end">
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Open <i class="bx bx-folder-open ms-2 text-muted"></i></a>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Edit <i class="bx bx-pencil ms-2 text-muted"></i></a>
                                        <div class="dropdown-divider"></div>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Delete <i class="bx bx-trash ms-2 text-muted"></i></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </li>
                    <li>
                        <div class="d-flex align-items-center">
                            <div class="flex-shrink-0 avatar-xs ms-1 me-3">
                                <div class="avatar-title bg-primary-subtle text-primary rounded-circle">
                                    <i class="bx bx-file"></i>
                                </div>
                            </div>
                            <div class="flex-grow-1 overflow-hidden">
                                <h5 class="font-size-14 mb-1"><a href="#" class="text-truncate p-0">Changelog.txt</a></h5>
                                <p class="text-muted text-truncate font-size-13 mb-0">6.7 MB</p>
                            </div>

                            <div class="flex-shrink-0 ms-3">
                                <div class="dropdown">
                                    <a class="dropdown-toggle font-size-16 text-muted px-1" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <i class="bx bx-dots-horizontal-rounded"></i>
                                    </a>
                                    <div class="dropdown-menu dropdown-menu-end">
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Open <i class="bx bx-folder-open ms-2 text-muted"></i></a>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Edit <i class="bx bx-pencil ms-2 text-muted"></i></a>
                                        <div class="dropdown-divider"></div>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Delete <i class="bx bx-trash ms-2 text-muted"></i></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </li>
                    <li>
                        <div class="d-flex align-items-center">
                            <div class="flex-shrink-0 avatar-xs ms-1 me-3">
                                <div class="avatar-title bg-primary-subtle text-primary rounded-circle">
                                    <i class="bx bx-file"></i>
                                </div>
                            </div>
                            <div class="flex-grow-1 overflow-hidden">
                                <h5 class="font-size-14 mb-1"><a href="#" class="text-truncate p-0">Widgets.zip</a></h5>
                                <p class="text-muted text-truncate font-size-13 mb-0">6.7 MB</p>
                            </div>

                            <div class="flex-shrink-0 ms-3">
                                <div class="dropdown">
                                    <a class="dropdown-toggle font-size-16 text-muted px-1" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <i class="bx bx-dots-horizontal-rounded"></i>
                                    </a>
                                    <div class="dropdown-menu dropdown-menu-end">
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Open <i class="bx bx-folder-open ms-2 text-muted"></i></a>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Edit <i class="bx bx-pencil ms-2 text-muted"></i></a>
                                        <div class="dropdown-divider"></div>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Delete <i class="bx bx-trash ms-2 text-muted"></i></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </li>
                    <li>
                        <div class="d-flex align-items-center">
                            <div class="flex-shrink-0 avatar-xs ms-1 me-3">
                                <div class="avatar-title bg-primary-subtle text-primary rounded-circle">
                                    <i class="bx bx-image"></i>
                                </div>
                            </div>
                            <div class="flex-grow-1 overflow-hidden">
                                <h5 class="font-size-14 mb-1"><a href="#" class="text-truncate p-0">logo-light.png</a></h5>
                                <p class="text-muted text-truncate font-size-13 mb-0">4.2 MB</p>
                            </div>

                            <div class="flex-shrink-0 ms-3">
                                <div class="dropdown">
                                    <a class="dropdown-toggle font-size-16 text-muted px-1" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <i class="bx bx-dots-horizontal-rounded"></i>
                                    </a>
                                    <div class="dropdown-menu dropdown-menu-end">
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Open <i class="bx bx-folder-open ms-2 text-muted"></i></a>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Edit <i class="bx bx-pencil ms-2 text-muted"></i></a>
                                        <div class="dropdown-divider"></div>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Delete <i class="bx bx-trash ms-2 text-muted"></i></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </li>
                    <li>
                        <div class="d-flex align-items-center">
                            <div class="flex-shrink-0 avatar-xs ms-1 me-3">
                                <div class="avatar-title bg-primary-subtle text-primary rounded-circle">
                                    <i class="bx bx-image"></i>
                                </div>
                            </div>
                            <div class="flex-grow-1 overflow-hidden">
                                <h5 class="font-size-14 mb-1"><a href="#" class="text-truncate p-0">Image-2.jpg</a></h5>
                                <p class="text-muted text-truncate font-size-13 mb-0">3.1 MB</p>
                            </div>

                            <div class="flex-shrink-0 ms-3">
                                <div class="dropdown">
                                    <a class="dropdown-toggle font-size-16 text-muted px-1" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <i class="bx bx-dots-horizontal-rounded"></i>
                                    </a>
                                    <div class="dropdown-menu dropdown-menu-end">
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Open <i class="bx bx-folder-open ms-2 text-muted"></i></a>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Edit <i class="bx bx-pencil ms-2 text-muted"></i></a>
                                        <div class="dropdown-divider"></div>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Delete <i class="bx bx-trash ms-2 text-muted"></i></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </li>
                    <li>
                        <div class="d-flex align-items-center">
                            <div class="flex-shrink-0 avatar-xs ms-1 me-3">
                                <div class="avatar-title bg-primary-subtle text-primary rounded-circle">
                                    <i class="bx bx-file"></i>
                                </div>
                            </div>
                            <div class="flex-grow-1 overflow-hidden">
                                <h5 class="font-size-14 mb-1"><a href="#" class="text-truncate p-0">Landing-A.zip</a></h5>
                                <p class="text-muted text-truncate font-size-13 mb-0">6.7 MB</p>
                            </div>

                            <div class="flex-shrink-0 ms-3">
                                <div class="dropdown">
                                    <a class="dropdown-toggle font-size-16 text-muted px-1" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <i class="bx bx-dots-horizontal-rounded"></i>
                                    </a>
                                    <div class="dropdown-menu dropdown-menu-end">
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Open <i class="bx bx-folder-open ms-2 text-muted"></i></a>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Edit <i class="bx bx-pencil ms-2 text-muted"></i></a>
                                        <div class="dropdown-divider"></div>
                                        <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Delete <i class="bx bx-trash ms-2 text-muted"></i></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </li>

                </ul>
            </div>
            <!-- end contact lists -->
        </div>
        <!-- Start Contact content -->
    </div>
    <!-- End bookmark tab-pane -->
    
    <!-- Start settings tab-pane -->
    <div class="tab-pane" id="pills-setting" role="tabpanel" aria-labelledby="pills-setting-tab">
        <!-- Start Settings content -->
        <div>
            <div class="user-profile-img">
                <img src="@/assets/images/small/img-4.jpg" class="profile-img profile-foreground-img" style="height: 160px;" alt="">
                <div class="overlay-content">
                    <div>
                        <div class="user-chat-nav p-3">
    
                            <div class="d-flex w-100 align-items-center">
                                <div class="flex-grow-1">
                                    <h5 class="text-white mb-0">Paramettre</h5>
                                </div>
                                <div class="flex-shrink-0">
                                    <div class="avatar-xs p-0 rounded-circle profile-photo-edit" data-bs-toggle="tooltip" data-bs-trigger="hover" data-bs-placement="bottom" title="Change Background">
                                        <input id="profile-foreground-img-file-input" type="file" class="profile-foreground-img-file-input" >
                                        <label for="profile-foreground-img-file-input" class="profile-photo-edit avatar-xs">
                                            <span class="avatar-title rounded-circle bg-light text-body">
                                                <i class="bx bxs-pencil"></i>
                                            </span>
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="text-center p-3 p-lg-4 border-bottom pt-2 pt-lg-2 mt-n5 position-relative">
                <div class="mb-3 profile-user">
                    <img :src=imageSrc class="rounded-circle avatar-lg img-thumbnail user-profile-image" alt="user-profile-image">
                    <div class="avatar-xs p-0 rounded-circle profile-photo-edit">
                        <input id="profile-img-file-input" type="file" class="profile-img-file-input" >
                        <label for="profile-img-file-input" class="profile-photo-edit avatar-xs">
                            <span class="avatar-title rounded-circle bg-light text-body">
                                <i class="bx bxs-camera"></i>
                            </span>
                        </label>
                    </div>
                </div>

                <h5 class="font-size-16 mb-1 text-truncate"></h5>

                <div class="dropdown d-inline-block">
                    <a class="text-muted dropdown-toggle d-block" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        <i class="bx bxs-circle text-success font-size-10 align-middle"></i> Active <i class="mdi mdi-chevron-down"></i>
                    </a>

                    <div class="dropdown-menu">
                        <a class="dropdown-item" href="#"><i class="bx bxs-circle text-success font-size-10 me-1 align-middle"></i> Active</a>
                        <a class="dropdown-item" href="#"><i class="bx bxs-circle text-warning font-size-10 me-1 align-middle"></i> Away</a>
                        <a class="dropdown-item" href="#"><i class="bx bxs-circle text-danger font-size-10 me-1 align-middle"></i> Do not disturb</a>
                    </div>
                </div>


            </div>
            <!-- End profile user -->

            <!-- Start User profile description -->
            <div class="user-setting" data-simplebar>
                <div id="settingprofile" class="accordion accordion-flush">
                    <div class="accordion-item">
                        <div class="accordion-header" id="headerpersonalinfo">
                            <button class="accordion-button font-size-14 fw-medium" type="button" data-bs-toggle="collapse" data-bs-target="#personalinfo" aria-expanded="true" aria-controls="personalinfo">
                                <i class="bx bxs-user text-muted me-3"></i>Info Personelle
                            </button>
                        </div>
                        <div id="personalinfo" class="accordion-collapse collapse show" aria-labelledby="headerpersonalinfo" data-bs-parent="#settingprofile">
                            <div class="accordion-body">
                                <div class="float-end">
                                    <button type="button" class="btn btn-soft-primary btn-sm"><i class="bx bxs-pencil align-middle"></i></button>
                                </div>

                                <div>
                                    <p class="text-muted mb-1">UserName</p>
                                    <h5 class="font-size-14">{{curentUser.username}}</h5>
                                </div>

                                <div class="mt-4">
                                    <p class="text-muted mb-1">Email</p>
                                    <h5 class="font-size-14">{{curentUser.email}}</h5>
                                </div>

                                
                            </div>
                        </div>
                    </div>
                    <!-- end personal info card -->

                    <div class="accordion-item">
                        <div class="accordion-header" id="headerthemes">
                            <button class="accordion-button font-size-14 fw-medium collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapsethemes" aria-expanded="false" aria-controls="collapsethemes">
                                <i class="bx bxs-adjust-alt text-muted me-3"></i> Themes
                            </button>
                        </div>
                        <div id="collapsethemes" class="accordion-collapse collapse" aria-labelledby="headerthemes" data-bs-parent="#settingprofile">
                            <div class="accordion-body">
                                <div>
                                    <h5 class="mb-3 font-size-11 text-muted text-uppercase">Choose Theme Color :</h5>
                                    <div class="d-flex align-items-center flex-wrap gap-2 theme-btn-list theme-color-list">
                                        <div class="form-check">
                                            <input class="form-check-input theme-color" type="radio" value="0" name="bgcolor-radio" id="bgcolor-radio1" >
                                            <label class="form-check-label avatar-xs" for="bgcolor-radio1">
                                                <span class="avatar-title bg-primary-custom rounded-circle theme-btn bgcolor-radio1"></span>
                                            </label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input theme-color" type="radio" value="1" name="bgcolor-radio" id="bgcolor-radio2">
                                            <label class="form-check-label avatar-xs" for="bgcolor-radio2">
                                                <span class="avatar-title bg-info rounded-circle theme-btn bgcolor-radio2"></span>
                                            </label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input theme-color" type="radio" value="2" name="bgcolor-radio" id="bgcolor-radio4">
                                            <label class="form-check-label avatar-xs" for="bgcolor-radio4">
                                                <span class="avatar-title bg-purple rounded-circle theme-btn bgcolor-radio4"></span>
                                            </label>
                                        </div>
                
                                        <div class="form-check">
                                            <input class="form-check-input theme-color" type="radio" value="3" name="bgcolor-radio" id="bgcolor-radio5">
                                            <label class="form-check-label avatar-xs" for="bgcolor-radio5">
                                                <span class="avatar-title bg-pink rounded-circle theme-btn bgcolor-radio5"></span>
                                            </label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input theme-color" type="radio" value="4" name="bgcolor-radio" id="bgcolor-radio6">
                                            <label class="form-check-label avatar-xs" for="bgcolor-radio6">
                                                <span class="avatar-title bg-danger rounded-circle theme-btn bgcolor-radio6"></span>
                                            </label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input theme-color" type="radio" value="5" name="bgcolor-radio" id="bgcolor-radio7">
                                            <label class="form-check-label avatar-xs" for="bgcolor-radio7">
                                                <span class="avatar-title bg-secondary rounded-circle theme-btn bgcolor-radio7"></span>
                                            </label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input theme-color" type="radio" value="6" name="bgcolor-radio" id="bgcolor-radio8" checked>
                                            <label class="form-check-label avatar-xs light-background" for="bgcolor-radio8">
                                                <span class="avatar-title bg-light rounded-circle theme-btn bgcolor-radio8"></span>
                                            </label>
                                        </div>
                                    </div>
                                </div>

                                <div class="mt-4 pt-2">
                                    <h5 class="mb-3 font-size-11 text-muted text-uppercase">Choose Theme Image :</h5>
                                    <div class="d-flex align-items-center flex-wrap gap-2 theme-btn-list theme-btn-list-img">
                                        <div class="form-check">
                                            <input class="form-check-input theme-img" type="radio" name="bgimg-radio" id="bgimg-radio1">
                                            <label class="form-check-label avatar-xs" for="bgimg-radio1">
                                                <span class="avatar-title bg-pattern-1 rounded-circle theme-btn bgimg-radio1"></span>
                                            </label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input theme-img" type="radio" name="bgimg-radio" id="bgimg-radio2">
                                            <label class="form-check-label avatar-xs" for="bgimg-radio2">
                                                <span class="avatar-title bg-pattern-2 rounded-circle theme-btn bgimg-radio2"></span>
                                            </label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input theme-img" type="radio" name="bgimg-radio" id="bgimg-radio3">
                                            <label class="form-check-label avatar-xs" for="bgimg-radio3">
                                                <span class="avatar-title bg-pattern-3 rounded-circle theme-btn bgimg-radio3"></span>
                                            </label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input theme-img" type="radio" name="bgimg-radio" id="bgimg-radio4">
                                            <label class="form-check-label avatar-xs" for="bgimg-radio4">
                                                <span class="avatar-title bg-pattern-4 rounded-circle theme-btn bgimg-radio4"></span>
                                            </label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input theme-img" type="radio" name="bgimg-radio" id="bgimg-radio5" checked>
                                            <label class="form-check-label avatar-xs" for="bgimg-radio5">
                                                <span class="avatar-title bg-pattern-5 rounded-circle theme-btn bgimg-radio5"></span>
                                            </label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input theme-img" type="radio" name="bgimg-radio" id="bgimg-radio6">
                                            <label class="form-check-label avatar-xs" for="bgimg-radio6">
                                                <span class="avatar-title bg-pattern-6 rounded-circle theme-btn bgimg-radio6"></span>
                                            </label>
                                        </div>
                
                                        <div class="form-check">
                                            <input class="form-check-input theme-img" type="radio" name="bgimg-radio" id="bgimg-radio7">
                                            <label class="form-check-label avatar-xs" for="bgimg-radio7">
                                                <span class="avatar-title bg-pattern-7 rounded-circle theme-btn bgimg-radio7"></span>
                                            </label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input theme-img" type="radio" name="bgimg-radio" id="bgimg-radio8">
                                            <label class="form-check-label avatar-xs" for="bgimg-radio8">
                                                <span class="avatar-title bg-pattern-8 rounded-circle theme-btn bgimg-radio8"></span>
                                            </label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input theme-img" type="radio" name="bgimg-radio" id="bgimg-radio9">
                                            <label class="form-check-label avatar-xs" for="bgimg-radio9">
                                                <span class="avatar-title bg-pattern-9 rounded-circle theme-btn bgimg-radio9"></span>
                                            </label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="accordion-item">
                        <div class="accordion-header" id="privacy1">
                            <button class="accordion-button font-size-14 fw-medium collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#privacy" aria-expanded="false" aria-controls="privacy">
                                <i class="bx bxs-lock text-muted me-3"></i>Privacy
                            </button>
                        </div>
                        <div id="privacy" class="accordion-collapse collapse" aria-labelledby="privacy1" data-bs-parent="#settingprofile">
                            <div class="accordion-body">
                                <ul class="list-group list-group-flush">
                                    <li class="list-group-item py-3 px-0 pt-0">
                                        <div class="d-flex align-items-center">
                                            <div class="flex-grow-1 overflow-hidden">
                                                <h5 class="font-size-13 mb-0 text-truncate">Profile photo</h5>
                                            </div>
                                            <div class="flex-shrink-0 ms-2">
                                                <select class="form-select form-select-sm">
                                                    <option value="Everyone" selected>Everyone</option>
                                                    <option value="Selected">Selected</option>
                                                    <option value="Nobody">Nobody</option>
                                                </select>
                                            </div>
                                        </div>
                                    </li>
                                    <li class="list-group-item py-3 px-0">
                                        <div class="d-flex align-items-center">
                                            <div class="flex-grow-1 overflow-hidden">
                                                <h5 class="font-size-13 mb-0 text-truncate">Last seen</h5>

                                            </div>
                                            <div class="flex-shrink-0 ms-2">
                                                <div class="form-check form-switch">
                                                    <input type="checkbox" class="form-check-input" id="privacy-lastseenSwitch" checked>
                                                    <label class="form-check-label" for="privacy-lastseenSwitch"></label>
                                                </div>
                                            </div>
                                        </div>
                                    </li>
                                    <li class="list-group-item py-3 px-0">
                                        <div class="d-flex align-items-center">
                                            <div class="flex-grow-1 overflow-hidden">
                                                <h5 class="font-size-13 mb-0 text-truncate">Status</h5>
                                            </div>
                                            <div class="flex-shrink-0 ms-2">
                                                <select class="form-select form-select-sm">
                                                    <option value="Everyone" selected>Everyone</option>
                                                    <option value="Selected">Selected</option>
                                                    <option value="Nobody">Nobody</option>
                                                </select>
                                            </div>
                                        </div>
                                    </li>
                                    <li class="list-group-item py-3 px-0">
                                        <div class="d-flex align-items-center">
                                            <div class="flex-grow-1 overflow-hidden">
                                                <h5 class="font-size-13 mb-0 text-truncate">Read receipts</h5>
                                            </div>
                                            <div class="flex-shrink-0 ms-2">
                                                <div class="form-check form-switch">
                                                    <input type="checkbox" class="form-check-input" id="privacy-readreceiptSwitch" checked>
                                                    <label class="form-check-label" for="privacy-readreceiptSwitch"></label>
                                                </div>
                                            </div>
                                        </div>
                                    </li>
                                    <li class="list-group-item py-3 px-0 pb-0">
                                        <div class="d-flex align-items-center">
                                            <div class="flex-grow-1 overflow-hidden">
                                                <h5 class="font-size-13 mb-0 text-truncate">Groups</h5>

                                            </div>
                                            <div class="flex-shrink-0 ms-2">
                                                <select class="form-select form-select-sm">
                                                    <option value="Everyone" selected>Everyone</option>
                                                    <option value="Selected">Selected</option>
                                                    <option value="Nobody">Nobody</option>
                                                </select>
                                            </div>
                                        </div>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <!-- end privacy card -->

                    <div class="accordion-item">
                        <div class="accordion-header" id="headersecurity">
                            <button class="accordion-button font-size-14 fw-medium collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapsesecurity" aria-expanded="false" aria-controls="collapsesecurity">
                                <i class="bx bxs-check-shield text-muted me-3"></i> Security
                            </button>
                        </div>
                        <div id="collapsesecurity" class="accordion-collapse collapse" aria-labelledby="headersecurity" data-bs-parent="#settingprofile">
                            <div class="accordion-body">
                                <ul class="list-group list-group-flush">
                                    <li class="list-group-item p-0">
                                        <div class="d-flex align-items-center">
                                            <div class="flex-grow-1 overflow-hidden">
                                                <h5 class="font-size-13 mb-0 text-truncate">Show security notification</h5>

                                            </div>
                                            <div class="flex-shrink-0 ms-2">
                                                <div class="form-check form-switch">
                                                    <input type="checkbox" class="form-check-input" id="security-notificationswitch">
                                                    <label class="form-check-label" for="security-notificationswitch"></label>
                                                </div>
                                            </div>
                                        </div>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <!-- end security card -->



                    <div class="accordion-item">
                        <div class="accordion-header" id="headerhelp">
                            <button class="accordion-button font-size-14 fw-medium collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapsehelp" aria-expanded="false" aria-controls="collapsehelp">
                                <i class="bx bxs-help-circle text-muted me-3"></i> Help
                            </button>
                        </div>
                        <div id="collapsehelp" class="accordion-collapse collapse" aria-labelledby="headerhelp" data-bs-parent="#settingprofile">
                            <div class="accordion-body">
                                <ul class="list-group list-group-flush">
                                    <li class="list-group-item py-3 px-0 pt-0">
                                        <h5 class="font-size-13 mb-0"><a href="#" class="text-body d-block">FAQs</a></h5>
                                    </li>
                                    <li class="list-group-item py-3 px-0">
                                        <h5 class="font-size-13 mb-0"><a href="#" class="text-body d-block">Contact</a></h5>
                                    </li>
                                    <li class="list-group-item py-3 px-0 pb-0">
                                        <h5 class="font-size-13 mb-0"><a href="#" class="text-body d-block">Terms & Privacy policy</a></h5>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- end profile-setting-accordion -->
            </div>
            <!-- End User profile description -->
        </div>
        <!-- Start Settings content -->
    </div>
    <!-- End settings tab-pane -->
</div>
<!-- end tab content -->
</div>
<!-- end chat-leftsidebar -->

<!-- chatbox view-->

<chatBoxView :user="chatUser"/>


<!--modal for search contact -->
<!-- Start Add contact Modal -->
<div class="modal fade" id="addContact-exampleModal2" tabindex="-1" role="dialog" aria-labelledby="addContact-exampleModalLabel2" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content modal-header-colored shadow-lg border-0">
            <div class="modal-header">
                <h5 class="modal-title text-white font-size-16" id="addContact-exampleModalLabel2">Chercher un Contact</h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close">
                </button>
            </div>
            <form @submit.prevent="addContact">
            <div class="modal-body p-4">
               
                        <div class="input-group mb-4">
                                <input type="text"  v-model="search.search" @input="find" class="form-control bg-light border-0 pe-0" id="searchContact"  placeholder="Search Contacts.." 
                                aria-describedby="button-searchcontactsaddon" >
                                <button class="btn btn-light" type="button" id="button-searchcontactsaddon"><i class='bx bx-search align-middle'></i></button>
                            </div>
                
                 
                <h3 v-if="findUser.id==0" class="text text-center">Utilisateur pas trouvé</h3>

                <div 
                    v-if="findUser.id!=0"
                    class="d-flex align-items-center mb-3 px-4 mt-4 font-size-11 text-muted bg-light rounded"
                    role="button"
                    @click=""
                    >
                    <img :src="findUser.img!=null?findUser.img:'/src/assets/images/users/user-dummy-img.jpg'" alt="Profile" class="rounded-circle me-3" width="40" height="40">
                    <span class=" text-center" style="font-weight: bold; size:20px;">{{findUser.email}} / </span>
                    <span class=" text-center"style="font-weight: bold; size:20px;" >{{findUser.username}}  </span>
                    
                </div>

            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-link" data-bs-dismiss="modal">Close</button>
                <button type="submit" class="btn btn-primary">add</button>
            </div>
           </form>
        </div>
    </div>
</div>
<!-- End Add contact Modal -->


<!--Post modal -->

<div class="modal fade" id="addPost" tabindex="-1" role="dialog" aria-labelledby="addPost" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content modal-header-colored shadow-lg border-0">
            <div class="modal-header">
                <h5 class="modal-title text-white font-size-16" id="addPost">Ajouter un Post</h5>
                <button type="button"  class="btn-close btn-close-white" data-bs-dismiss="modal"  aria-label="Close">
                </button>
            </div>
          
            <div class="modal-body p-4">
               
                        
              <!--content here-->
              <QuillEditor v-model:content="editorData" theme="snow" toolbar="full" contentType="html" />
              

            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-link" data-bs-dismiss="modal">Close</button>
                <button  @click="sendPostContent()" class="btn btn-primary">add</button>
            </div>
          
        </div>
    </div>
</div>
<!--End post Modal-->


<!-- show post modal -->
<div class="modal fade" id="showPost" tabindex="-1" role="dialog" aria-labelledby="showPost" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content modal-header-colored shadow-lg border-0">
            <div class="modal-header">
                <h5 class="modal-title text-white font-size-16" id="addPost">Poste de : {{showModalTitle }}</h5>
                <button type="button"  class="btn-close btn-close-white" data-bs-dismiss="modal"  aria-label="Close">
                </button>
            </div>
          
            <div class="modal-body p-4">
               
              
                <div v-html="showContentdata"></div>


            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-link" data-bs-dismiss="modal">Close</button>
               
            </div>
          
        </div>
    </div>
</div>
<!-- end show  -->


</template>