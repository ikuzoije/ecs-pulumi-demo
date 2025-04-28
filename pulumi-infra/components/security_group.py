from pulumi_aws.ec2 import SecurityGroup, SecurityGroupRule
from pulumi import ResourceOptions

def setup_security_group(vpc_id: str, vpc_cidr:str):
    loadbalancer_sg = SecurityGroup(
        f"lb-security-group",
        name="lb-security-group",
        vpc_id=vpc_id,
        tags={
            "Name": "Loadbalancer-SG",
        },
    )


    lb_allow_inbound_80_rule = SecurityGroupRule(
        "alb-allow-inbound-80",
        security_group_id=loadbalancer_sg.id,
        type="ingress",
        protocol="tcp",
        from_port=80,
        to_port=80,
        cidr_blocks=["0.0.0.0/0"],
    )

    lb_allow_outbound_all_rule = SecurityGroupRule(
        "alb-allow-outbound-all",
        security_group_id=loadbalancer_sg.id,
        type="egress",
        protocol="-1",
        from_port=0,
        to_port=0,
        cidr_blocks=["0.0.0.0/0"],
    )

    ecs_security_group = SecurityGroup(
        f"ecs-security-group",
        name="ecs-security-group",
        vpc_id=vpc_id,
        tags={
            "Name": "ECS-SG",
        },
    )

    ecs_allow_inbound_80_rule = SecurityGroupRule(
        "ecs-allow-inbound-80",
        security_group_id=ecs_security_group.id,
        type="ingress",
        protocol="tcp",
        from_port=8080,
        to_port=8080,
        cidr_blocks=[f"{vpc_cidr}"],  # Allow traffic from the VPC CIDR block
    )

    ecs_allow_outbound_all_rule = SecurityGroupRule(
        "ecs-allow-outbound-all",
        security_group_id=ecs_security_group.id,
        type="egress",
        protocol="-1",
        from_port=0,
        to_port=0,
        cidr_blocks=["0.0.0.0/0"],
    )

    return {
        "loadbalancer_sg": loadbalancer_sg,
        "ecs_security_group": ecs_security_group
    }