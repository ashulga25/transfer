Repo Description:

Sample python hello-world web-app, which has 3 endpoints

- /             # Prints "Hello, World!"
- healthz       # healthcheck
- /primes/<n>   # prints specified number of prime numbers. Purpose - simulate CPU load and cause auto-scaling.
                # A proper number to check auto-scaling is working properly would be about 125000 or more.
                # If the very large number calculation is initiated - it would generate a 504 Gateway timeout, 
                but the app would continue calculations.


Pipeline is build in a way to use Azure OIDC. So upon deployment just update following from TF output
Secrets:
- AWS_ROLE_ARN              # AWS ROLE ARN required to login and push to ECR
- AWS_ROLE_ARN_FOR_DEPLOY   # AWS ROLE ARN required to deploy into EKS cluster

Variables:
- APP_NAME                  # Appllication name, required for deployment in AWS EKS clsuter. Default name "python-app"
- AWS_REGION                # AWS Region where ECR and EKS CLsuter are deployed, default `us-east-2`
- ECR_REPO_NAME             # AWS ECR Repo name, default `ashulga_logika_repo`
- ECR_CLUSTER_NAME          # AWS ECR Cluslter name, default `dev-con_andrii_shulga`
- NAMESPACE                 # Namespace where to deploy K8s objects (Deployment, Service, Ingress). Default `con-andrii-shulga-logika`
- QUALITY_GATE              # Number of acceptable trivy critical findings. If exceeded - pipeline would break. Default `5`
- SITE_TESL_URL             # URL name where the app should be reachable, used for test upon deployment. There was no requirement for HTTPS deployment,
                            # so no cert-bot or custom cert was used. Default vallue `ashulga-python-app.logika.com`

Pipeline builds the docker image, performs tests of the built application with basic tests.
Also pipeline performs vulnerability scan with trivy and prints the table of HIGH and CRITICAL findings.
Also it has some predefined threshold, if number of CRITICAL findings is too high - the pipeline would break, forcing developer to fix vulnerabilities in the app.
Scan results are stored as artifact and can be downloaded by users for offline analysis.


Push to Azure ACR and deployment of the app into Azure WebApp are performed using Azure Federated credentials via OIDC, so no credentials are stored in the repo, only the roles ARNs. This is the most secure approach, astoken used are short-lived and AWS IAM permissions are very granular and allow access only from this github_organization. 
Pipeline authenticates via OIDC in AWS IAM, so we have to create respective policies and roles in AWS IAM.


Before deploying to AWS EKS pipeline check the number of nodes to make sure EKS clsuter is reachable. Then updates placeholder with namespace and image repository, 
which are acquired dynamically based on the role login. A new image tag is used for every deployment, based on built. Only app repository remains static with this approach.

Application uses modern AWS ALB Controller, so it does not need a static IP. Once deployed it gets a dynamic ALB DNS name,
which pipeline then utilizes for tests to check that application is reachable and the `/healthz` endpoint responds the status.
There is some delay until the ALB is registered for the first time, so test is utilizing a script with 10 attempts to check endpoint availability, sleeping 60s between
attempts.

I have not deployed any TLS certifiacate as it was not part of the task and it would require a DNS name with this type of ALB. 
Also, we have a simple app, which does not transfer any sensitive data.

.dockerfile ignore is used for the Docker to add only application relevant files to the image, and do not add the kubernetes deployment of github pipeline files.