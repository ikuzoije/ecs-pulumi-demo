# ECS Fargate Application with Pulumi

This project demonstrates deploying a Node.js application on AWS ECS Fargate using Pulumi as the Infrastructure as Code (IaC) tool. The application accepts an input value via Pulumi configuration, which is passed as an environment variable to the Node.js application.

## Project Structure

- **`/pulumi-infra`**: Contains all Pulumi infrastructure code.
    - **`/pulumi-infra/components`**: Contains reusable Pulumi components implemented as Python functions.
    - **`__main__.py`**: Entry point for defining and deploying the infrastructure. It orchestrates the components and passes data between them.

## Features

- **AWS ECS Fargate**: The application is deployed as a containerized service on AWS ECS Fargate.
- **Pulumi Configuration**: Accepts user-defined input via `pulumi config`, which is passed as an environment variable to the Node.js application.
- **Modular Infrastructure**: Core infrastructure is implemented as reusable components for better maintainability.

## Prerequisites

- [Pulumi CLI](https://www.pulumi.com/docs/get-started/install/)
- [AWS CLI](https://aws.amazon.com/cli/) configured with appropriate credentials
- Python 3.7+ and `pip` for managing dependencies
- Docker for building and pushing the Node.js application container image to Amazon ECR during infrastructure deployment

## Getting Started

1. **Install Dependencies**  
     Navigate to the `/pulumi-infra` folder and install the required Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```

2. **Set Pulumi Configuration**  
     Set the required configuration value using the Pulumi CLI:
     ```bash
     pulumi config set <key> <value>
     ```
     Replace `<key>` with the configuration key expected by the application.

3. **Deploy the Infrastructure**  
     Deploy the infrastructure using Pulumi. This step will also build the Docker image for the Node.js application and push it to Amazon ECR:
     ```bash
     pulumi up
     ```

4. **Access the Application**  
     Once deployed, Pulumi will output the URL of the ECS service. Use this URL to access the application.

## Cleanup

To tear down the infrastructure, run:
```bash
pulumi destroy
```

## Notes

- Ensure that the AWS region is correctly configured in your Pulumi stack.
- Docker must be installed and running during the deployment process, as Pulumi will build and push the application image to Amazon ECR.
- The Node.js application should be designed to read the environment variable passed by Pulumi.

