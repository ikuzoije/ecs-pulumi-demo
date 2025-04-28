import pulumi
from pulumi_aws import get_availability_zones
from components.vpc import create_vpc
from components.security_group import setup_security_group
from components.ecr_docker import setup_ecr_docker_repo
from components.iam import project_roles
from components.ecs import setup_ecs_cluster
from components.alb import setup_alb

aws_config = pulumi.Config("aws")
aws_region = aws_config.require("region")

vpc_cidr = "10.0.0.0/16"
public_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
azs = get_availability_zones(state="available")
vpc_tags = {
    "Name": "ecs-demo",
    "Environment": "dev",
    "Project": "ecs-demo"
}

# setup vpc
vpc = create_vpc(
    name="ecs-demo",
    cidr_block=vpc_cidr,
    tags=vpc_tags,
    public_subnet_cidrs=public_subnet_cidrs,
    azs=[azs.names[0], azs.names[1]]
)

# set up security groups
security_groups = setup_security_group(vpc["vpc"].id, vpc_cidr)

# Setup app docker image & ECR repo
ecr_repo = setup_ecr_docker_repo(name="ecs-demo", tags=vpc_tags)

# set up IAM role
project_iam_role = project_roles("ecs-demo")

# setup load balancer
app_alb = setup_alb(
    name="ecs-demo",
    vpc_id=vpc["vpc"].id,
    subnets=[subnet.id for subnet in vpc["public_subnets"]],
    security_groups=[security_groups["loadbalancer_sg"].id],
)

# set up ECS cluster
setup_ecs_cluster(
    name="ecs-demo",
    security_group_id=security_groups["ecs_security_group"].id,
    subnet_ids=[subnet.id for subnet in vpc["public_subnets"]],
    task_definition_role=project_iam_role,
    image_url=ecr_repo,
    region=aws_region,
    target_group_arn=app_alb["target_group"].arn
)

pulumi.export("app_endpoint", app_alb["load_balancer"].dns_name)
