# Terraform
## What it does?

## How to Install?
Run file ```terraform_installation.sh```

## How to get started?
To reproduce system, please, follow instructions:
1. Install terraform
2. Create a folder for terraform scripts
3. Add needed credentials to the file ```variables.tf```
4. Check all configs for the file ```ec2_with_code.tf```
5. Input:
~~~
terraform init
terraform apply -auto-approve
~~~
Terraform automatically grabs all scripts from the folder (!)
