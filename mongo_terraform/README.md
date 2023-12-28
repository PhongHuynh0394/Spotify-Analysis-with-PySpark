# Set up MongoDB Atlas with Terraform
This page will help you to set up your own MongoDB Atlas Cluster with Terraform.

For more detail, please read this: [Create an Atlas Cluster from a Template using Terraform](https://www.mongodb.com/docs/mongodb-vscode/create-cluster-terraform/)

## Prerequisite 
- [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
- [MongoDB Atlas account](https://www.mongodb.com/cloud/atlas/register)

## Step by Step
### Create Organization
When you create an MongoDB Atlas account, it will ask you to create your organization, just create
your own. Then you will lead to the home page of your organization.
Go to `Settings` section, copy your `Organization ID` and paste it to organization variable block in [variable.tf](./vairables.tf)
```bash
variable "org_id" {
  type = string
  description = "Organiztion ID"
  default = "add-your-id" # add your id here
}
```
### Create API key
Then go to `Access Manager` section in your Atlas menu, you will see the `API keys` tab. Just make
your own and copy it into [variables.tf](./vairables.tf) respectively
> Make sure your api key have `organization owner` role
```bash
variable "public_key" {
  type = string
  default = "add-your-key" # add your
}

variable "private_key" {
  type = string
  default = "add-your-key" #add your
}
```
### Deploy your Atlas Cluster
Now run the following command
```bash
cd mongo_terraform
terraform init # set up provider for atlas
terraform plan
```
You need to type `yes` to continue this process, then type `terraform apply` to deploy your cluster.

> Again, don't forget to type `yes` to continue, this process will take a few minutes. Just chill

After all, you will get something like:
```bash
Apply complete! Resources: 4 added, 0 changed, 0 destroyed.

Outputs:

password = "123"
srv_address = "mongodb+srv://spotify-cluster.kdglyul.mongodb.net"
user = "root"
```
Just notice 3 last lines. You will need them to add into your `.env` to run the system. They are
 `MONGODB_PASS`, `MONGODB_SRV` and `MONGODB_USER` respectively in .env file. Just copy the values and patse to it.

## Conclusion
 This terraform set up will deploy a MongoDB Atlas Cluster which is hosted on `GCP`. You can change to `AWS` or `Azure`
 if you want (don't forget to modify region also)

## To destroy resources
> :heavy_exclamation_mark: **Warning**: This command will terminate all your atlas cluster contain all your data. Use it carefully !

You can destroy everything on MongoDB by typing on terminal
```bash
terraform destroy
```
