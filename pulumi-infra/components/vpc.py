from pulumi_aws.ec2 import Route, InternetGateway, Vpc, Subnet, RouteTable, RouteTableAssociation
from pulumi import Output, ResourceOptions


def create_vpc(name: str, cidr_block: str, tags: dict, public_subnet_cidrs: list,  azs: list):
    vpc = Vpc(
        f"{name}",
        cidr_block=cidr_block,
        enable_dns_support=True,
        enable_dns_hostnames=True,
        tags=tags
    )

    public_subnets = [Subnet(
        f"{name}-public-subnet-{i}",
        vpc_id=vpc.id,
        cidr_block=public_subnet_cidrs[i],
        availability_zone=azs[i],
        map_public_ip_on_launch=True,
        tags={
            "Name": f"public-subnet-{ "a" if "a" in azs[i] else "b" }",
        },
        opts=ResourceOptions(parent=vpc)
    ) for i in range(len(public_subnet_cidrs))]

    public_route_table = RouteTable(
        f"{name}-public-route-table",
        vpc_id=vpc.id,
        tags={
            "Name": f"public-route-table-{ "a" if "a" in azs[0] else "b" }",
        },
        opts=ResourceOptions(parent=vpc)
    )

    internet_gateway = InternetGateway(
        f"{name}-internet-gateway",
        vpc_id=vpc.id,
        tags=tags,
        opts=ResourceOptions(parent=vpc)
    )

    for i, public_subnet in enumerate(public_subnets):
        RouteTableAssociation(
            f"{name}-public-route-table-association-{i}",
            subnet_id=public_subnet.id,
            route_table_id=public_route_table.id,
            opts=ResourceOptions(parent=public_route_table)
        )
    
    route_table_route_igw = Route(
        f"{name}-public-route-table-route-igw",
        route_table_id=public_route_table.id,
        destination_cidr_block="0.0.0.0/0",
        gateway_id=internet_gateway.id,
        opts=ResourceOptions(parent=public_route_table)
    )

    return {
        "vpc": vpc,
        "public_subnets": public_subnets,
        "public_route_table": public_route_table,
        "internet_gateway": internet_gateway,
        "route_table_route_igw": route_table_route_igw
    }