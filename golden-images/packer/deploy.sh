#!/bin/bash
#
# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
#

# Function to deploy on AWS
deploy_aws() {
    echo "Deploying to AWS..."
    read -p "Enter your AWS Access Key: " aws_access_key
    read -p "Enter your AWS Secret Key: " aws_secret_key
    read -p "Enter the AWS Region: " aws_region
    read -p "Enter the Source AMI Filter Name: " source_ami_filter_name

    # Create a copy of the Packer template in the /tmp directory
    mkdir -p /tmp/composabl; cp -r ./ /tmp/composabl

    # Replace the placeholder values in your Packer template
    sed -i "s|your_aws_access_key|$aws_access_key|g" /tmp/composabl/cloud-aws.pkr.hcl
    sed -i "s|your_aws_secret_key|$aws_secret_key|g" /tmp/composabl/cloud-aws.pkr.hcl
    sed -i "s|us-west-2|$aws_region|g" /tmp/composabl/cloud-aws.pkr.hcl
    sed -i "s|ubuntu/images/*ubuntu-jammy-22.04-amd64-server-*|$source_ami_filter_name|g" /tmp/composabl/cloud-aws.pkr.hcl

    # Run Packer build
    packer init /tmp/composabl/cloud-aws.pkr.hcl
    packer build /tmp/composabl/cloud-aws.pkr.hcl

    # Print info
    echo "Your image is ready. You can now create a VM from the image."
    echo "Credentials:"
    echo "Username: composabl" # https://developer.hashicorp.com/packer/integrations/hashicorp/azure/latest/components/builder/arm#defaults
    echo "Password: composabl123!"
}

# Function to deploy on Azure
deploy_azure() {
    echo "Deploying to Azure..."
    read -p "Enter your Client ID: " azure_client_id
    read -p "Enter your Client Secret: " azure_client_secret
    read -p "Enter your Subscription ID: " azure_subscription_id
    read -p "Enter your Tenant ID: " azure_tenant_id
    read -p "Enter your Resource Group: " azure_resource_group
    read -p "Enter your Image Name: " azure_image_name
    # read -p "Enter your Location (see az account list-locations): " azure_location

    # Create a copy of the Packer template in the /tmp directory
    mkdir -p /tmp/composabl; cp -r ./ /tmp/composabl

    # Replace the placeholder values in your Packer template
    sed -i "s|your_client_id|$azure_client_id|g" /tmp/composabl/cloud-azure.pkr.hcl
    sed -i "s|your_client_secret|$azure_client_secret|g" /tmp/composabl/cloud-azure.pkr.hcl
    sed -i "s|your_subscription_id|$azure_subscription_id|g" /tmp/composabl/cloud-azure.pkr.hcl
    sed -i "s|your_tenant_id|$azure_tenant_id|g" /tmp/composabl/cloud-azure.pkr.hcl
    sed -i "s|your_resource_group|$azure_resource_group|g" /tmp/composabl/cloud-azure.pkr.hcl
    sed -i "s|your_image_name|$azure_image_name|g" /tmp/composabl/cloud-azure.pkr.hcl
    # sed -i "s|eastus|$azure_location|g" /tmp/composabl/cloud-azure.pkr.hcl

    # Run Packer build
    packer init /tmp/composabl/cloud-azure.pkr.hcl
    packer build /tmp/composabl/cloud-azure.pkr.hcl

    # Print info
    echo "Your image is ready. You can now create a VM from the image."
    echo "Credentials:"
    echo "Username: composabl" # https://developer.hashicorp.com/packer/integrations/hashicorp/azure/latest/components/builder/arm#defaults
    echo "Password: composabl123!"
}

# Function to deploy on GCP
deploy_gcp() {
    echo "Deploying to GCP..."
    read -p "Enter your Project ID: " gcp_project_id
    read -p "Enter the Zone: " gcp_zone
    read -p "Enter the SSH Username: " gcp_ssh_username

    # Create a copy of the Packer template in the /tmp directory
    mkdir -p /tmp/composabl; cp -r ./ /tmp/composabl

    # Replace the placeholder values in your Packer template
    sed -i "s|your_project_id|$gcp_project_id|g" /tmp/composabl/cloud-gcp.pkr.hcl
    sed -i "s|us-central1-a|$gcp_zone|g" /tmp/composabl/cloud-gcp.pkr.hcl
    sed -i "s|your_ssh_username|$gcp_ssh_username|g" /tmp/composabl/cloud-gcp.pkr.hcl

    # Run Packer build
    packer init /tmp/composabl/cloud-gcp.pkr.hcl
    packer build /tmp/composabl/cloud-gcp.pkr.hcl

    # Print info
    echo "Your image is ready. You can now create a VM from the image."
    echo "Credentials:"
    echo "Username: composabl" # https://developer.hashicorp.com/packer/integrations/hashicorp/azure/latest/components/builder/arm#defaults
    echo "Password: composabl123!"
}

# Main menu
echo "Select your cloud provider for deployment:"
echo "1) AWS"
echo "2) Azure"
echo "3) GCP"
read -p "Enter your choice (1-3): " provider_choice

case $provider_choice in
    1)
        deploy_aws
        ;;
    2)
        deploy_azure
        ;;
    3)
        deploy_gcp
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
