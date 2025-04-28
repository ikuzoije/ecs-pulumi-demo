import json
from pulumi import Config 

app_name = Config("app").require("name")
app_version = Config("app").require("version")

def container_definition(image_url: str, region: str, project_name: str):
    container_definition = [
        {
            "name": "demo-app",
            "image": image_url,
            "cpu": 256,
            "memory": 512,
            "essential": True,
            "networkMode": "awsvpc",
            "portMappings": [{
                "containerPort": 8080,
                "hostPort": 8080
            }],
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": f"/ecs/{project_name}/demo-app",
                    "awslogs-region": f"{region}",
                    "awslogs-create-group": "true",
                    "awslogs-stream-prefix": "ecs"
                }
            },
            "environment": [
                {"name": "APP_NAME", "value": f"{app_name}"},
                {"name": "APP_VERSION", "value": f"{app_version}"}
            ]
        }
    ]
    return json.dumps(container_definition)