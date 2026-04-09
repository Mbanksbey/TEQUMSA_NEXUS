provider "aws" {
  # The AWS region to deploy into. Use variables so callers can override this at apply time.
  region = var.aws_region
}

# Input variables used throughout the infrastructure configuration. These allow you
# to customise the environment without editing the Terraform code. The default
# region is set to us‑west‑2 (Oregon), but you can override it on the command
# line with `terraform apply -var "aws_region=us-east-1"`.
variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-west-2"
}

variable "allowed_origins" {
  description = "Comma‑separated list of origins allowed to call the API."
  type        = string
  default     = "*"
}

variable "openai_api_key" {
  description = "API key used by the AI service to call OpenAI's LLM."
  type        = string
}

variable "elevenlabs_api_key" {
  description = "API key used by the AI service for ElevenLabs TTS."
  type        = string
}

# Collect availability zones for the current region. This data source allows
# dynamic selection of zone names when creating subnets so the module works in
# any region with at least two AZs available.
data "aws_availability_zones" "available" {}

# The base VPC that hosts all resources. A /16 CIDR is used to give ample
# address space. If you already have a VPC this module could be parameterised
# to re‑use it instead.
resource "aws_vpc" "tequmsa" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = {
    Name = "tequmsa-vpc"
  }
}

# Two public subnets spread across distinct availability zones. These subnets
# automatically assign a public IP to launched ECS tasks so that they can
# communicate with the outside world. The cidrsubnet() function splits the
# parent VPC CIDR into smaller /24 networks.
resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.tequmsa.id
  cidr_block              = cidrsubnet(aws_vpc.tequmsa.cidr_block, 8, count.index)
  availability_zone       = element(data.aws_availability_zones.available.names, count.index)
  map_public_ip_on_launch = true
  tags = {
    Name = "tequmsa-public-${count.index}"
  }
}

# Internet gateway to provide egress to the internet for resources in public
# subnets.
resource "aws_internet_gateway" "gateway" {
  vpc_id = aws_vpc.tequmsa.id
  tags = {
    Name = "tequmsa-igw"
  }
}

# Route table for public subnets. Routes all outbound traffic to the internet
# gateway.
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.tequmsa.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gateway.id
  }
  tags = {
    Name = "tequmsa-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Security group for the Application Load Balancer. Allows inbound HTTP from
# anywhere and outbound to anywhere. TLS can be added later by adding a
# certificate and changing the listener protocol to HTTPS.
resource "aws_security_group" "alb" {
  name        = "tequmsa-alb-sg"
  description = "Allow inbound HTTP for ALB"
  vpc_id      = aws_vpc.tequmsa.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Security group for Fargate tasks. Permits traffic only from the ALB on the
# container port. Outbound traffic is unrestricted to permit calls to external
# APIs (e.g. OpenAI, ElevenLabs).
resource "aws_security_group" "fargate" {
  name        = "tequmsa-fargate-sg"
  description = "Allow inbound from ALB and outbound anywhere"
  vpc_id      = aws_vpc.tequmsa.id

  ingress {
    description      = "Allow HTTP from ALB"
    from_port        = 5000
    to_port          = 5000
    protocol         = "tcp"
    security_groups  = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ECS cluster definition. This does not create any compute capacity by itself
# because Fargate is used.
resource "aws_ecs_cluster" "tequmsa" {
  name = "tequmsa-cluster"
}

# ECR repository to store the Docker image for the backend service. You'll need
# to push your built image to this repository prior to running `terraform
# apply`.
resource "aws_ecr_repository" "tequmsa_backend" {
  name = "tequmsa-backend"
  tags = {
    Project = "TEQUMSA"
  }
}

# IAM role allowing ECS tasks to pull images from ECR and send logs to
# CloudWatch. The AmazonECSTaskExecutionRolePolicy managed policy grants the
# necessary permissions.
data "aws_iam_policy_document" "ecs_task_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name               = "tequmsa-task-execution-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_assume_role.json
}

resource "aws_iam_role_policy_attachment" "ecs_execution_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Application Load Balancer used to expose the backend service publicly.
resource "aws_lb" "tequmsa_alb" {
  name               = "tequmsa-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = [for subnet in aws_subnet.public : subnet.id]
  enable_deletion_protection = false
  tags = {
    Project = "TEQUMSA"
  }
}

resource "aws_lb_target_group" "tequmsa_tg" {
  name        = "tequmsa-tg"
  port        = 5000
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = aws_vpc.tequmsa.id

  health_check {
    path                = "/healthz"
    matcher             = "200"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
  tags = {
    Project = "TEQUMSA"
  }
}

resource "aws_lb_listener" "tequmsa_listener" {
  load_balancer_arn = aws_lb.tequmsa_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tequmsa_tg.arn
  }
}

# ECS task definition describing the Docker container. The image is pulled
# from ECR. Environment variables configure the AI service and allowed origins
# for CORS. The CPU and memory values should be tuned based on expected
# workload.
resource "aws_ecs_task_definition" "tequmsa_task" {
  family                   = "tequmsa-task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name  = "tequmsa-backend"
      image = aws_ecr_repository.tequmsa_backend.repository_url
      portMappings = [
        {
          containerPort = 5000
          hostPort      = 5000
          protocol      = "tcp"
        }
      ]
      environment = [
        {
          name  = "ALLOWED_ORIGINS"
          value = var.allowed_origins
        },
        {
          name  = "OPENAI_API_KEY"
          value = var.openai_api_key
        },
        {
          name  = "ELEVENLABS_API_KEY"
          value = var.elevenlabs_api_key
        }
      ]
      essential = true
    }
  ])

  tags = {
    Project = "TEQUMSA"
  }
}

# ECS service that runs the Fargate task and attaches it to the load balancer.
resource "aws_ecs_service" "tequmsa_service" {
  name            = "tequmsa-service"
  cluster         = aws_ecs_cluster.tequmsa.id
  task_definition = aws_ecs_task_definition.tequmsa_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [for subnet in aws_subnet.public : subnet.id]
    security_groups  = [aws_security_group.fargate.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.tequmsa_tg.arn
    container_name   = "tequmsa-backend"
    container_port   = 5000
  }

  depends_on = [aws_lb_listener.tequmsa_listener]
  tags = {
    Project = "TEQUMSA"
  }
}