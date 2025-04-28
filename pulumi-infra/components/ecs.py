from pulumi_aws.ecs import Cluster, Service, TaskDefinition
from components.container_json import container_definition
import pulumi

def setup_ecs_cluster(name: str, security_group_id: str, subnet_ids: list, task_definition_role, image_url: str, region: str, target_group_arn: str):
    ecs_cluster = Cluster(
        f"{name}-cluster",
        name=f"{name}-cluster",
        tags={
            "Name": f"{name}-cluster",
        }
    )
    task_def_json = pulumi.Output.all(
        image_url, region, name
    ).apply(lambda args: container_definition(args[0], args[1], args[2]))

    # Add a dummy output to force Pulumi to detect changes
    task_def_hash = task_def_json.apply(lambda x: hash(str(x)))

    task_definition = TaskDefinition(
        f"{name}-task-definition",
        family=f"{name}-task-definition",
        container_definitions=task_def_json,
        execution_role_arn=task_definition_role.arn,
        requires_compatibilities=["FARGATE"],
        network_mode="awsvpc",
        cpu="512",
        memory="1024",
        opts=pulumi.ResourceOptions(replace_on_changes=["container_definitions"])
    )

    app_service = Service(
        "app-service",
        name="app-service",
        cluster=ecs_cluster.id,
        task_definition=task_definition.arn,
        desired_count=1,
        load_balancers=[{
            "target_group_arn": target_group_arn,
            "container_name": "demo-app",
            "container_port": 8080,
        }],
        launch_type="FARGATE",
        network_configuration={
            "subnets": subnet_ids,
            "security_groups": [security_group_id],
            "assign_public_ip": True,
        },
        
        )
