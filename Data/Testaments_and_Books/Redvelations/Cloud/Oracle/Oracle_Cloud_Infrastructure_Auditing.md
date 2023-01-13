<!---------------------------------------------------------------------------------
Copyright: (c) BLS OPS LLC.
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
--------------------------------------------------------------------------------->
# Oracle Cloud Infrastructure Auditing

## References

* Oracle Cloud Infrastructure Security Guide -<br />[https://docs.oracle.com/en-us/iaas/Content/Security/Concepts/security_guide.htm](https://docs.oracle.com/en-us/iaas/Content/Security/Concepts/security_guide.htm)
* Oracle Cloud Infrastructure Documentation: Security Best Practices -<br />[https://docs.oracle.com/en-us/iaas/Content/Security/Reference/configuration_security.htm](https://docs.oracle.com/en-us/iaas/Content/Security/Reference/configuration_security.htm)

## Overview

The intended design for a secure Oracle Cloud Infrastructure (OCI) environment is to have the following characterstics. These characteristics are spelled out in the standards for each section with slightly varied language.

* One account should be maintained as the break-glass administrator account. This account can **manage** all resources in the tenancy.
* The break-glass administrator account should be accessible only through heavily restricted means
* The break-glass administrator should not have any option for programmatic access such as API keys. The existence of API keys would be contrary to the purpose of the break-glass administrator.
* All other accounts should be federated. MFA enabled and effective password policies.
* The tenancy is divided into compartments for the various needs of the enterprise. Each compartment should have distinct compartment administrators that hold functions considered sensitive, including **delete** permissions. Compartment administrators should not be used for performing daily functions.
* *Summarizing*, a section such as asset management highlights what a failure to enforce several principles looks like. Having resources stored in the root compartment of the tenancy is a violation of the principals because it requires that an account with permissions to manage the tenancy to create the resources initially. Additionally, removal or management of those resources requires accounts with the same elevated permisions. By design, accounts with those permissions should only be accessed in emergency situations.

## Noteworthy Security List Information

Security Lists are policies that define permissions using specific **verbs**. Understand the below to know how much permission you may have.

When understanding security lists, the below outline is very helpful:

**Verbs**
* **inspect**
    * Ability to list resources, without access to any confidential information or user-specified metadata that may be part of that resource. Important: The operation to list policies includes the contents of the policies themselves, and the list operations for the Networking resource-types return all the information (e.g., the contents of security lists and route tables).
    * Third-party auditors
* **read**
    * Includes inspect plus the ability to get user-specified metadata and the actual resource itself.
    * Internal auditors
* **use**
    * Includes read plus the ability to work with existing resources (the actions vary by resource type). Includes the ability to update the resource, except for resource-types where the "update" operation has the same effective impact as the "create" operation (e.g., UpdatePolicy, UpdateSecurityList, etc.), in which case the "update" ability is available only with the manage verb. In general, this verb does not include the ability to create or delete that type of resource.
    * Day-to-day end users of resources
* **manage**
    * Includes all permissions for the resource.
    * Administrators

**Special exceptions**

* Users
	* Access to both manage users and manage groups lets you do anything with users and groups, including creating and deleting users and groups, and adding/removing users from groups. To add/remove users from groups without access to creating and deleting users and groups, only both use users and use groups are required. See Common Policies.
* Policies
	* The ability to update a policy is available only with manage policies, not use policies, because updating a policy is similar in effect to creating a new policy (you can overwrite the existing policy statements). In addition, inspect policies lets you get the full contents of the policies.
* Object Storage objects
	* **inspect objects** lets you list all the objects in a bucket and do a HEAD operation for a particular object. In comparison, **read objects** lets you download the object itself.
* Load Balancing resources
	* Be aware that inspect load-balancers lets you get all information about your load balancers and related components (backend sets, etc.).
* Networking resources:
	* Be aware that the inspect verb not only returns general information about the cloud network's components (for example, the name and OCID of a security list, or of a route table). It also includes the contents of the component (for example, the actual rules in the security list, the routes in the route table, and so on).
	* Also, the following types of abilities are available only with the manage verb, not the use verb:
		* Update (enable/disable) internet-gateways
	    * Update security-lists
	    * Update route-tables
	    * Update dhcp-options
	    * Attach a dynamic routing gateway (DRG) to a virtual cloud network (VCN)
	    * Create an IPSec connection between a DRG and customer-premises equipment (CPE)
	    * Peer VCNs


## Segments

### Identity and Access Management

**CIS**

* 1.1 - Ensure service level admins are created to manage resources of particular service
* 1.2 -Ensure permissions on all resources are given only to the tenancy administrator group
* 1.3 - Ensure IAM administrators cannot update tenancy Administrators group
* 1.4 - Ensure IAM password policy requires minimum length of 14 or greater
* 1.5, OBP - Ensure IAM password policy expires passwords within 365 days (CIS) or 90 Days (OBP)
* 1.6 - Ensure IAM password policy prevents password reuse
* 1.7 - Ensure MFA is enabled for all users with a console password
* 1.8 - Ensure user API keys rotate within 90 days or less
* 1.9 - Ensure user customer secret keys rotate within 90 days or less
* 1.10 - Ensure user auth tokens rotate within 90 days or less
* 1.11 - Ensure API keys are not created for tenancy administrator users
* 1.12 - Ensure all OCI IAM user accounts have a valid and current email address

**Oracle Best Practices**

* Keep the group of tenancy administrators as small as possible.
* Tenancy administrators should use high-complexity passwords, along with MFA, and periodically rotate their passwords.
* Create a strong console password for each IAM user, including a lowercase letter, uppercase letter, symbol, and number.
* Have security policies granting membership of tenancy administrator group strictly on an as-needed basis.
* After account set up and configuration, do not use the tenancy administrator account for day-to-day operations. Instead, create less privileged users and groups.
* Though administrator accounts are not used for daily operations, they are still needed to address emergency scenarios impacting customer tenancy and operations. Specify secure and auditable "break-glass" procedures for using administrator accounts in such emergencies.
* Disable tenancy administration access immediately when an employee leaves the organization.
* Because the tenancy administrator group membership is restricted, create security policies which prevent administrator account lock-out (for example, if the tenancy administrator leaves the company and no current employees have administrator privileges).
* The recommended unit of administration is IAM groups, which makes it easier to manage and keep track of security permissions (as opposed to individual users). Create IAM groups with permissions to do commonly needed tasks (for example, network administration, volume administration), and assign users to these groups on an as-needed basis.
* Do not share IAM user accounts across multiple users, especially those with administrative accounts.
* Periodically review membership of IAM users in IAM groups, and remove IAM users from groups they do not need access to anymore.
* Do not hard code sensitive IAM credentials directly in software or documents accessible to a wide audience.
* For software application access to Oracle Cloud Infrastructure resources, use instance principals. If it is not feasible to use instance principals, use user environment variables to store credentials, and using locally stored credential files with API keys to be used by the Oracle Cloud Infrastructure SDK or CLI.
* Use federation to manage logins into the Console.
* When using federation, create a federation administrators group that maps to the federated IdP administrator group.* Create a local user belonging to the default tenancy administrator group.
* Create a highly complex Console password or passphrase (18 characters or more, with at least one lowercase letter, one uppercase letter, one number, and one special character) for the local tenancy administrator user.
* Securely escrow the local tenancy administrator user password in an on-premises location (for example, place the password in a sealed envelope in an on-premises physical safe).
* Create security policies for accessing the escrowed password only under specific "break-glass" scenarios.


### Networking

**CIS**

* 2.1 - Ensure no security lists allow ingress from 0.0.0.0/0 to port 22
* 2.2 - Ensure no security lists allow ingress from 0.0.0.0/0 to port 3389
* 2.3 - Ensure no network security groups allow ingress from 0.0.0.0/0 to port 22
* 2.4 - Ensure no network security groups allow ingress from 0.0.0.0/0 to port 3389
* 2.5 - Ensure the default security list of every VCN restricts all traffic except ICMP

**Oracle Best Practices**

* Periodically monitor Oracle Cloud Infrastructure Audit logs to review changes to VCN network security groups, security lists, route table rules, and VCN gateways.
* Place security-sensitive hosts (DB systems, for example) in a private subnet, and use security rules to control the type of connectivity to hosts in a public subnet.
* In addition to VCN security rules, configure host-based firewalls such as iptables, firewalled for network access control, as a defense-in-depth mechanism.
* To prevent unauthorized access or attacks on Compute instances, use a VCN security rule to allow SSH or RDP access only from authorized CIDR blocks rather than leave them open to the internet (0.0.0.0/0).
* Use bastion hosts as a way to control external access (for example, SSH) to VCN hosts. Usually bastion hosts in a VCN public subnet control access to VCN private subnet hosts.
* Use IAM policies to allow only network administrators to make NSG and security list changes.
* Use an IAM policy to allow only network administrators to create or modify VCN gateways.
* Oracle recommends that you limit IAM users who can modify DNS zones and records.


### Logging and Monitoring

**CIS**

* 3.1 - Ensure audit log retention period is set to 365 days
* 3.2 - Ensure default tags are used on resources
* 3.3 - Create at least one notification topic and subscription to receive monitoring alerts
* 3.4 - Ensure a notification is configured for Identity Provider changes
* 3.5 - Ensure a notification is configured for IdP group mapping changes
* 3.6 - Ensure a notification is configured for IAM group changes
* 3.7 - Ensure a notification is configured for IAM policy changes
* 3.8 - Ensure a notification is configured for user changes
* 3.9 - Ensure a notification is configured for VCN changes
* 3.10 - Ensure a notification is configured for changes to route tables
* 3.11 - Ensure a notification is configured for security list changes
* 3.12 - Ensure a notification is configured for network security group changes
* 3.13 - Ensure a notification is configured for changes to network gateways
* 3.14 - Ensure VCN flow logging is enabled for all subnets
* 3.15 - Ensure Cloud Guard is enabled in the root compartment of the tenancy
* 3.16 - Ensure customer created Customer Managed Key (CMK) is rotated at least annually
* 3.17 - Ensure write level Object Storage logging is enabled for all buckets
* Monitor audit logs for accesses by default tenancy administrator and changes to the administrator group, to alert on any unauthorized actions.

### Object Storage

* 4.1 - Ensure no Object Storage buckets are publicly visible

```
oci os bucket get -ns <your_namespace> --bucket-name <bucket_name> | grep "public-access-type"
```

* 4.2 - Ensure Object Storage Buckets are encrypted with a Customer Managed Key (CMK)

**Oracle Best Practices**

* Users without IAM credentials use pre-authenticated requests (PARs) for time-bound access to objects or buckets.
* Enable object versioning to provide data protection against accidental or malicious object update, overwrite, or deletion.
* Give `BUCKET_DELETE` and `OBJECT_DELETE` permissions to a minimum set of IAM users and groups. Grant delete permissions only to tenancy and compartment administrators.

### Asset Management

**CIS**

* 5.1 - Create at least one compartment in your tenancy to store cloud resources
* 5.2 - Ensure no resources are created in the root compartment

### Compute

* Give DELETE permissions only to tenancy and compartment administrators.
* Give INSTANCE_DELETE permissions to a minimal set of groups.
* Limit instance metadata access to privileged users on the instance.
* Periodically apply the latest available software updates to your instances.
* Periodically review these log files to detect any security issues. Example logs: /var/log/secure, /var/log/audit , /var/log/yum.log, /var/log/cloud-init.log
* SSH Recommendations
    * Use public-key logins only
    * Disable password logins
    * Disable root logins
    * Change SSH port to a non-standard port
    * Use secure SSH private keys to access instances and to prevent inadvertent disclosures.
* Establish a baseline for security hardening of Linux and Windows images running on instances.

### Block Volume Management

**Oracle Best Practices**

* Assign least privilege access for IAM users and groups to resource types in volume-family.
* To minimize loss of data due to deletes or corruption, make periodic backups of volumes.
* DELETE permissions should be given only to tenancy and compartment administrators.

### GoldenGate

GoldenGate is a data replication solution.

**Oracle Best Practices**

* Assign least privilege access for IAM users and groups to resource types in goldengate-family.
* To minimize loss of data from inadvertent deletes by an authorized user or malicious deletes, Oracle recommends giving the `GOLDENGATE_DEPLOYMENT_DELETE` and `GOLDENGATE_DATABASE_REGISTRATION_DELETE` permissions to the minimum possible set of IAM users and groups. Give these permissions only to tenancy and compartment administrators.
* GoldenGate only needs USE level access to capture data from database registrations.

### Cloud Advisor

**Oracle Best Practices**

* Your security reponsibility (as opposed to Oracle's) includes the following area:
	* Access Control: Limit privileges as much as possible. Users should be given only the access necessary to perform their work.
* Use policies to limit access to Cloud Advisor.
	* Assign a group the least privileges that are required to perform their responsibilities. Each policy has a verb. From the least amount of access to the most, the available verbs are: inspect, read, use, and manage.
	* Create this policy to allow group CloudAdvisorUsers to perform all actions in Cloud Advisor except deleting profiles.
	```
	Allow group CloudAdvisorUsers to manage optimizer-api-family in tenancy
 	where request.permission!='OPTIMIZER_PROFILE_DELETE'
	```
* Cloud Advisor uses standard Oracle Cloud Infrastructure encryption for all data stored at rest in the service. No configuration is necessary.
* Cloud Advisor does not use Vault keys. Internally, Cloud Advisor stores data in an Autonomous Database that uses Vault keys. Oracle manages and secures these resources.
* Cloud Advisor creates backups daily. No configuration is necessary.

### Container Engine for Kubernetes

**Oracle Best Practices**

* Do not run mutually distrusted workloads in the same cluster. Examples of workloads that should not be run in the same cluster:
	* Development workloads and production workloads
	* Control plane and data plane
	* Workloads that run arbitrary customer code
* Only use private subnets for node pools. A service gateway should be configured to provide access to Oracle Cloud Infrastructure services. A service gateway cannot be used if the subnets are public with an internet gateway. use a NAT gateway for private subnets that require access to the internet.
* To block access internet access, use a network policy plugin with a default policy of "deny all". Then, explicitly grant access to pods and networks using NetworkPolicy resources in Kubernetes via label selectors.
* If you do not have a network policy plugin installed, you can use a IPTables rule to restrict access from all pods on the host. Do not use this approach to block a subset of pods on a host.
* Only pull images using the image digests, and not pull images using tags (because image tags are mutable). Image digests are the sha256 digest of your image, which allows docker to verify the image it downloaded is what you expected.
* Add-ons
    * Tiller add-on (optional) - Do not use for production clusters because of the security risks associated with Tiller. Clusters provisioned with Tiller do not have authentication or authorization for API calls made to Tiller, which means they cannot provide attribution for requests. Therefore, any operator or service that can reach Tiller can invoke its APIs with Tiller access. To solve the security problems associated with Tiller, Helm V3 was developed. The Helm V3 release completely removed Tiller from Helm. We recommend that you consider using Helm V3 if you'd like to utilize the functionality offered by Helm+Tiller.
    * Kubernetes Dashboard add-on (Optional) - Do not install this add-on on production clusters due to the lack of extensible authentication support. Consequently, you cannot specify that you want to install the Kubernetes Dashboard when creating a cluster using the Console. If you decide you do want to install the Kubernetes Dashboard, create the cluster using the API and set the isKubernetesDashboardEnabled attribute to true.
    * If you do install the Kubernetes Dashboard, restrict access within clusters and do notexposing it externally via either a load balancer or an ingress controller. The Kubernetes Dashboard is a common attack vector used to gain access to a Kubernetes Cluster.

### Data Catalog

**Oracle Best Practices**

* Assign least privilege access for IAM users and groups to resource types in data-catalog-family.
* To minimize loss of data due to inadvertent deletes by an authorized user or malicious deletes, Oracle recommends to giving `CATALOG_DELETE` permission to a minimum possible set of IAM users and groups. Give `CATALOG_DELETE` permissions only to tenancy and compartment admins.
* To protect your data sources from any security vulnerability, provide credentials to read-only accounts only. Data Catalog only needs read access to harvest data assets.

### Data Integration

**Oracle Best Practices**

* Assign least privilege access for IAM users and groups to resource types in dis-family.
* To minimize loss of data due to inadvertent deletes by an authorized user or malicious deletes, Oracle recommends to giving DIS_WORKSPACE_DELETE permission to a minimum possible set of IAM users and groups. Give DIS_WORKSPACE_DELETE * permissions only to tenancy and compartment admins.
* To protect your data sources from any security vulnerability, provide credentials to read-only accounts only. Data * Integration only needs read access to ingest data from data assets.

### Data Transfer

**Oracle Best Practices**

* Go to [Oracle's website](https://docs.oracle.com/en-us/iaas/Content/Security/Reference/datatransfer_security.htm) for more information.

### Database

**Oracle Best Practices**

* Use strong database passwords be strong. For guidelines on choosing Oracle database passwords, see [Guidelines for Securing Passwords](https://docs.oracle.com/cd/E11882_01/network.112/e36292/guidelines.htm#DBSEG10005). In addition, Oracle database provides a PL/SQL script to verify database password complexity. This script is located at `ORACLE_HOME/rdbms/admin/UTLPWDMG.SQL`. For instructions on running UTLPWDMG.SQL script to verify password complexity, see Enforcing Password Complexity Verification.
* Configure VCN network security groups or security lists to allow least privilege access to customer databases in Oracle Cloud Infrastructure Database. To perform OS patching and backup for a DB system on private subnet, you can use a service gateway or a NAT gateway to connect to your patching or backup endpoints.
* Give database delete permissions (`DATABASE_DELETE`, `DB_SYSTEM_DELETE`) to a minimum possible set of IAM users and groups. Only give `DELETE` permissions to tenancy and compartment administrators.
* Use managed backups (backups created using the Oracle Cloud Infrastructure Console or the API) whenever possible.
    * With managed backups, Oracle manages the object store user and credentials, and rotates these credentials every 3 days. Oracle Cloud Infrastructure encrypts all managed backups in the object store. Oracle uses the Database Transparent Encryption feature by default for encrypting the backups.
* If you are not using managed backups, Oracle recommends that you change the object store passwords at regular intervals.
* If a custom password is set for the Oracle Wallet, set a strong password (eight characters or more, with at least one capital letter, one small letter, one number, and one special symbol)
* Periodically rotate the TDE master key. The recommended rotation period is 90 days or less.
Applying Oracle database security patches (Oracle Critical Patch Updates) is imperative to mitigate known security issues, and Oracle recommends that you keep patches up-to-date. Patchsets and Patch Set Updates (PSUs) are released on a quarterly basis. These patch releases contain security fixes and additional high-impact/low-risk critical bug fixes.

For information about the latest known security issues and available fixes, see Critical Patch Updates, Security Alerts and Bulletins. If your application does not support the latest patches and needs to use a DB system with older patches, you can provision a DB system with an older version of the Oracle Database edition you are using. In addition to reviewing the critical patch updates and security alerts for your Oracle Database, Oracle recommends that you analyze and patch the operating system provisioned with the DB system.

The Oracle Database Security Assessment Tool (DBSAT) provides automated security configuration checks of Oracle databases in Oracle Cloud Infrastructure. DBSAT performs security checks for user privilege analysis, database authorization controls, auditing polices, database listener configuration, OS file permissions, and sensitive data stored. Oracle database images in Oracle Cloud Infrastructure Database are scanned with DBSAT before provisioning. After provisioning, Oracle recommends that you periodically scan databases with DBSAT, and remediate any issues found. DBSAT is available free of charge to Oracle customers.

Oracle recommends using Managed backups (backups created using the Oracle Cloud Infrastructure Console or the API) whenever possible. When you use managed backups, Oracle manages the object store user and credentials, and rotates these credentials every 3 days. Oracle Cloud Infrastructure encrypts all managed backups in the object store. Oracle uses the Database Transparent Encryption feature by default for encrypting the backups.

If you are not using managed backups, Oracle recommends that you change the object store passwords at regular intervals.

### Email Delivery

**Oracle Best Practices**

* Create a separate IAM user for SMTP. This user must have manage permissions for approved-senders and suppressions resource types.
* Securely store the SMTP credential, and periodically rotate it.

### File Storage

**Oracle Best Practices**

* Use VCN security lists (of the mount target subnet) to configure network access to the mount target from only authorized IP addresses.
	* The File Storage Service exposes an NFSv3 endpoint as a mount target in each customer's VCN subnet. The mount target is identified by a DNS name and is mapped to an IP address.
* For data durability, Oracle recommends that you take periodic snapshots of the file system. To minimize accidental deletion of data, constrain the set of users having privileges to delete mount targets, file-systems, and snapshots.
	* All file-system data is encrypted at rest.
* Use well-known NFS security best practices such as the `all_squash` option to map all users to nfsnobody, and NFS ACLs to enforce access control to the mounted file system.

### Resource Manager

**Oracle Best Practices**

* For recommended Resource Manager policies, see [Policies for Managing Resources Used with Resource Manager](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingstacksandjobs.htm#Policies_for_Managing_Stacks_and_Jobs)

* The Resource Manager workflow typically includes writing or generating a Terraform configuration that is then used to manage your stack. Because the Terraform configuration can be accessed using the Resource Manager API GetJobTfConfig, we recommend that you do not include sensitive information in your configuration files.

* Terraform state (.tfstate) can contain sensitive data, including resource IDs and in some cases sensitive user data like passwords. HashiCorp provides recommendations for handling Terraform state in the article [Sensitive Data in State](https://www.terraform.io/docs/state/sensitive-data.html).