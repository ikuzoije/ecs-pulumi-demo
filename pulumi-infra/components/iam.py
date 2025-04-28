from pulumi_aws.iam import Role, RolePolicyAttachment
import json

def project_roles(project_name: str):
    # Create IAM role for ECS task execution
    ecs_task_execution_role = Role(f"{project_name}-ecs-task-execution-role",
        name=f"{project_name}-ecs-task-execution-role",
        assume_role_policy=json.dumps({
            "Version": "2012-10-17",
            "Statement": [{
                "Action": "sts:AssumeRole",
                "Effect": "Allow",
                "Sid": "trustPolicy1",
                "Principal": {
                    "Service": "ecs-tasks.amazonaws.com",
                },
            }],
        }))
    # Attach the AmazonECSTaskExecutionRolePolicy to the role
    ecs_task_execution_role_policy_attachment = RolePolicyAttachment(f"{project_name}-ecs-task-execution-role-policy-attachment",
        role=ecs_task_execution_role.name,
        policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy")

    # Attach a custom policy for logs:CreateLogGroup
    logs_policy_attachment = RolePolicyAttachment(f"{project_name}-logs-policy-attachment",
        role=ecs_task_execution_role.name,
        policy_arn="arn:aws:iam::aws:policy/CloudWatchLogsFullAccess")

    return ecs_task_execution_role