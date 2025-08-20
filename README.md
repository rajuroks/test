| rex field=vulnerableAsset.cloudProviderURL "(?<baseURL>https:\/\/[^\/]+\/ec2\/v2\/home\?region=[^#]+#)"
