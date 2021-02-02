# Demo Flow
## ACI + GitHub Actions
We want to emphaise the following points
- best practices for running your container in production: avoid puling from public registries for prodution, use specific version tags rather than latest, use container scans to detect vulnerabilities 
- GitHub Actions makes it easy to follow these best practices in a dev friendly, an automated workflow. Make use of features like GitHub Secrets to store your Azure Credentials (no plain text passwords folks!!) 
- ACI is a quick, simple, and cost effective way to run serverless containers in production

## Demo
Azure Friday Demo GitHub Action 
* Job 1 - Setup environment: Storage account and Container Registry
* Job 2 - Build / Bush to ACR: build image, scan image, and push image to ACR
* Job 3 - Deploy to ACI: deploy to ACI
