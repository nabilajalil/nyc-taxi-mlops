
## Validate Configuration

```bash
terraform -chdir=infra/terraform fmt -check
terraform -chdir=infra/terraform validate
```

## Review Infrastructure Changes

```bash
terraform -chdir=infra/terraform plan
```

Always review the Terraform plan before applying changes.

## Existing AWS Resources

The following resources were imported into Terraform:

- S3 bucket
- S3 bucket versioning
- S3 server-side encryption
- S3 public-access protection
- EC2 instance
- EC2 security group

Existing resources were imported rather than recreated.

A fresh clone does not contain the local Terraform state.
Do not run terraform apply until the existing state has been
restored or the AWS resources have been imported.

## Security

- Terraform state files are excluded from Git.
- S3 versioning and encryption are enabled.
- S3 public access is blocked.
- EC2 SSH access is restricted to specific IP addresses.
- Terraform prevent_destroy protects key resources against
  deletion through Terraform.

## Future Improvements

- Configure a dedicated least-privilege IAM identity.
- Migrate local Terraform state to a secure remote backend.
- Add infrastructure validation to GitHub Actions.
