# tkd_ess

Taekwondo Electronic Scoring System

Introduction

This Taekwondo Electronic Scoring System consists of 3 components: client, server and admin. Client can be built into an android app and be used as a controller by referees. Server (not a good name) is the central processing component that display the scores. Admin is used by the technical personel to control all other settings, such as Match number, Time, Scores etc.


How It Works
All 3 components are developed with Kivy in Python. At the moment, Server is the central processing unit that listens to multiple Clients and one Admin connection through socket. Upon receiving the data sent by the Clients and Admin, the Server will update the display texts. However, this is not a good architecture, because Server now needs to send data back to Admin to update the scores. Therefore, the architecture will be changed in future, that the Admin should be the central processing unit. It will listen inputs from Clients and send data to Server (which to be renamed to Display later). This way, we can keep the signals following in one direction: Clients -> Admin -> Server (Display)