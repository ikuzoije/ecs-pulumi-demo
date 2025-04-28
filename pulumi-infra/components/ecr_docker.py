from pulumi_aws.ecr import Repository, get_authorization_token_output
from pulumi_docker import Image, RegistryArgs


def setup_ecr_docker_repo(name: str, tags: dict):
    """Setup ECR Docker repository"""
    repo = Repository(
        f"{name}-docker-repo",
        name=name,
        image_scanning_configuration={
        "scan_on_push": True,
    },
        image_tag_mutability="MUTABLE",
        force_delete=True,
        tags=tags
    )

    auth_token = get_authorization_token_output(registry_id=repo.registry_id)

    # build docker app and push to ECR
    build_docker_image(name=name, dockerfile_path="../src/Dockerfile", context_path="../src", ecr_repository=repo, auth_token=auth_token)


    return repo.repository_url

def build_docker_image(name: str, dockerfile_path: str, context_path: str, ecr_repository: str, auth_token):    
    image = Image(
        f"{name}-docker-image",
        build={
            "context": context_path,
            "dockerfile": dockerfile_path,
            "platform": "linux/amd64"
        },
        image_name=ecr_repository.repository_url,
        skip_push=False,
        registry={
        "server": ecr_repository.repository_url,
        "password": auth_token.password,
        "username": auth_token.user_name
        }
    )

    return image