# Taekwondo Electronic Scoring System

<h4>Introduction</h4>

This Taekwondo Electronic Scoring System consists of 3 components: 
1. Client, 
2. Admin and
3. Display. 
Client can be built into an android app and be used as a controller by referees. Server (not a good name) is the central processing component that display the scores. Admin is used by the technical personel to control all other settings, such as Match number, Time, Scores etc.


<h4>Overall Architecture</h4>
All 3 components are developed with Kivy in Python. Admin is the central unit that listens to multiple Client connections through sockets, as well as connecting to Display. Data sent by the Clients is received by Admin, processed and later on send to Display.

<h4>Client</h4>

Client's development is completed. Since other two components are still under development, it is difficult to test on Client. 
Nevertheless, you can proceed to build an APK using buildozer and run it on Android phone. The Client already has the basic functionalities as follow:
<ol>
  <li>Connect to server</li>
  <li>Send score to server</li>
</ol>

<h4>Admin</h4>
Status: Under development

<h4>Server</h4>
Status: Under development
