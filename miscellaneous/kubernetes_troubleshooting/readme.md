### Note:

This directory is meant to serve as a record of all the time spent in troubleshooting and configuring kubernetes cluster on our team's server. It took us disproportionately more time than what this txt file represents but it is an indication of the same.

- Reflection for the same have been added on wiki notes here: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/wikis/M3---stuck-on-port-issue-for-kubernetes-cluster

We spent a lot of time on this but we feel it would be better if we spend the remaining time on other aspects of the project.

What we tried:
- Reverse proxy through nginx container outside the cluster was tried.
ip tables was tried.
- creating pods with nginx + ubuntu was tried inside the cluster.
- creating docker containers to ditch cluster was tried then using redirection requests. get was tried as well.
(none worked to give what we want)

To summarise: everything works with curl http://fall2023-comp585-4.cs.mcgill.ca/recommend/12345 but not with curl http://fall2023-comp585-4.cs.mcgill.ca:8082/recommend/12345.


### more info.

##### Meeting Debugging 01

Nov 18th: Aayush and Varun - duration (whole night)
We had thought of using Kubernetes to set up our canary release pipeline. We launched a Kubernetes cluster on our server using KIND (Kubernetes in Docker) since we don't have root access. Our inference service is set up on the cluster but we are having a hard time exposing it to our external server IP and DNS (http://fall2023-comp585-4.cs.mcgill.ca) on port 8082. We tried multiple things: we set up an ingress controller on our cluster to direct traffic from http://fall2023-comp585-4.cs.mcgill.ca to our internal K8s service. This works, but only for port 80, not port 8082, i.e. http://fall2023-comp585-4.cs.mcgill.ca/recommend/34566 works but not http://fall2023-comp585-4.cs.mcgill.ca:8082/recommend/34566. We figured this may be because the ingress is taking traffic from port 80 and not 8082. We tried a lot of things to change this but nothing works. We have an external IP exposed by the KIND cluster http://172.25.255.200:8082 and we tried to set up an NGINX reverse proxy outside the cluster on our server to direct traffic from http://fall2023-comp585-4.cs.mcgill.ca:8082 to http://172.25.255.200:8082, but that doesn't work either (we get a 499 error from nginx).

##### Meeting Debugging 02

Nov 19th: Aayush and Varun
We continued with trying to fix the port issue for the cluster.
It is to be noted that we do not have root access so installation of ingress controllers is limited. Also, we cannot do port forwarding using iptables because we do not have sudo privileges. We tried nginx reverse proxy through a separate docker container but it did not work sadly.
Varun and I spent most of weekend on kubernetes deployment for specific port without using iptable port forwarding or support container reverse proxy. None worked. Need sudo access. Have asked Deeksha. We spent 30-35 hours between both of us.