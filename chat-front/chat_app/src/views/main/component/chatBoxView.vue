<script lang="ts">
import { api } from '@/api_env/api';
import { Message } from '@/model/message';

import { User } from '@/model/user';
import apiClient from '@/services/interceptor';
import { ToastService } from '@/services/toast_service';


export default {
    name: 'ChatBox',
    props: {
        user: {
            type: Object as () => User,
            required: true
        }
    },
    data() {
        return {
            list_messages_send_to_user: [] as Message[],
            list_messages_recieve_for_user: [] as Message[],
            toast: new ToastService(),
            sendMessage:new Message(),
            

            

        }
    },
    computed: {
    sortedMessages() {
      // Combine and sort messages by timestamp
      return [...this.list_messages_send_to_user, ...this.list_messages_recieve_for_user].sort((a, b) => {
        return new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime();
      });
    }
  },
    methods: {

        getAllMeseageSendTo() {
            if (this.user.id != 0) {
                console.log(this.user.id);
                apiClient.get(api.url + "chat/messages/send_to/" + this.user.id).then(
                    (res) => {
                        console.log("liste message envoyé")
                        console.log(res.data);
                        this.list_messages_send_to_user = res.data.data;

                        console.log(this.list_messages_send_to_user);
                    },
                    (error) => {
                        this.toast.toast("error", "erreur pour la recuperation des message envoyé");
                        console.log(error);
                    }
                );
            }


        },

        getAllMeseageRecieveTo() {
            if (this.user.id != 0) {
                console.log(this.user.id);
                apiClient.get(api.url + "chat/messages/recieve_to/" + this.user.id).then(
                    (res) => {
                        console.log("liste message recus")
                        console.log(res.data);
                        this.list_messages_recieve_for_user = res.data.data;

                        console.log(this.list_messages_recieve_for_user);
                    },
                    (error) => {
                        this.toast.toast("error", "erreur pour la recuperation des message recus");
                        console.log(error);
                    }
                );
            }


        },

        load() {
            this.getAllMeseageRecieveTo();
            this.getAllMeseageSendTo();
        },

        // send message

        sendContent(){
           this.sendMessage.receiver_id=this.user.id;
           console.log(this.sendMessage);
            apiClient.post(api.url + "chat/send_message" , this.sendMessage).then(
                    (res) => {                     
                        console.log(res.data);
                        this.toast.toast("success", "Message envoyé");    
                        // reload data
                        this.load();
                      
                    },
                    (error) => {
                        this.toast.toast("error", "erreur pendant l'envoie du message ");
                        console.log(error);
                    }
                );

        },
        // send Message with socket io
       

    },
    mounted() {
        this.load();
    },
    watch: {
        user: {
            handler(newUser, oldUser) {
                if (newUser && oldUser && newUser.id !== oldUser.id) {
                    this.load(); // Appeler la fonction load lorsque la prop user change
                }
            },
            deep: true, // Si user est un objet complexe et que vous voulez détecter les changements profonds
            immediate: true // Appeler immédiatement le watcher après le montage du composant
        }
    },
    

}

</script>

<template>


    <!-- Start User chat -->
    <div class="user-chat w-100 overflow-hidden">
        <div class="user-chat-overlay"></div>

        <div class="chat-content d-lg-flex">
            <!-- start chat conversation section -->
            <div class="w-100 overflow-hidden position-relative" v-if="user.email != ''">
                <!-- conversation user -->
                <div id="users-chat" class="position-relative">
                    <!-- topbar -->
                    <div class="p-3 p-lg-4 user-chat-topbar">
                        <div class="row align-items-center">
                            <div class="col-sm-4 col-8">
                                <div class="d-flex align-items-center">
                                    <div class="flex-shrink-0 d-block d-lg-none me-3">
                                        <a href="javascript: void(0);" class="user-chat-remove font-size-18 p-1"><i
                                                class="bx bx-chevron-left align-middle"></i></a>
                                    </div>
                                    <div class="flex-grow-1 overflow-hidden">
                                        <div class="d-flex align-items-center">
                                            <div
                                                class="flex-shrink-0 chat-user-img online user-own-img align-self-center me-3 ms-0">
                                                <img src="@/assets/images/users/avatar-2.jpg"
                                                    class="rounded-circle avatar-sm" alt="">
                                                <span class="user-status"></span>
                                            </div>
                                            <div class="flex-grow-1 overflow-hidden">
                                                <h6 class="text-truncate mb-0 font-size-18"><a href="#"
                                                        class="user-profile-show text-reset">{{ user.email }}</a></h6>
                                                <p class="text-truncate text-muted mb-0"><small>{{ user.username
                                                        }}</small></p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-sm-8 col-4">
                                <ul class="list-inline user-chat-nav text-end mb-0">
                                    <li class="list-inline-item">
                                        <div class="dropdown">
                                            <button class="btn nav-btn dropdown-toggle" type="button"
                                                data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                <i class='bx bx-search'></i>
                                            </button>
                                            <div class="dropdown-menu p-0 dropdown-menu-end dropdown-menu-lg">
                                                <div class="search-box p-2">
                                                    <input type="text" class="form-control" placeholder="Search.."
                                                        id="searchChatMessage">
                                                </div>
                                            </div>
                                        </div>
                                    </li>

                                    <li class="list-inline-item d-none d-lg-inline-block me-2 ms-0">
                                        <button type="button" class="btn nav-btn" data-bs-toggle="modal"
                                            data-bs-target=".audiocallModal">
                                            <i class='bx bxs-phone-call'></i>
                                        </button>
                                    </li>

                                    <li class="list-inline-item d-none d-lg-inline-block me-2 ms-0">
                                        <button type="button" class="btn nav-btn" data-bs-toggle="modal"
                                            data-bs-target=".videocallModal">
                                            <i class='bx bx-video'></i>
                                        </button>
                                    </li>

                                    <li class="list-inline-item d-none d-lg-inline-block me-2 ms-0">
                                        <button type="button" class="btn nav-btn user-profile-show">
                                            <i class='bx bxs-info-circle'></i>
                                        </button>
                                    </li>

                                    <li class="list-inline-item">
                                        <div class="dropdown">
                                            <button class="btn nav-btn dropdown-toggle" type="button"
                                                data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                <i class='bx bx-dots-vertical-rounded'></i>
                                            </button>
                                            <div class="dropdown-menu dropdown-menu-end">
                                                <a class="dropdown-item d-flex justify-content-between align-items-center d-lg-none user-profile-show"
                                                    href="#">View Profile <i class="bx bx-user text-muted"></i></a>
                                                <a class="dropdown-item d-flex justify-content-between align-items-center d-lg-none"
                                                    href="#" data-bs-toggle="modal"
                                                    data-bs-target=".audiocallModal">Audio <i
                                                        class="bx bxs-phone-call text-muted"></i></a>
                                                <a class="dropdown-item d-flex justify-content-between align-items-center d-lg-none"
                                                    href="#" data-bs-toggle="modal"
                                                    data-bs-target=".videocallModal">Video <i
                                                        class="bx bx-video text-muted"></i></a>
                                                <a class="dropdown-item d-flex justify-content-between align-items-center"
                                                    href="#">Archive <i class="bx bx-archive text-muted"></i></a>
                                                <a class="dropdown-item d-flex justify-content-between align-items-center"
                                                    href="#">Muted <i class="bx bx-microphone-off text-muted"></i></a>
                                                <a class="dropdown-item d-flex justify-content-between align-items-center"
                                                    href="#">Delete <i class="bx bx-trash text-muted"></i></a>
                                            </div>
                                        </div>
                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="alert alert-warning alert-dismissible topbar-bookmark fade show p-1 px-3 px-lg-4 pe-lg-5 pe-5"
                            role="alert">
                            <div class="d-flex align-items-start bookmark-tabs">
                                <div class="tab-list-link">
                                    <a href="#" class="tab-links" data-bs-toggle="modal"
                                        data-bs-target=".pinnedtabModal"><i
                                            class="ri-pushpin-fill align-middle me-1"></i> 10 Pinned</a>
                                </div>
                                <div>
                                    <a href="#" class="tab-links border-0 px-3" data-bs-toggle="tooltip"
                                        data-bs-trigger="hover" data-bs-placement="bottom" title="Add Bookmark"><i
                                            class="ri-add-fill align-middle"></i></a>
                                </div>
                            </div>
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>

                    </div>
                    <!-- end chat user head -->

                    <!-- start chat conversation -->

                <div class="chat-conversation p-3 p-lg-4" id="chat-conversation" data-simplebar>
                    <ul class="list-unstyled chat-conversation-list" id="users-conversation">
                        <li v-for="(message, index) in sortedMessages" :key="index" :class=" message.receiver_id == user.id ?'chat-list right' : 'chat-list left'">
                            <div class="conversation-list">
                            <div class="user-chat-content">
                                <div class="ctext-wrap">
                                <div class="ctext-wrap-content">
                                    <p class="mb-0 ctext-content">{{ message.content }}</p>
                                </div>
                                <div class="dropdown align-self-start message-box-drop">
                                    <a class="dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    <i class="ri-more-2-fill"></i>
                                    </a>
                                    <div class="dropdown-menu">
                                    <a class="dropdown-item d-flex align-items-center justify-content-between delete-item" href="#">
                                        Delete <i class="bx bx-trash text-muted ms-2"></i>
                                    </a>
                                    </div>
                                </div>
                                </div>
                                <div class="conversation-name">
                                <small class="text-muted time">{{ message.timestamp }}</small>
                                <span class="text-success check-message-icon"><i class="bx bx-check"></i></span>
                                </div>
                            </div>
                            </div>
                        </li>

                         
                        </ul>
                </div>

                    <div class="alert alert-warning alert-dismissible copyclipboard-alert px-4 fade show "
                        id="copyClipBoard" role="alert">
                        message copied
                    </div>


                    <!-- end chat conversation end -->
                </div>

                <!-- conversation group -->
                <div id="channel-chat" class="position-relative">
                    <div class="p-3 p-lg-4 user-chat-topbar">
                        <div class="row align-items-center">
                            <div class="col-sm-4 col-8">
                                <div class="d-flex align-items-center">
                                    <div class="flex-shrink-0 d-block d-lg-none me-3">
                                        <a href="javascript: void(0);" class="user-chat-remove font-size-18 p-1"><i
                                                class="bx bx-chevron-left align-middle"></i></a>
                                    </div>
                                    <div class="flex-grow-1 overflow-hidden">
                                        <div class="d-flex align-items-center">
                                            <div
                                                class="flex-shrink-0 chat-user-img online user-own-img align-self-center me-3">
                                                <img src="@/assets/images/users/user-dummy-img.jpg"
                                                    class="rounded-circle avatar-sm" alt="">
                                            </div>
                                            <div class="flex-grow-1 overflow-hidden">
                                                <h6 class="text-truncate mb-0 font-size-18"><a href="#"
                                                        class="user-profile-show text-reset">Design Phase 2</a></h6>
                                                <p class="text-truncate text-muted mb-0"><small>24 Members</small></p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-sm-8 col-4">
                                <ul class="list-inline user-chat-nav text-end mb-0">
                                    <li class="list-inline-item">
                                        <div class="dropdown">
                                            <button class="btn nav-btn dropdown-toggle" type="button"
                                                data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                <i class='bx bx-search'></i>
                                            </button>
                                            <div class="dropdown-menu p-0 dropdown-menu-end dropdown-menu-lg">
                                                <div class="search-box p-2">
                                                    <input type="text" class="form-control" placeholder="Search..">
                                                </div>
                                            </div>
                                        </div>
                                    </li>

                                    <li class="list-inline-item d-none d-lg-inline-block me-2 ms-0">
                                        <button type="button" class="btn nav-btn user-profile-show">
                                            <i class='bx bxs-info-circle'></i>
                                        </button>
                                    </li>

                                    <li class="list-inline-item">
                                        <div class="dropdown">
                                            <button class="btn nav-btn dropdown-toggle" type="button"
                                                data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                <i class='bx bx-dots-vertical-rounded'></i>
                                            </button>
                                            <div class="dropdown-menu dropdown-menu-end">
                                                <a class="dropdown-item d-flex justify-content-between align-items-center d-lg-none user-profile-show"
                                                    href="#">View Profile <i class="bx bx-user text-muted"></i></a>
                                                <a class="dropdown-item d-flex justify-content-between align-items-center d-lg-none"
                                                    href="#" data-bs-toggle="modal"
                                                    data-bs-target=".audiocallModal">Audio <i
                                                        class="bx bxs-phone-call text-muted"></i></a>
                                                <a class="dropdown-item d-flex justify-content-between align-items-center d-lg-none"
                                                    href="#" data-bs-toggle="modal"
                                                    data-bs-target=".videocallModal">Video <i
                                                        class="bx bx-video text-muted"></i></a>
                                                <a class="dropdown-item d-flex justify-content-between align-items-center"
                                                    href="#">Archive <i class="bx bx-archive text-muted"></i></a>
                                                <a class="dropdown-item d-flex justify-content-between align-items-center"
                                                    href="#">Muted <i class="bx bx-microphone-off text-muted"></i></a>
                                                <a class="dropdown-item d-flex justify-content-between align-items-center"
                                                    href="#">Delete <i class="bx bx-trash text-muted"></i></a>
                                            </div>
                                        </div>
                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="alert alert-warning alert-dismissible topbar-bookmark fade show p-1 px-3 px-lg-4 pe-lg-5 pe-5"
                            role="alert">
                            <div class="d-flex align-items-start bookmark-tabs">
                                <div class="tab-list-link">
                                    <a href="#" class="tab-links" data-bs-toggle="modal"
                                        data-bs-target=".pinnedtabModal"><i
                                            class="ri-pushpin-fill align-middle me-1"></i> 10 Pinned</a>
                                </div>
                                <div>
                                    <a href="#" class="tab-links border-0 px-3" data-bs-toggle="tooltip"
                                        data-bs-trigger="hover" data-bs-placement="bottom" title="Add Bookmark"><i
                                            class="ri-add-fill align-middle"></i></a>
                                </div>
                            </div>
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>
                    </div>
                    <!-- end chat user head -->

                    <!-- start chat conversation -->


                    <!-- end chat conversation end -->
                </div>

                <!-- start chat input section -->
                <div class="position-relative">
                    <div class="chat-input-section p-3 p-lg-4">

                        <form @submit.prevent="sendContent" id="chatinput-form" enctype="multipart/form-data">
                            <div class="row g-0 align-items-center">
                                <div class="file_Upload"></div>
                                <div class="col-auto">
                                    <div class="chat-input-links me-md-2">
                                        <div class="links-list-item" data-bs-toggle="tooltip" data-bs-trigger="hover"
                                            data-bs-placement="top" title="More">
                                            <button type="button"
                                                class="btn btn-link text-decoration-none btn-lg waves-effect"
                                                data-bs-toggle="collapse" data-bs-target="#chatinputmorecollapse"
                                                aria-expanded="false" aria-controls="chatinputmorecollapse">
                                                <i class="bx bx-dots-horizontal-rounded align-middle"></i>
                                            </button>
                                        </div>
                                        <div class="links-list-item" data-bs-toggle="tooltip" data-bs-trigger="hover"
                                            data-bs-placement="top" title="Emoji">
                                            <button type="button"
                                                class="btn btn-link text-decoration-none btn-lg waves-effect emoji-btn"
                                                id="emoji-btn">
                                                <i class="bx bx-smile align-middle"></i>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                                <div class="col">
                                    <div class="position-relative">
                                        <div class="chat-input-feedback">
                                            Please Enter a Message
                                        </div>
                                        <input v-model="sendMessage.content" autocomplete="off" type="text"
                                            class="form-control form-control-lg chat-input" autofocus id="chat-input"
                                            placeholder="Type your message...">
                                    </div>
                                </div>
                                <div class="col-auto">
                                    <div class="chat-input-links ms-2 gap-md-1">
                                        <div class="links-list-item d-none d-sm-block"
                                            data-bs-container=".chat-input-links" data-bs-toggle="popover"
                                            data-bs-trigger="focus" data-bs-html="true" data-bs-placement="top"
                                            data-bs-content="<div class='loader-line'><div class='line'></div><div class='line'></div><div class='line'></div><div class='line'></div><div class='line'></div></div>">
                                            <button type="button"
                                                class="btn btn-link text-decoration-none btn-lg waves-effect"
                                                onclick="audioPermission()">
                                                <i class="bx bx-microphone align-middle"></i>
                                            </button>
                                        </div>
                                        <div class="links-list-item">
                                            <button type="submit"
                                                class="btn btn-primary btn-lg chat-send waves-effect waves-light"
                                                data-bs-toggle="collapse" data-bs-target=".chat-input-collapse1.show">
                                                <i class="bx bxs-send align-middle" id="submit-btn"></i>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </form>
                        <div class="chat-input-collapse chat-input-collapse1 collapse" id="chatinputmorecollapse">
                            <div class="card mb-0">
                                <div class="card-body py-3">
                                    <!-- Swiper -->
                                    <div class="swiper chatinput-links">
                                        <div class="swiper-wrapper">
                                            <div class="swiper-slide">
                                                <div class="text-center px-2 position-relative">
                                                    <div>
                                                        <input id="attachedfile-input" type="file" class="d-none"
                                                            accept=".zip,.rar,.7zip,.pdf" multiple>
                                                        <label for="attachedfile-input"
                                                            class="avatar-sm mx-auto stretched-link">
                                                            <span
                                                                class="avatar-title font-size-18 bg-primary-subtle text-primary rounded-circle">
                                                                <i class="bx bx-paperclip"></i>
                                                            </span>
                                                        </label>
                                                    </div>
                                                    <h5
                                                        class="font-size-11 text-uppercase mt-3 mb-0 text-body text-truncate">
                                                        Attached</h5>
                                                </div>
                                            </div>
                                            <div class="swiper-slide">
                                                <div class="text-center px-2">
                                                    <div class="avatar-sm mx-auto">
                                                        <div
                                                            class="avatar-title font-size-18 bg-primary-subtle text-primary rounded-circle">
                                                            <i class="bx bxs-camera"></i>
                                                        </div>
                                                    </div>
                                                    <h5 class="font-size-11 text-uppercase text-truncate mt-3 mb-0"><a
                                                            href="#" class="text-body stretched-link"
                                                            onclick="cameraPermission()">Camera</a></h5>
                                                </div>
                                            </div>
                                            <div class="swiper-slide">
                                                <div class="text-center px-2 position-relative">
                                                    <div>
                                                        <input id="galleryfile-input" type="file" class="d-none"
                                                            accept="image/png, image/gif, image/jpeg" multiple>
                                                        <label for="galleryfile-input"
                                                            class="avatar-sm mx-auto stretched-link">
                                                            <span
                                                                class="avatar-title font-size-18 bg-primary-subtle text-primary rounded-circle">
                                                                <i class="bx bx-images"></i>
                                                            </span>
                                                        </label>
                                                    </div>
                                                    <h5 class="font-size-11 text-uppercase text-truncate mt-3 mb-0">
                                                        Gallery</h5>
                                                </div>
                                            </div>
                                            <div class="swiper-slide">
                                                <div class="text-center px-2">
                                                    <div>
                                                        <input id="audiofile-input" type="file" class="d-none"
                                                            accept="audio/*" multiple>
                                                        <label for="audiofile-input"
                                                            class="avatar-sm mx-auto stretched-link">
                                                            <span
                                                                class="avatar-title font-size-18 bg-primary-subtle text-primary rounded-circle">
                                                                <i class="bx bx-headphone"></i>
                                                            </span>
                                                        </label>
                                                    </div>
                                                    <h5 class="font-size-11 text-uppercase text-truncate mt-3 mb-0">
                                                        Audio</h5>
                                                </div>
                                            </div>
                                            <div class="swiper-slide">
                                                <div class="text-center px-2">
                                                    <div class="avatar-sm mx-auto">
                                                        <div
                                                            class="avatar-title font-size-18 bg-primary-subtle text-primary rounded-circle">
                                                            <i class="bx bx-current-location"></i>
                                                        </div>
                                                    </div>

                                                    <h5 class="font-size-11 text-uppercase text-truncate mt-3 mb-0"><a
                                                            href="#" class="text-body stretched-link"
                                                            onclick="getLocation()">Location</a></h5>
                                                </div>
                                            </div>
                                            <div class="swiper-slide">
                                                <div class="text-center px-2">
                                                    <div class="avatar-sm mx-auto">
                                                        <div
                                                            class="avatar-title font-size-18 bg-primary-subtle text-primary rounded-circle">
                                                            <i class="bx bxs-user-circle"></i>
                                                        </div>
                                                    </div>
                                                    <h5 class="font-size-11 text-uppercase text-truncate mt-3 mb-0"><a
                                                            href="#" class="text-body stretched-link"
                                                            data-bs-toggle="modal"
                                                            data-bs-target=".contactModal">Contacts</a></h5>
                                                </div>
                                            </div>

                                            <div class="swiper-slide d-block d-sm-none">
                                                <div class="text-center px-2">
                                                    <div class="avatar-sm mx-auto">
                                                        <div
                                                            class="avatar-title font-size-18 bg-primary-subtle text-primary rounded-circle">
                                                            <i class="bx bx-microphone"></i>
                                                        </div>
                                                    </div>
                                                    <h5 class="font-size-11 text-uppercase text-truncate mt-3 mb-0"><a
                                                            href="#" class="text-body stretched-link">Audio</a></h5>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="replyCard">
                        <div class="card mb-0">
                            <div class="card-body py-3">
                                <div class="replymessage-block mb-0 d-flex align-items-start">
                                    <div class="flex-grow-1">
                                        <h5 class="conversation-name"></h5>
                                        <p class="mb-0"></p>
                                    </div>
                                    <div class="flex-shrink-0">
                                        <button type="button" id="close_toggle"
                                            class="btn btn-sm btn-link mt-n2 me-n3 font-size-18">
                                            <i class="bx bx-x align-middle"></i>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- end chat input section -->
            </div>
            <!-- end chat conversation section -->

            <div v-if="user.email === ''"
                class=" w-100 d-flex flex-column justify-content-center align-items-center text-center italic-text custom-font"
                style="margin-top: 20%; font-style: italic;">
                <h1>Bienvenue sur <span class="text text-success"> simpleChat</span></h1>
                <h1>Clickez sur un contact pour discuter 😎</h1>
            </div>

            <!-- start User profile detail sidebar -->

            <!-- end User profile detail sidebar -->
        </div>
        <!-- end user chat content -->
    </div>
    <!-- End User chat -->

</template>

<style scoped>
.custom-font {
    font-family: 'Gloria Hallelujah', cursive;
}
</style>