from pulumi_aws.lb import LoadBalancer, TargetGroup, Listener

def setup_alb(name: str, vpc_id: str,subnets: list, security_groups: list):
    app_lb = LoadBalancer("app-lb",
        name=f"{name}",
        internal=False,
        load_balancer_type="application",
        security_groups=security_groups,
        subnets=subnets,
        enable_deletion_protection=False,
        tags={
            "Environment": "production",
        })
    
    app_tg = TargetGroup("app-tg",
        name=f"{name}-tg",
        port=8080,
        protocol="HTTP",
        target_type="ip",
        vpc_id=vpc_id,
        health_check={
            "enabled": True,
            "port": "8080",
            "protocol": "HTTP",
    }
    )


    app_listener = Listener("app_listener",
        load_balancer_arn=app_lb.arn,
        port=80,
        protocol="HTTP",
        default_actions=[{
            "type": "forward",
            "target_group_arn": app_tg.arn,
        }])
    
    return {
        "load_balancer": app_lb,
        "target_group": app_tg,
        "listener": app_listener
    }