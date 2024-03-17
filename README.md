# pns-si5-orchestration
This repository contains the source code of the polymetrie application along with all deployment files used. Below, you will find important information to understand and utilize this repository.

## Directory Contents
* /src: This directory contains the source code of the Polymetry application and the code for load testing.

* /deployment: All deployment files necessary.
 ## Deployment prerequisites :
* kubectl: Kubernetes command-line tool.

* Helm: Kubernetes package manager.
## Polymetrie helm chart
You can find [here](https://github.com/sourour9/Helm-Chart-Polymetrie/tree/main) the Helm Chart for deploying the polymetrie application.

## Polymetrie image docker 
The latest Docker image for the Polymetrie application is hosted on Docker Hub. You can find the image and its corresponding tags at the following link:

[Docker Hub - Polymetrie Application](https://hub.docker.com/r/hamza125/polymetrie-increment/tags)

## Polymetrie Grafana Dashboard
You can find [here](https://grafana.orch-team-g.pns-projects.fr.eu.org/d/c71bf583-d634-4274-83a4-0d2146db3f75/polymetrie-dashboard?orgId=1) a Grafana dashboard that display system and business metrics.

user : admin

password: teamg

## Polymetrie ArgoCD
You can find [here](https://argocd.orch-team-g.pns-projects.fr.eu.org/login?return_url=https%3A%2F%2Fargocd.orch-team-g.pns-projects.fr.eu.org%2Fapplications) our ArgoCD web user interface.

user : admin 

password : bCStMcxRHezrhwZ1A2q0Uy3BPm9QXLGs


## Polymetrie Kibana
You can find [here](https://kibana.orch-team-g.pns-projects.fr.eu.org/app/home) our Kibana web user interface.

user : elastic

password : vzp20028y7Ku7g9uqYJpim85


