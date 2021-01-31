# Demo Flow
## Main takeaways
We want to emphaise the following points
- best practices for running your container in production: avoid puling from public registries for prodution, use specific version tags rather than latest, use container scans to detect vulnerabilities 
- GitHub Actions makes it easy to follow these best practices in a dev friendly, an automated workflow. Make use of features like GitHub Secrets to store your Azure Credentials (no plain text passwords folks!!) 
- ACI is a quick, simple, and cost effective way to run serverless containers in production

## Before the demo
Viewers will need the context set that an 'ops team' have provisioned the Virtual Network and App Gateway. The application consists of two container groups: one hosts an internal observability dash and the other an API. There are two environments,staging and production (accessed with port 8443), that Jessica will be working in as a developer. 

## Demo
1. Source code is modified to update health check response in API (returns 'healthy' instead of 'ok')
2. Image is built, scanned, and pushed to ACR (v:1.1) with the [Container Scan GitHub Action](https://github.com/Azure/container-scan). 
2.	Staging containers are provisioned with the [AZ CLI GitHub Action](https://github.com/marketplace/actions/azure-cli-action). Jose verifying App Gateway being able to refresh DNS changes.
3.	Functionality of the new containers is verified using the staging URL
4. Jessica opens a PR to merge into prod that Scott will review using [PR GitHub Action](https://github.com/marketplace/actions/create-pr-action)
5. Once approved, production containers are patched with the new version (ACI does updates by running a second create command on top of the existing container group). 

## Rude FAQ
_When should I use ACI vs Web App for containers?_
Web Apps for Containers provides several features specifically designed for hosting web applications such as
* Fully customizable domain names
* TLS/SSL certificate management 
* Traffic manager integration
If you don't mind managing SSL termination or networking, ACI is a pure, serverless container offering with flexible pay-as-you-go pricing for you to host your web applications too. 

_When should I use AKS vs ACI_?
ACI is a great option for general-purpose serverless compute where tasks can be run independently. However, when you start to need to orchestrate relatinships between complex, multicontainer applicatsions with features such as 
--> affinity/anti-antfinity
--> coordinated application upgrades
--> autoscaling
we recommend you look to a container orchestrator such as AKS. ACI can be a complimentary service to orchestrators such as AKS through the Virtual Kubelet integration, allowing for quick bursts of serverless compute with PAYG pricing. 

## Slides
[Powerpoint deck](https://microsoft-my.sharepoint.com/:p:/p/macolso/EQ1TXy53GQBAr-TQ06mNm4YB4QJxEmKgPmUufi94qggMKA?e=q7AXrvs)